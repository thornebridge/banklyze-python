"""CRM resource — config, field mapping, sync, and test."""

from __future__ import annotations

from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource


class CrmResource(SyncAPIResource):

    def get_config(self, provider: str) -> dict[str, Any]:
        """Get CRM configuration for a provider."""
        return self._request("GET", f"/v1/crm/config/{provider}")

    def update_config(self, provider: str, **kwargs: Any) -> dict[str, Any]:
        """Create or update CRM configuration for a provider."""
        return self._request("PUT", f"/v1/crm/config/{provider}", json=kwargs)

    def delete_config(self, provider: str) -> dict[str, Any]:
        """Remove CRM configuration for a provider."""
        return self._request("DELETE", f"/v1/crm/config/{provider}")

    def test(self, provider: str) -> dict[str, Any]:
        """Test CRM connection for a provider."""
        return self._request("POST", f"/v1/crm/config/{provider}/test")

    def get_field_mapping(self, provider: str) -> dict[str, Any]:
        """Get field mapping for a provider."""
        return self._request("GET", f"/v1/crm/field-mapping/{provider}")

    def update_field_mapping(self, provider: str, **kwargs: Any) -> dict[str, Any]:
        """Update field mapping for a provider."""
        return self._request("PUT", f"/v1/crm/field-mapping/{provider}", json=kwargs)

    def sync(self, *, deal_id: int) -> dict[str, Any]:
        """Trigger a manual CRM sync for a deal."""
        return self._request("POST", "/v1/crm/sync", json={"deal_id": deal_id})

    def sync_log(self, *, page: int = 1, per_page: int = 25, deal_id: int | None = None) -> dict[str, Any]:
        """List CRM sync log entries."""
        return self._request("GET", "/v1/crm/sync-log", params={"page": page, "per_page": per_page, "deal_id": deal_id})


class AsyncCrmResource(AsyncAPIResource):

    async def get_config(self, provider: str) -> dict[str, Any]:
        """Get CRM configuration for a provider."""
        return await self._request("GET", f"/v1/crm/config/{provider}")

    async def update_config(self, provider: str, **kwargs: Any) -> dict[str, Any]:
        """Create or update CRM configuration for a provider."""
        return await self._request("PUT", f"/v1/crm/config/{provider}", json=kwargs)

    async def delete_config(self, provider: str) -> dict[str, Any]:
        """Remove CRM configuration for a provider."""
        return await self._request("DELETE", f"/v1/crm/config/{provider}")

    async def test(self, provider: str) -> dict[str, Any]:
        """Test CRM connection for a provider."""
        return await self._request("POST", f"/v1/crm/config/{provider}/test")

    async def get_field_mapping(self, provider: str) -> dict[str, Any]:
        """Get field mapping for a provider."""
        return await self._request("GET", f"/v1/crm/field-mapping/{provider}")

    async def update_field_mapping(self, provider: str, **kwargs: Any) -> dict[str, Any]:
        """Update field mapping for a provider."""
        return await self._request("PUT", f"/v1/crm/field-mapping/{provider}", json=kwargs)

    async def sync(self, *, deal_id: int) -> dict[str, Any]:
        """Trigger a manual CRM sync for a deal."""
        return await self._request("POST", "/v1/crm/sync", json={"deal_id": deal_id})

    async def sync_log(self, *, page: int = 1, per_page: int = 25, deal_id: int | None = None) -> dict[str, Any]:
        """List CRM sync log entries."""
        return await self._request("GET", "/v1/crm/sync-log", params={"page": page, "per_page": per_page, "deal_id": deal_id})
