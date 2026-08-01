from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from sqlalchemy.orm import Session

from app.services.analytics import dashboard_snapshot


def create_report_pdf(db: Session, title: str, report_type: str) -> bytes:
    summary = dashboard_snapshot(db)["kpis"]
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter, title=title)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 16),
        Paragraph(f"Report type: {report_type.title()}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(f"Overall equipment effectiveness: {summary['oee']}%", styles["Normal"]),
        Paragraph(
            (
                f"Production: {summary['production_today']:,} of "
                f"{summary['production_target']:,} units"
            ),
            styles["Normal"],
        ),
        Paragraph(
            f"Running machines: {summary['running_machines']} of {summary['machine_count']}",
            styles["Normal"],
        ),
        Paragraph(f"Energy consumption: {summary['energy_kwh']:,.1f} kWh", styles["Normal"]),
        Paragraph(f"Open alerts: {summary['open_alerts']}", styles["Normal"]),
    ]
    document.build(story)
    return buffer.getvalue()
