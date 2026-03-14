"""Tests for the deals resource with typed responses."""

from __future__ import annotations


from banklyze.types import DealListResponse, DealSummary, DealStats
from tests.conftest import SAMPLE_DEAL, SAMPLE_DEAL_LIST, make_response


def test_list_deals(mock_client):
    mock_client._responses["GET /v1/deals"] = make_response(200, SAMPLE_DEAL_LIST)

    result = mock_client.deals.list()

    assert isinstance(result, DealListResponse)
    assert len(result.data) == 1
    assert isinstance(result.data[0], DealSummary)
    assert result.data[0].business_name == "Acme Trucking LLC"
    assert result.data[0].health_score == 72.5
    assert result.meta.page == 1
    assert result.meta.total == 1


def test_create_deal(mock_client):
    mock_client._responses["POST /v1/deals"] = make_response(201, SAMPLE_DEAL)

    result = mock_client.deals.create(
        business_name="Acme Trucking LLC",
        funding_amount_requested=75000,
    )

    assert isinstance(result, DealSummary)
    assert result.id == 1
    assert result.business_name == "Acme Trucking LLC"


def test_get_deal_stats(mock_client):
    stats_data = {
        "total": 42,
        "by_status": {"ready": 10, "approved": 20},
        "total_volume": 1250000.00,
        "avg_health": 68.5,
    }
    mock_client._responses["GET /v1/deals/stats"] = make_response(200, stats_data)

    result = mock_client.deals.stats()

    assert isinstance(result, DealStats)
    assert result.total == 42
    assert result.by_status["ready"] == 10


def test_deal_forward_compatibility(mock_client):
    """Unknown fields from API are preserved (extra='allow')."""
    deal_with_new_field = {**SAMPLE_DEAL, "new_field": "new_value"}
    mock_client._responses["POST /v1/deals"] = make_response(201, deal_with_new_field)

    result = mock_client.deals.create(business_name="Test", funding_amount_requested=50000)

    assert result.new_field == "new_value"  # type: ignore[attr-defined]
