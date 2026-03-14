"""Base classes for sync and async API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from banklyze.async_client import AsyncBanklyzeClient
    from banklyze.client import BanklyzeClient


class SyncAPIResource:
    """Base class for synchronous resource implementations."""

    _client: BanklyzeClient

    def __init__(self, client: BanklyzeClient) -> None:
        self._client = client

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        return self._client._request(method, path, **kwargs)


class AsyncAPIResource:
    """Base class for asynchronous resource implementations."""

    _client: AsyncBanklyzeClient

    def __init__(self, client: AsyncBanklyzeClient) -> None:
        self._client = client

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        return await self._client._request(method, path, **kwargs)
