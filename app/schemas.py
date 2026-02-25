from decimal import Decimal
from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field, PlainSerializer

# Кастомный тип: всегда сериализуется с 2 знаками после запятой
Money = Annotated[
    Decimal,
    PlainSerializer(lambda x: f"{x:.2f}", return_type=str, when_used="json"),
]


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class AccountOut(BaseModel):
    id: int
    name: str


class EntryType(str, Enum):
    debit = "debit"
    credit = "credit"


class JournalLineIn(BaseModel):
    account_id: int
    amount: Decimal = Field(gt=0, decimal_places=2)
    type: EntryType


class JournalEntryCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    lines: list[JournalLineIn] = Field(min_length=2)


class JournalLineOut(BaseModel):
    id: int
    account_id: int
    amount: Money
    type: EntryType


class JournalEntryOut(BaseModel):
    id: int
    description: str
    lines: list[JournalLineOut]


class TrialBalanceLine(BaseModel):
    account_id: int
    account_name: str
    total_debits: Money
    total_credits: Money
    balance: Money
