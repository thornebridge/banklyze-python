"""Async Banklyze API resource modules."""

from banklyze.async_resources.admin import AsyncAdminResource
from banklyze.async_resources.collaboration import (
    AsyncAssignmentsResource,
    AsyncCommentsResource,
    AsyncDocRequestsResource,
    AsyncTimelineResource,
    AsyncUserSearchResource,
)
from banklyze.async_resources.crm import AsyncCrmResource
from banklyze.async_resources.deals import AsyncDealsResource
from banklyze.resources.documents import AsyncDocumentsResource
from banklyze.async_resources.events import AsyncEventsResource
from banklyze.async_resources.exports import AsyncExportsResource
from banklyze.async_resources.ingest import AsyncIngestResource
from banklyze.async_resources.integrations import AsyncIntegrationsResource
from banklyze.async_resources.keys import AsyncKeysResource
from banklyze.async_resources.notifications import AsyncNotificationsResource
from banklyze.async_resources.oauth import AsyncOAuthResource
from banklyze.async_resources.onboarding import AsyncOnboardingResource
from banklyze.async_resources.push import AsyncPushResource
from banklyze.async_resources.rulesets import AsyncRulesetsResource
from banklyze.async_resources.share import AsyncSharesResource
from banklyze.async_resources.team import AsyncTeamResource
from banklyze.async_resources.transactions import AsyncTransactionsResource
from banklyze.async_resources.usage import AsyncUsageResource
from banklyze.async_resources.webhooks import AsyncWebhooksResource

__all__ = [
    "AsyncAdminResource",
    "AsyncAssignmentsResource",
    "AsyncCommentsResource",
    "AsyncCrmResource",
    "AsyncDealsResource",
    "AsyncDocRequestsResource",
    "AsyncDocumentsResource",
    "AsyncEventsResource",
    "AsyncExportsResource",
    "AsyncIngestResource",
    "AsyncIntegrationsResource",
    "AsyncKeysResource",
    "AsyncNotificationsResource",
    "AsyncOAuthResource",
    "AsyncOnboardingResource",
    "AsyncPushResource",
    "AsyncRulesetsResource",
    "AsyncSharesResource",
    "AsyncTeamResource",
    "AsyncTimelineResource",
    "AsyncTransactionsResource",
    "AsyncUsageResource",
    "AsyncUserSearchResource",
    "AsyncWebhooksResource",
]
