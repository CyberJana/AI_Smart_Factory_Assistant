from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import (
    Alert,
    DefectInspection,
    Document,
    EnergyReading,
    InventoryItem,
    Machine,
    MaintenanceRecord,
    Product,
    ProductionOrder,
    SensorReading,
    User,
)


def seed_demo_data(db: Session) -> None:
    if db.scalar(select(User).limit(1)):
        return

    admin = User(
        email="admin@smartfactory.example",
        full_name="Avery Morgan",
        hashed_password=hash_password("ChangeMe123!"),
        role="factory_admin",
        is_verified=True,
    )
    db.add(admin)
    machines = [
        Machine(
            code="CNC-01",
            name="CNC Milling Cell 01",
            location="Assembly Line A",
            status="running",
            health_score=96.0,
            utilization=89.0,
        ),
        Machine(
            code="PRESS-02",
            name="Hydraulic Press 02",
            location="Forming Line B",
            status="warning",
            health_score=68.0,
            utilization=72.0,
        ),
        Machine(
            code="ROBOT-04",
            name="Welding Robot 04",
            location="Assembly Line A",
            status="running",
            health_score=92.0,
            utilization=94.0,
        ),
        Machine(
            code="PACK-03",
            name="Packaging Station 03",
            location="Packaging",
            status="maintenance",
            health_score=55.0,
            utilization=0.0,
        ),
    ]
    db.add_all(machines)
    db.flush()

    now = datetime.now(UTC)
    readings = []
    telemetry = {
        "CNC-01": [("temperature", 68.4, "C"), ("vibration", 1.8, "mm/s"), ("rpm", 2450, "rpm")],
        "PRESS-02": [
            ("temperature", 77.9, "C"),
            ("vibration", 4.7, "mm/s"),
            ("pressure", 122, "bar"),
        ],
        "ROBOT-04": [
            ("temperature", 61.3, "C"),
            ("current", 18.2, "A"),
            ("vibration", 1.2, "mm/s"),
        ],
        "PACK-03": [("temperature", 43.1, "C"), ("current", 0.0, "A"), ("humidity", 48.0, "%")],
    }
    for machine in machines:
        for metric, value, unit in telemetry[machine.code]:
            readings.append(
                SensorReading(
                    machine_id=machine.id,
                    metric=metric,
                    value=value,
                    unit=unit,
                    recorded_at=now,
                )
            )
    db.add_all(readings)
    db.add_all(
        [
            MaintenanceRecord(
                machine_id=machines[1].id,
                title="Inspect hydraulic pump vibration",
                maintenance_type="predictive",
                priority="high",
                status="open",
                due_at=now + timedelta(hours=8),
                notes="Vibration has exceeded the baseline for three shifts.",
            ),
            MaintenanceRecord(
                machine_id=machines[3].id,
                title="Replace packaging conveyor belt",
                maintenance_type="corrective",
                priority="medium",
                status="in_progress",
                due_at=now + timedelta(days=1),
                notes="Planned during the maintenance window.",
            ),
        ]
    )
    db.add_all(
        [
            Alert(
                machine_id=machines[1].id,
                title="High vibration on PRESS-02",
                severity="high",
                message="Current vibration is 4.7 mm/s, 34% above the operating baseline.",
            ),
            Alert(
                machine_id=machines[3].id,
                title="Maintenance window active",
                severity="info",
                message="PACK-03 is unavailable until the conveyor belt replacement is complete.",
            ),
        ]
    )
    db.add_all(
        [
            Product(sku="FG-HOUSING-A", name="Precision Housing A", category="finished_good"),
            Product(sku="FG-BRACKET-B", name="Control Bracket B", category="finished_good"),
        ]
    )
    db.add_all(
        [
            ProductionOrder(
                order_number="WO-2026-0812",
                product_name="Precision Housing A",
                target_quantity=2400,
                actual_quantity=1820,
                status="in_progress",
                due_at=now + timedelta(days=1),
            ),
            ProductionOrder(
                order_number="WO-2026-0813",
                product_name="Control Bracket B",
                target_quantity=1800,
                actual_quantity=1800,
                status="completed",
                due_at=now,
            ),
        ]
    )
    db.add_all(
        [
            InventoryItem(
                sku="RM-AL-6061",
                name="Aluminium 6061 Sheet",
                category="raw_material",
                quantity=780,
                reorder_point=1000,
                unit="kg",
                location="Warehouse A",
            ),
            InventoryItem(
                sku="RM-BOLT-M8",
                name="M8 Fastener",
                category="raw_material",
                quantity=14200,
                reorder_point=8000,
                unit="pcs",
                location="Warehouse B",
            ),
            InventoryItem(
                sku="FG-HOUSING-A",
                name="Precision Housing A",
                category="finished_good",
                quantity=620,
                reorder_point=400,
                unit="pcs",
                location="Finished Goods",
            ),
        ]
    )
    db.add_all(
        [
            EnergyReading(
                machine_id=machines[0].id,
                source="electricity",
                consumption_kwh=421.3,
                carbon_kg=168.5,
                recorded_at=now - timedelta(hours=3),
            ),
            EnergyReading(
                machine_id=machines[1].id,
                source="electricity",
                consumption_kwh=338.7,
                carbon_kg=135.5,
                recorded_at=now - timedelta(hours=2),
            ),
            EnergyReading(
                machine_id=machines[2].id,
                source="compressed_air",
                consumption_kwh=189.2,
                carbon_kg=75.7,
                recorded_at=now - timedelta(hours=1),
            ),
        ]
    )
    db.add_all(
        [
            DefectInspection(
                product_code="HOUSING-A-1042",
                result="pass",
                defect_type=None,
                confidence=0.991,
                bounding_boxes=[],
            ),
            DefectInspection(
                product_code="HOUSING-A-1043",
                result="fail",
                defect_type="surface_scratch",
                confidence=0.944,
                bounding_boxes=[{"x": 0.23, "y": 0.41, "width": 0.18, "height": 0.12}],
            ),
        ]
    )
    db.add_all(
        [
            Document(
                title="Hydraulic Press Vibration SOP",
                document_type="sop",
                content=(
                    "When vibration on a hydraulic press exceeds 4.0 mm/s for two consecutive "
                    "measurements, schedule a pump and bearing inspection within one shift."
                ),
            ),
            Document(
                title="Daily Production Handover",
                document_type="production_report",
                content=(
                    "Assembly Line A is tracking at 75.8 percent against its current target. "
                    "Packaging Station 03 is under corrective maintenance."
                ),
            ),
        ]
    )
    db.commit()
