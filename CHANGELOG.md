# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-13

### Added

- **Typed responses** — all resource methods return Pydantic models with full IDE autocompletion
- **22 resource groups** covering the entire Banklyze API:
  - Core: deals, documents, transactions, exports, events, webhooks, ingest, rulesets
  - Collaboration: comments, assignments, doc requests, timeline, user search
  - Platform: team, notifications, keys, shares, usage, search
  - Admin: admin, integrations, onboarding
- **Sync + async clients** — `BanklyzeClient` and `AsyncBanklyzeClient`
- **Auto-pagination** — `list_all()` iterators on list endpoints
- **Retry with backoff** — exponential backoff with jitter, safe mutation handling
- **Webhook signature verification** — `verify_signature()` for HMAC-SHA256
- **SSE streaming** — real-time event streams for deals, org, and batches
- **Sub-resources** — `client.deals.comments.list(42)` for deal-scoped operations
- **PEP 561** — `py.typed` marker for type checker support
- **Forward compatible** — all response models use `extra="allow"`

### Changed

- Standardized all list response envelopes to `data` + `meta` (breaking change from 0.x)
- Switched build system from setuptools to hatchling
- Added pydantic as a required dependency
- Refactored sync client to use `ClientConfig` composition (eliminates duplicated retry logic)

### Removed

- Changed default `data_key` to `"data"` in pagination iterators (was entity-specific)
