import asyncio
from datetime import UTC, datetime
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db import get_db
from app.models import (
    Alert,
    AuditLog,
    ChatMessage,
    DefectInspection,
    EnergyReading,
    GeneratedReport,
    InventoryItem,
    Machine,
    MaintenanceRecord,
    Product,
    ProductionOrder,
    SensorReading,
    User,
)
from app.schemas import (
    AlertOut,
    ChatRequest,
    ChatResponse,
    EnergyOut,
    InspectionCreate,
    InspectionOut,
    InventoryOut,
    MachineOut,
    MaintenanceOut,
    ProductionOrderOut,
    ProductOut,
    ReportOut,
    ReportRequest,
    SensorReadingOut,
    UserOut,
)
from app.services.analytics import dashboard_snapshot
from app.services.copilot import answer_factory_question
from app.services.reports import create_report_pdf
from app.services.vision import inspect_product

router = APIRouter(tags=["Factory Operations"])


@router.get("/analytics/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return dashboard_snapshot(db)


@router.get("/machines", response_model=list[MachineOut])
def list_machines(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[Machine]:
    return list(db.scalars(select(Machine).order_by(Machine.code)).all())


@router.get("/machines/{machine_id}", response_model=MachineOut)
def get_machine(
    machine_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> Machine:
    machine = db.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine


@router.get("/sensors", response_model=list[SensorReadingOut])
def list_sensor_readings(
    machine_id: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[SensorReading]:
    statement = select(SensorReading).order_by(SensorReading.recorded_at.desc()).limit(100)
    if machine_id:
        statement = statement.where(SensorReading.machine_id == machine_id)
    return list(db.scalars(statement).all())


@router.get("/maintenance", response_model=list[MaintenanceOut])
def list_maintenance(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[MaintenanceRecord]:
    return list(db.scalars(select(MaintenanceRecord).order_by(MaintenanceRecord.due_at)).all())


@router.get("/alerts", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[Alert]:
    return list(db.scalars(select(Alert).order_by(Alert.created_at.desc())).all())


@router.post("/alerts/{alert_id}/acknowledge", response_model=AlertOut)
def acknowledge_alert(
    alert_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Alert:
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="alert.acknowledged",
            entity_type="alert",
            entity_id=alert.id,
        )
    )
    db.commit()
    db.refresh(alert)
    return alert


@router.get("/production", response_model=list[ProductionOrderOut])
def list_production(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[ProductionOrder]:
    return list(db.scalars(select(ProductionOrder).order_by(ProductionOrder.due_at)).all())


@router.get("/inventory", response_model=list[InventoryOut])
def list_inventory(
    low_stock: bool = False,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[InventoryItem]:
    items = list(db.scalars(select(InventoryItem).order_by(InventoryItem.name)).all())
    return [item for item in items if item.quantity <= item.reorder_point] if low_stock else items


@router.get("/products", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.name)).all())


@router.get("/energy", response_model=list[EnergyOut])
def list_energy(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[EnergyReading]:
    return list(db.scalars(select(EnergyReading).order_by(EnergyReading.recorded_at.desc())).all())


@router.get("/vision", response_model=list[InspectionOut])
def inspection_history(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[DefectInspection]:
    return list(
        db.scalars(select(DefectInspection).order_by(DefectInspection.inspected_at.desc())).all()
    )


@router.post("/vision/inspect", response_model=InspectionOut, status_code=201)
def create_inspection(
    payload: InspectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("factory_admin", "quality_inspector")),
) -> DefectInspection:
    inspection = DefectInspection(**inspect_product(payload))
    db.add(inspection)
    db.flush()
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="vision.inspected",
            entity_type="inspection",
            entity_id=inspection.id,
            details={"result": inspection.result},
        )
    )
    db.commit()
    db.refresh(inspection)
    return inspection


@router.post("/chat", response_model=ChatResponse)
def chat_with_factory(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    result = answer_factory_question(db, payload.question)
    db.add(
        ChatMessage(
            user_id=current_user.id,
            question=payload.question,
            answer=result.answer,
            sources=result.sources,
        )
    )
    db.commit()
    return ChatResponse(answer=result.answer, sources=result.sources)


@router.post("/reports/pdf")
def export_pdf(
    payload: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("factory_admin", "production_manager", "executive")),
) -> StreamingResponse:
    report = create_report_pdf(db, payload.title, payload.report_type)
    db.add(
        GeneratedReport(
            title=payload.title,
            report_type=payload.report_type,
            generated_by=current_user.id,
        )
    )
    db.commit()
    filename = "".join(char if char.isalnum() else "-" for char in payload.title.lower()).strip("-")
    return StreamingResponse(
        BytesIO(report),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename or "factory-report"}.pdf"'
        },
    )


@router.get("/reports", response_model=list[ReportOut])
def list_reports(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[GeneratedReport]:
    return list(
        db.scalars(select(GeneratedReport).order_by(GeneratedReport.created_at.desc())).all()
    )


@router.get("/users", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("factory_admin")),
) -> list[User]:
    return list(db.scalars(select(User).order_by(User.full_name)).all())


@router.get("/settings")
def application_settings(_: User = Depends(require_roles("factory_admin"))) -> dict:
    return {
        "features": {
            "mqtt": True,
            "opc_ua": False,
            "ollama": True,
            "openai": True,
            "vision": True,
        }
    }


@router.websocket("/ws/telemetry")
async def telemetry_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(
                {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "machine_code": "PRESS-02",
                    "metric": "vibration",
                    "value": 4.7,
                    "unit": "mm/s",
                }
            )
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        return
