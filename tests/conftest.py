"""Shared fixtures for SDK tests."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from banklyze import BanklyzeClient


def make_response(
    status_code: int = 200,
    json_data: dict[str, Any] | None = None,
    content: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    """Build a mock httpx.Response."""
    resp_headers = {"X-Request-ID": "test-req-id", **(headers or {})}
    if json_data is not None:
        return httpx.Response(
            status_code,
            content=json.dumps(json_data).encode(),
            headers={**resp_headers, "content-type": "application/json"},
        )
    return httpx.Response(
        status_code,
        content=content or b"",
        headers=resp_headers,
    )


SAMPLE_DEAL = {
    "id": 1,
    "business_name": "Acme Trucking LLC",
    "status": "ready",
    "document_count": 3,
    "health_score": 72.5,
    "health_grade": "B",
    "avg_monthly_deposits": 85432.10,
    "avg_daily_balance": 12340.50,
    "funding_amount_requested": 75000.00,
    "screening_flags": 2,
    "created_at": "2026-01-15T10:30:00",
    "updated_at": "2026-01-16T14:22:00",
}

SAMPLE_DEAL_LIST = {
    "data": [SAMPLE_DEAL],
    "meta": {"page": 1, "per_page": 25, "total": 1, "total_pages": 1},
}

SAMPLE_DOCUMENT = {
    "id": 15,
    "filename": "chase_jan_2026.pdf",
    "document_type": "bank_statement",
    "bank_name": "Chase",
    "status": "completed",
    "health_grade": "B",
    "created_at": "2026-02-01T09:15:30",
}


@pytest.fixture
def mock_client(monkeypatch):
    """BanklyzeClient with a mock transport that returns canned responses."""
    responses: dict[str, httpx.Response] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        key = f"{request.method} {request.url.path}"
        if key in responses:
            return responses[key]
        # Default: 404
        return make_response(404, {"error": "Not found", "code": "RESOURCE_NOT_FOUND"})

    transport = httpx.MockTransport(handler)
    client = BanklyzeClient(api_key="bk_test_xxx", base_url="https://test.banklyze.com")
    # Replace the real transport with our mock
    client._http = httpx.Client(
        transport=transport,
        base_url="https://test.banklyze.com",
        headers={"X-API-Key": "bk_test_xxx"},
    )
    client._responses = responses  # type: ignore[attr-defined]
    return client
