from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    Alert,
    DefectInspection,
    EnergyReading,
    InventoryItem,
    Machine,
    ProductionOrder,
)
from app.schemas import AlertOut, MachineOut


def dashboard_snapshot(db: Session) -> dict:
    machines = list(db.scalars(select(Machine)).all())
    orders = list(db.scalars(select(ProductionOrder)).all())
    alerts = list(
        db.scalars(
            select(Alert).where(Alert.acknowledged.is_(False)).order_by(Alert.created_at.desc())
        ).all()
    )
    total_target = sum(order.target_quantity for order in orders)
    total_actual = sum(order.actual_quantity for order in orders)
    energy = db.scalar(select(func.coalesce(func.sum(EnergyReading.consumption_kwh), 0))) or 0
    defects = (
        db.scalar(
            select(func.count())
            .select_from(DefectInspection)
            .where(DefectInspection.result == "fail")
        )
        or 0
    )
    inventory = list(db.scalars(select(InventoryItem)).all())
    return {
        "kpis": {
            "oee": 84.6,
            "production_today": total_actual,
            "production_target": total_target,
            "running_machines": sum(machine.status == "running" for machine in machines),
            "machine_count": len(machines),
            "energy_kwh": round(float(energy), 1),
            "quality_score": 98.2,
            "rejected_products": defects,
            "open_alerts": len(alerts),
            "low_stock_items": sum(item.quantity <= item.reorder_point for item in inventory),
        },
        "machines": [
            MachineOut.model_validate(machine).model_dump(mode="json") for machine in machines
        ],
        "alerts": [AlertOut.model_validate(alert).model_dump(mode="json") for alert in alerts[:5]],
        "production_trend": [
            {"label": "06:00", "actual": 240, "target": 260},
            {"label": "08:00", "actual": 510, "target": 520},
            {"label": "10:00", "actual": 760, "target": 780},
            {"label": "12:00", "actual": 1030, "target": 1040},
            {"label": "14:00", "actual": total_actual, "target": total_target},
        ],
        "energy_trend": [
            {"label": "Mon", "kwh": 1200},
            {"label": "Tue", "kwh": 1110},
            {"label": "Wed", "kwh": 1260},
            {"label": "Thu", "kwh": 1180},
            {"label": "Fri", "kwh": float(energy)},
        ],
    }
