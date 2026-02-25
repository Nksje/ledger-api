from decimal import Decimal
from app.schemas import JournalEntryCreate


def validate_balance(payload: JournalEntryCreate) -> None:
    """Сумма дебетов должна равняться сумме кредитов."""
    debits = sum(l.amount for l in payload.lines if l.type == "debit")
    credits = sum(l.amount for l in payload.lines if l.type == "credit")
    if debits != credits:
        raise ValueError(f"Debits ({debits}) != Credits ({credits})")
