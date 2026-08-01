from dataclasses import dataclass
from re import findall

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Alert, Document, Machine, MaintenanceRecord


@dataclass
class CopilotAnswer:
    answer: str
    sources: list[str]


def _keywords(question: str) -> set[str]:
    return {word.lower() for word in findall(r"[a-zA-Z]{3,}", question)}


def answer_factory_question(db: Session, question: str) -> CopilotAnswer:
    """Provide local RAG behavior; replace this adapter with an LLM provider in production."""
    terms = _keywords(question)
    documents = list(db.scalars(select(Document)).all())
    ranked = sorted(
        documents,
        key=lambda document: len(
            terms.intersection(_keywords(document.title + " " + document.content))
        ),
        reverse=True,
    )
    sources = [
        document.title for document in ranked[:2] if terms.intersection(_keywords(document.content))
    ]
    lower_question = question.lower()

    if "maintenance" in lower_question or "vibration" in lower_question:
        work = list(
            db.scalars(
                select(MaintenanceRecord).where(
                    MaintenanceRecord.status.in_(["open", "in_progress"])
                )
            ).all()
        )
        alerts = list(db.scalars(select(Alert).where(Alert.acknowledged.is_(False))).all())
        action = work[0].title if work else "No maintenance work is currently open."
        high_alerts = [alert.title for alert in alerts if alert.severity in {"high", "critical"}]
        details = f"Priority action: {action}."
        if high_alerts:
            details += f" Active high-risk alert: {high_alerts[0]}."
        return CopilotAnswer(answer=details, sources=sources or ["Hydraulic Press Vibration SOP"])

    if "machine" in lower_question or "health" in lower_question:
        machine = db.scalar(select(Machine).order_by(Machine.health_score.asc()))
        if machine:
            return CopilotAnswer(
                answer=(
                    f"{machine.name} ({machine.code}) needs attention first. Its health score is "
                    f"{machine.health_score:.0f}/100 and its current status is {machine.status}."
                ),
                sources=sources,
            )

    context = ranked[0].content if ranked else "No indexed factory documents matched the question."
    return CopilotAnswer(
        answer=f"Based on the available factory records: {context}",
        sources=sources or ["Factory operational data"],
    )
