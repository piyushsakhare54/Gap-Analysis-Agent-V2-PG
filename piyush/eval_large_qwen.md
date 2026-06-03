# Requirements Gap Analysis Report

## Metadata
- Mode: large
- Generated at: 2026-06-02T15:20:45.357549+00:00
- Requirements: 36
- Solutions: 26
- Gaps: 0
- Chunks: 2
- Embedding provider: sentence_transformers
- Embedding model: BAAI/bge-m3
- Top k: 3
- Min score: 0.15

## Pipeline Audit
- requirements_extractor: ollama
- solution_extractor: ollama
- gap_analyzer: ollama
- gap_critic: ollama
- retrieval: cosine

## Requirements
- **REQ-0001** The enterprise portal must support SAML SSO for all administrator accounts.
- **REQ-0002** SAML setup must allow identity provider metadata upload and certificate validation.
- **REQ-0003** Admins need bulk user invitation through CSV upload.
- **REQ-0004** CSV invitation files must support at least ten thousand rows.
- **REQ-0005** CSV import errors should show row number, field name, and a human readable message.
- **REQ-0006** Administrator audit logs must be retained for seven years.
- **REQ-0007** Audit logs must include actor, action, timestamp, IP address, and affected resource.
- **REQ-0008** Admins need a searchable audit log screen in the admin console.
- **REQ-0009** Monthly billing reports must export as CSV and PDF.
- **REQ-0010** Billing exports must include account id, invoice id, tax, credits, and total due.
- **REQ-0011** Billing owners must receive payment method expiration alerts thirty days, seven days, and one day before expiration.
- **REQ-0012** Account admins must manage user roles without contacting support.
- **REQ-0013** The portal must include a read-only auditor role.
- **REQ-0014** Auditor users must view reports and logs but cannot change account settings.
- **REQ-0015** Dashboard pages must load in under two seconds for accounts with up to ten thousand users.
- **REQ-0016** User list pages must filter by status, role, and last login date.
- **REQ-0017** The portal must send notification emails when SSO setup fails.
- **REQ-0018** The system must detect suspicious login spikes and alert security admins.
- **REQ-0019** Daily usage metrics must export to the analytics warehouse.
- **REQ-0020** Usage metrics must include active users, API calls, storage usage, and workspace count.
- **REQ-0021** Analytics exports must exclude customer secrets and authentication tokens.
- **REQ-0022** Analytics records must be pseudonymized before export.
- **REQ-0023** The public API must expose a health endpoint for uptime monitoring.
- **REQ-0024** The health endpoint must report database, cache, and queue status.
- **REQ-0025** Public API endpoints must have configurable per-contract rate limits.
- **REQ-0026** Enterprise customers must configure custom branding.
- **REQ-0027** Branding must include logo upload, primary color, and email footer text.
- **REQ-0028** Customer data deletion requests must complete within thirty days.
- **REQ-0029** Data deletion must create an immutable evidence record.
- **REQ-0030** The application must support legal hold for selected customer accounts.
- **REQ-0031** Legal hold must prevent deletion until the hold is removed.
- **REQ-0032** EU customers must have regional data residency.
- **REQ-0033** EU customer data must remain in EU storage and compute regions.
- **REQ-0034** Backups must run every day.
- **REQ-0035** Backups must support point-in-time recovery with fifteen minute recovery point objective.
- **REQ-0036** Customer documents must be encrypted at rest.

## Solutions
- **SOL-0001** SAML SSO for administrator accounts
- **SOL-0002** SAML setup flow for identity provider metadata upload
- **SOL-0003** Bulk user invitation through CSV upload
- **SOL-0004** CSV invite worker for ten thousand rows per file
- **SOL-0005** CSV import errors with row number and field name
- **SOL-0006** Human readable CSV error messages
- **SOL-0007** Administrator audit logs in Postgres
- **SOL-0008** Audit log records with actor, action, timestamp, IP address, and affected resource
- **SOL-0009** Searchable audit log screen in admin console
- **SOL-0010** Monthly billing CSV export
- **SOL-0011** Billing exports include account id, invoice id, tax, credits, and total due
- **SOL-0012** Payment method expiration alerts
- **SOL-0013** Self-service role management for standard and billing roles
- **SOL-0014** Security role editing requires support intervention
- **SOL-0015** Read-only auditor role
- **SOL-0016** Auditor permissions allow reports and logs but block settings changes
- **SOL-0017** User list filtering by status, role, and last login date
- **SOL-0018** Dashboard performance optimization
- **SOL-0019** Failed SSO setup notification emails
- **SOL-0020** Suspicious login spike detection
- **SOL-0021** Daily usage metrics export to analytics warehouse
- **SOL-0022** Usage export includes active users, API calls, storage usage, and workspace count
- **SOL-0023** Analytics export excludes customer secrets and authentication tokens
- **SOL-0024** Public API health endpoint
- **SOL-0025** Per-contract rate limit configuration
- **SOL-0026** Custom branding with logo upload and primary color

## Verified Gaps
No verified gaps found.
