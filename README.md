<div align="center">

# banklyze

Official Python SDK for the [Banklyze API](https://banklyze.com)

[![PyPI version](https://img.shields.io/pypi/v/banklyze)](https://pypi.org/project/banklyze/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-brightgreen)](https://python.org)
[![Typing: strict](https://img.shields.io/badge/typing-strict-blue)](https://peps.python.org/pep-0561/)

AI-powered bank statement analysis for MCA underwriting.
<br />Fully typed. Sync + async. Pydantic v2.

[Documentation](https://docs.banklyze.com) &nbsp;&middot;&nbsp; [API Reference](https://docs.banklyze.com/api) &nbsp;&middot;&nbsp; [Changelog](CHANGELOG.md)

</div>

---

## Install

```bash
pip install banklyze
```

## Quick Start

```python
from banklyze import BanklyzeClient

client = BanklyzeClient(api_key="bk_live_...")

# Create a deal and upload a statement
deal = client.deals.create(business_name="Acme Trucking LLC")
doc = client.documents.upload(deal.id, "chase_jan_2026.pdf")

# Get the underwriting result
detail = client.deals.get(deal.id)
print(detail.health.health_grade)        # "B"
print(detail.recommendation.decision)    # "approved"

client.close()
```

## Why This SDK

- **Fully typed** — every method returns a Pydantic model. Full IDE autocompletion, not `dict`.
- **Sync + async** — `BanklyzeClient` and `AsyncBanklyzeClient` with identical APIs.
- **Automatic retries** — exponential backoff with jitter, rate limit aware, safe for mutations.
- **Forward compatible** — all models use `extra="allow"`. API additions never break your code.

## Usage

### Typed Responses

Every response is a Pydantic model with nested sub-objects:

```python
detail = client.deals.get(42)

# Financials
detail.financials.avg_monthly_deposits
detail.financials.avg_daily_balance

# Health scoring (12 sub-factors)
for name, factor in detail.health.factors.items():
    print(f"{name}: {factor.score}/{factor.max}")

# Underwriting recommendation
detail.recommendation.decision    # "approved" | "conditional" | "declined"
detail.recommendation.risk_factors
detail.recommendation.strengths
```

### Async Client

```python
from banklyze import AsyncBanklyzeClient

async with AsyncBanklyzeClient(api_key="bk_live_...") as client:
    deals = await client.deals.list(status="ready")
    for deal in deals.data:
        print(deal.business_name, deal.health_grade)
```

### Auto-Pagination

Iterate over all items across pages automatically:

```python
for deal in client.deals.list_all(status="ready"):
    print(deal.business_name, deal.health_grade)  # typed DealSummary
```

### Document Analysis

```python
doc = client.documents.get(doc_id)

# Pre-screen (regex-based, no LLM cost)
doc.prescreen.bank_name
doc.prescreen.viable
doc.prescreen.confidence

# Tamper detection
doc.integrity.tampering_risk_level  # "clean" | "low" | "medium" | "high"

# Extraction quality
doc.extraction_confidence_detail.overall_confidence
doc.extraction_confidence_detail.overall_tier
```

### Real-Time Streaming

Stream pipeline progress via Server-Sent Events:

```python
for event in client.events.stream(deal_id=42):
    print(event.event, event.data)
```

### Webhook Verification

```python
from banklyze.webhooks import verify_signature

verify_signature(
    payload=request.body,
    signature=request.headers["X-Webhook-Signature"],
    secret="whsec_...",
)
```

### Error Handling

```python
from banklyze.exceptions import NotFoundError, RateLimitError, ValidationError

try:
    client.deals.get(999)
except NotFoundError:
    pass  # 404 — deal doesn't exist
except RateLimitError as e:
    print(f"Retry after {e.retry_after}s")
except ValidationError as e:
    print(e.body)  # validation details

# All errors include e.request_id for support correlation
```

### Idempotency

```python
client.deals.create(
    business_name="Acme Trucking LLC",
    idempotency_key="create-acme-001",  # safe to retry
)
```

## Configuration

```python
client = BanklyzeClient(
    api_key="bk_live_...",
    base_url="https://api.banklyze.com",  # default
    timeout=30.0,                          # seconds, default
    max_retries=2,                         # default
)

# Or as a context manager
with BanklyzeClient(api_key="bk_live_...") as client:
    deals = client.deals.list()
```

| Timeout Constant | Value | Use Case |
|-----------------|-------|----------|
| `TIMEOUT_READ` | 10 s | List, get |
| `TIMEOUT_WRITE` | 30 s | Create, update |
| `TIMEOUT_UPLOAD` | 120 s | File uploads |
| `TIMEOUT_REPORT` | 300 s | PDF generation |

## Resources

| Resource | Access | Methods |
|----------|--------|---------|
| **Deals** | `client.deals` | CRUD, decision, evaluate, notes, stats, analytics, batch |
| **Documents** | `client.documents` | Upload, bulk upload, status, reprocess, triage, classify |
| **Transactions** | `client.transactions` | List, correct, corrections history |
| **Exports** | `client.exports` | Deal/document CSV and PDF |
| **Events** | `client.events` | SSE streams (deal, org, batch) |
| **Webhooks** | `client.webhooks` | Config, test, delivery logs, retry |
| **Rulesets** | `client.rulesets` | Underwriting criteria CRUD, set default |
| **Ingest** | `client.ingest` | Bulk CRM ingest with batch tracking |
| **BVL** | `client.bvl` | Business validation, call queue, SAM entities |
| **SAM Profiles** | `client.sam_profiles` | SAM.gov search profiles, watchers, triggers |
| **Reviews** | `client.reviews` | Document review queue, approve/correct |
| **Instant** | `client.instant` | Free-tier instant PDF analysis |
| **Team** | `client.team` | Invite, update, deactivate members |
| **Keys** | `client.keys` | API key management |
| **Notifications** | `client.notifications` | In-app notifications, preferences |
| **CRM** | `client.crm` | Provider config, field mapping, sync |
| **Integrations** | `client.integrations` | Slack, Teams, SMTP |
| **Shares** | `client.shares` | Public deal share links |
| **Admin** | `client.admin` | Health, usage, error logs, DLQ, pipeline settings |
| **Usage** | `client.usage` | Metering, processing times |
| **Push** | `client.push` | Web push subscriptions |
| **OAuth** | `client.oauth` | Client credentials token exchange |

**Sub-resources on deals:**

```python
client.deals.comments.list(deal_id)
client.deals.assignments.create(deal_id, user_id=5)
client.deals.doc_requests.create(deal_id, ...)
client.deals.timeline.list(deal_id)
client.deals.users.search(q="jane")
```

## Retry Behavior

| Method | 429 | 5xx | Connection Error |
|--------|-----|-----|-----------------|
| GET / DELETE | Retry | Retry | Retry |
| POST / PUT / PATCH | No | No | Retry |

Backoff: exponential with jitter (0.5 s base, 30 s cap). Honors `Retry-After` header.

## Requirements

- Python 3.10+
- httpx, pydantic (installed automatically)

## License

MIT
