# Banklyze Python SDK

Official Python client for the [Banklyze API](https://banklyze.com) — AI-powered MCA underwriting platform.

## Installation

```bash
pip install banklyze
```

Requires Python 3.10+.

## Quickstart

```python
from banklyze import BanklyzeClient

client = BanklyzeClient(api_key="bk_live_...")

# Create a deal
deal = client.deals.create(business_name="Acme Trucking LLC", funding_amount_requested=75000)
print(deal.id, deal.status)

# Upload a document
doc = client.documents.upload(deal.id, "chase_jan_2026.pdf")
print(doc.status)  # "uploaded"

# List deals with typed responses
response = client.deals.list(status="ready", page=1)
for deal in response.data:
    print(deal.business_name, deal.health_grade)
print(f"Page {response.meta.page} of {response.meta.total_pages}")

# Get full deal detail
detail = client.deals.get(deal.id)
print(detail.health.health_score, detail.recommendation.decision)

# Export PDF report
pdf = client.exports.deal_pdf(deal.id)
with open("report.pdf", "wb") as f:
    f.write(pdf)

client.close()
```

## Context Manager

```python
with BanklyzeClient(api_key="bk_live_...") as client:
    deals = client.deals.list()
```

## Async Client

```python
from banklyze import AsyncBanklyzeClient

async with AsyncBanklyzeClient(api_key="bk_live_...") as client:
    deals = await client.deals.list()
    for deal in deals.data:
        print(deal.business_name)
```

## Typed Responses

Every method returns a Pydantic model with full IDE autocompletion:

```python
response = client.deals.list(status="ready")
# response is DealListResponse with .data and .meta attributes
# response.data is list[DealSummary] — each has .id, .business_name, .health_score, etc.
# response.meta is PaginationMeta with .page, .per_page, .total, .total_pages

detail = client.deals.get(42)
# detail is DealDetail with typed sub-objects:
# detail.business.industry, detail.financials.avg_monthly_deposits,
# detail.recommendation.decision, detail.health.health_grade, etc.
```

All response models accept unknown fields (`extra="allow"`), so new API fields won't break your code.

## Auto-Pagination

Iterate over all items across pages automatically:

```python
# list_all() yields raw dicts (not typed models) for streaming efficiency
for deal in client.deals.list_all(status="ready"):
    print(deal["business_name"])
```

## Resources

| Resource | Access | Description |
|----------|--------|-------------|
| Deals | `client.deals` | CRUD, decision, notes, stats, evaluate |
| Documents | `client.documents` | Upload, list, status, reprocess, classify |
| Transactions | `client.transactions` | List, correct |
| Exports | `client.exports` | CSV and PDF downloads |
| Events | `client.events` | SSE real-time streams |
| Webhooks | `client.webhooks` | Config, test, delivery logs |
| Ingest | `client.ingest` | Bulk upload with batch tracking (accepts file paths) |
| Rulesets | `client.rulesets` | Underwriting criteria CRUD |
| Comments | `client.deals.comments` | Deal comment threads |
| Assignments | `client.deals.assignments` | Deal user assignments |
| Doc Requests | `client.deals.doc_requests` | Request documents from applicants |
| Timeline | `client.deals.timeline` | Deal activity history |
| Team | `client.team` | Org member management |
| Notifications | `client.notifications` | In-app notifications |
| Keys | `client.keys` | API key management |
| Shares | `client.shares` | Public share links |
| Usage | `client.usage` | API usage metrics |
| Admin | `client.admin` | System health, usage, DLQ |
| Integrations | `client.integrations` | Slack, Teams, SMTP config |
| Onboarding | `client.onboarding` | Demo data seeding |
| CRM | `client.crm` | CRM config, sync, field mapping |
| Push | `client.push` | Push notification subscriptions |
| OAuth | `client.oauth` | Client credentials token exchange |

## Idempotency

Pass an idempotency key to prevent duplicate operations on retries:

```python
deal = client.deals.create(
    business_name="Acme Trucking LLC",
    funding_amount_requested=75000,
    idempotency_key="create-acme-001",
)
```

## Webhook Signature Verification

```python
from banklyze.webhooks import verify_signature

# In your webhook handler:
verify_signature(
    payload=request.body,
    signature=request.headers["X-Webhook-Signature"],
    secret="whsec_your_secret",
)
```

## Error Handling

```python
from banklyze import BanklyzeClient
from banklyze.exceptions import NotFoundError, RateLimitError, ValidationError

client = BanklyzeClient(api_key="bk_live_...")

try:
    deal = client.deals.get(999)
except NotFoundError:
    print("Deal not found")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Invalid request: {e.body}")
```

All exceptions include `request_id` for debugging correlation with the Banklyze team.

## Retry Behavior

The SDK automatically retries on transient failures:

- **GET/DELETE**: Retries on 429 (rate limit) and 5xx errors
- **POST/PUT/PATCH**: Only retries on connection errors (request never reached server)
- **Backoff**: Exponential with jitter (0.5s base, 30s max)
- **Rate limits**: Honors `Retry-After` header

## SSE Events

Stream real-time processing updates:

```python
for event in client.events.stream(deal_id=42):
    print(event.event, event.data)
```

## Configuration

```python
client = BanklyzeClient(
    api_key="bk_live_...",
    base_url="https://api.banklyze.com",  # default
    timeout=30.0,                          # default request timeout
    max_retries=2,                         # default retry count
)
```

## License

MIT
