# Ledger API

A double-entry bookkeeping API built with FastAPI, PostgreSQL, and SQLAlchemy.

Inspired by real-world ERP and fintech systems (Stripe, Ramp, QuickBooks) where every financial event is recorded as a balanced journal entry.

## What it does

- Create accounts (Cash, Revenue, Expenses, etc.)
- Post journal entries with debit/credit lines
- Enforces double-entry rule: **sum(debits) must equal sum(credits)**
- Generate a Trial Balance report across all accounts

## Tech Stack

- **FastAPI** — REST API framework
- **SQLAlchemy 2.0** — ORM (synchronous)
- **Alembic** — database migrations
- **PostgreSQL** — primary database
- **Docker Compose** — local development environment
- **pytest** — integration tests with isolated transactions
- **GitHub Actions** — CI on every push

## Getting Started

### With Docker (recommended)

    docker compose up --build

API will be available at http://localhost:8000
Interactive docs: http://localhost:8000/docs

### Without Docker (local)

    python3.12 -m venv .ven    python3.12 -m venv .ven    python3.12 -m venv .ven    python3.12 -m venv ic upgrade head
    uvicorn app.main:app --reload

## API Endpoints

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| GET    | `/ping`          | Health check             |
| POST   | `/accounts`      | Create an account        |
| GET    | `/accounts`      | List all accounts        |
| POST   | `/entries`       | Post a journal entry     |
| GET    | `/trial-balance` | Get trial balance report |

## Example Usage

Create accounts:

    curl -X POST http://localhost:8000/accounts \
      -H "Content-Type: application/json" \
      -d '{"name": "Cash"}'

Post a journal entry:

    curl -X POST http://localhost:8000/entries \
      -H "Content-Type: application/json" \
      -d '{
        "description": "Customer payment received",
        "lines": [
          {"account_id": 1, "amount": "1000.00", "type": "debit"},
          {"account_id": 2, "amount": "1000.00", "type": "credit"}
        ]
      }'

Get trial balance:

    curl http://localhost:8000/trial-balance

## Running Tests

    ENV_FILE=.env.local pytest -q

Tests use an isolated PostgreSQL database with transaction rollback after each test.

## Project Structure

    ledger-api/
    ├── app/
    │   ├── main.py          # FastAPI routes
    │   ├── db.py            # SQLAlchemy engine & session
    │   ├── models.py        # ORM models
    │   ├── schemas.py       # Pydantic schemas
    │   └── services/
    │       └── ledger.py    # Business logic (balance validation)
    ├── alembic/             # Database migrations
    ├── tests/               # pytest test suite
    ├── Dockerfile
    ├── docker-compose.yml
    └── .github/workflows/   # GitHub Actions CI
