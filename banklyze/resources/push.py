"""Push notifications resource — VAPID key, subscribe, unsubscribe."""

from __future__ import annotations

from typing import Any

from banklyze._base_resource import AsyncAPIResource, SyncAPIResource


class PushResource(SyncAPIResource):

    def vapid_key(self) -> dict[str, Any]:
        """Get the VAPID public key for web push subscriptions."""
        return self._request("GET", "/v1/push/vapid-key")

    def subscribe(self, **kwargs: Any) -> dict[str, Any]:
        """Register or update a push subscription for the authenticated user."""
        return self._request("POST", "/v1/push/subscribe", json=kwargs)

    def unsubscribe(self, **kwargs: Any) -> dict[str, Any]:
        """Remove a push subscription for the authenticated user."""
        return self._request("DELETE", "/v1/push/subscribe", json=kwargs)


class AsyncPushResource(AsyncAPIResource):

    async def vapid_key(self) -> dict[str, Any]:
        """Get the VAPID public key for web push subscriptions."""
        return await self._request("GET", "/v1/push/vapid-key")

    async def subscribe(self, **kwargs: Any) -> dict[str, Any]:
        """Register or update a push subscription for the authenticated user."""
        return await self._request("POST", "/v1/push/subscribe", json=kwargs)

    async def unsubscribe(self, **kwargs: Any) -> dict[str, Any]:
        """Remove a push subscription for the authenticated user."""
        return await self._request("DELETE", "/v1/push/subscribe", json=kwargs)
