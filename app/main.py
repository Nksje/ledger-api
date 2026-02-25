from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import get_db
from app.models import Account, JournalEntry, JournalLine
from app.schemas import (
    AccountCreate, AccountOut,
    JournalEntryCreate, JournalEntryOut,
)
from app.services.ledger import validate_balance

app = FastAPI(title="Ledger API")


@app.get("/ping")
def ping():
    return {"ping": "pong"}


@app.get("/accounts", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.execute(select(Account)).scalars().all()


@app.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(Account).where(Account.name == payload.name)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Account with this name already exists")
    acc = Account(name=payload.name)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc


@app.post("/entries", response_model=JournalEntryOut, status_code=201)
def create_entry(payload: JournalEntryCreate, db: Session = Depends(get_db)):
    try:
        validate_balance(payload)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    entry = JournalEntry(description=payload.description)
    for line in payload.lines:
        entry.lines.append(
            JournalLine(
                account_id=line.account_id,
                amount=line.amount,
                type=line.type.value,
            )
        )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
