# Requirements Gap Analysis Report

## Metadata
- Mode: large
- Generated at: 2026-06-02T11:14:45.342211+00:00
- Requirements: 55
- Solutions: 32
- Gaps: 23
- Chunks: 6
- Embedding provider: sentence_transformers
- Embedding model: BAAI/bge-m3
- Top k: 5
- Min score: 0.15

## Requirements
- **REQ-0001** The enterprise onboarding flow must support SSO login for all customer administrators.
- **REQ-0002** We need SAML authentication with metadata upload for enterprise identity providers.
- **REQ-0003** The customer portal must allow admins to invite users by email in bulk.
- **REQ-0004** We require uploaded CSV invite files to support at least five thousand rows.
- **REQ-0005** The platform must keep audit logs for administrator actions for seven years.
- **REQ-0006** Audit logs should include actor, action, timestamp, IP address, and affected resource.
- **REQ-0007** Customers need a searchable audit log screen inside the admin console.
- **REQ-0008** The billing area should export invoice summaries in CSV and PDF format.
- **REQ-0009** Monthly billing exports must include account id, invoice id, tax, credits, and total due.
- **REQ-0010** Account admins need self-service role management for standard, billing, and security roles.
- **REQ-0011** The dashboard must load within two seconds for accounts with up to ten thousand users.
- **REQ-0012** The user list should support filtering by status, role, and last login date.
- **REQ-0013** The portal must send notification emails for failed SSO setup attempts.
- **REQ-0014** The system should detect suspicious login spikes and alert security admins.
- **REQ-0015** We need daily usage metrics exported to the analytics warehouse.
- **REQ-0016** Usage metrics must include active users, API calls, storage usage, and workspace count.
- **REQ-0017** The API should expose a health endpoint for uptime monitoring.
- **REQ-0018** The health endpoint must report database, cache, and queue status.
- **REQ-0019** The application must support custom branding for enterprise customers.
- **REQ-0020** Branding should include logo upload, primary color, and email footer text.
- **REQ-0021** Data deletion requests must complete within thirty days.
- **REQ-0022** The deletion workflow should create an immutable evidence record.
- **REQ-0023** Customers require an in-app support ticket widget.
- **REQ-0024** Support tickets should attach the current page URL and account id automatically.
- **REQ-0025** The roadmap requires workspace-level feature flags.
- **REQ-0026** Feature flags should be editable by internal operators only.
- **REQ-0027** We need rate limiting for public API endpoints.
- **REQ-0028** API rate limits must be configurable per enterprise contract.
- **REQ-0029** The system should notify billing owners before payment method expiration.
- **REQ-0030** Payment expiration alerts must be sent thirty days, seven days, and one day before expiration.
- **REQ-0031** Admins need an account activity digest email every Monday.
- **REQ-0032** The digest should summarize new users, deleted users, failed logins, and billing changes.
- **REQ-0033** The system must support regional data residency for EU customers.
- **REQ-0034** EU customer data should remain in EU storage and compute regions.
- **REQ-0035** Backups must run every day and support point-in-time recovery.
- **REQ-0036** Recovery point objective should be no more than fifteen minutes.
- **REQ-0037** We require encryption at rest for all customer documents.
- **REQ-0038** Customer document encryption keys should rotate every ninety days.
- **REQ-0039** The analytics export must not include customer secrets or authentication tokens.
- **REQ-0040** Analytics records should be pseudonymized before export.
- **REQ-0041** The admin console should show clear error messages for failed CSV imports.
- **REQ-0042** CSV import errors must identify the row number and failed field.
- **REQ-0043** The portal needs a read-only auditor role.
- **REQ-0044** Auditor users should see reports and logs but cannot change settings.
- **REQ-0045** The application must support legal hold for selected customer accounts.
- **REQ-0046** Legal hold should prevent deletion until the hold is removed.
- **REQ-0047** The engineering team needs deployment status visible to internal operators.
- **REQ-0048** Deployment status should show version, environment, region, and last deploy time.
- **REQ-0049** The mobile layout must support the billing summary and usage dashboard.
- **REQ-0050** Mobile pages should preserve the same permission model as desktop.
- **REQ-0051** The customer portal must support passwordless login for enterprise users.
- **REQ-0052** We need audit logs retained for at least seven years for regulated customers.
- **REQ-0053** The system should export monthly billing reports in CSV format.
- **REQ-0054** We require response time under two seconds for dashboard page loads.
- **REQ-0055** The roadmap needs self-service role management for account administrators.

## Solutions
- **SOL-0001** We implemented SSO login for enterprise administrators using SAML and FastAPI.
- **SOL-0002** The SAML service supports metadata upload and validates identity provider certificates.
- **SOL-0003** Bulk user invites are implemented with CSV parsing and async processing.
- **SOL-0004** The invite worker currently supports ten thousand CSV rows per upload.
- **SOL-0005** Administrator audit logging is built in Postgres with seven year retention.
- **SOL-0006** The searchable audit log screen is implemented in the admin console.
- **SOL-0007** PDF invoice export is deferred until the next billing milestone.
- **SOL-0008** Role management is currently read-only and self-service editing is out of scope for this release.
- **SOL-0009** The user list supports filtering by status, role, and last login date.
- **SOL-0010** Dashboard performance work is deferred until after the analytics migration.
- **SOL-0011** Failed SSO setup emails are implemented through the notification service.
- **SOL-0012** Daily usage metrics are exported to the analytics warehouse using the batch pipeline.
- **SOL-0013** Usage export includes active users, API calls, storage usage, and workspace count.
- **SOL-0014** The API health endpoint is implemented for uptime monitoring.
- **SOL-0015** The health endpoint reports database, Redis cache, and queue status.
- **SOL-0016** Custom branding supports logo upload and primary color configuration.
- **SOL-0017** Data deletion workflow is implemented with a thirty day SLA.
- **SOL-0018** The in-app support ticket widget is implemented in the admin console.
- **SOL-0019** Workspace-level feature flags are implemented for internal operators.
- **SOL-0020** Public API rate limiting is implemented with Redis token buckets.
- **SOL-0021** Per-contract enterprise rate limit configuration is not implemented yet.
- **SOL-0022** Payment method expiration notifications are implemented for billing owners.
- **SOL-0023** Monday account activity digest emails are implemented.
- **SOL-0024** Customer documents are encrypted at rest using managed cloud keys.
- **SOL-0025** Ninety day customer document key rotation is implemented.
- **SOL-0026** Read-only auditor role is implemented for reports and logs.
- **SOL-0027** Mobile usage dashboard is deferred until the responsive layout sprint.
- **SOL-0028** We implemented passwordless login using email magic links and FastAPI endpoints.
- **SOL-0029** Audit logging is built with Postgres tables and retention policies for seven years.
- **SOL-0030** The billing service supports CSV export for monthly invoice reports.
- **SOL-0031** Dashboard optimization is deferred until the next performance sprint.
- **SOL-0032** Role management is out of scope for this release and only read-only roles are included.

## Verified Gaps
### GAP-0001: Unaddressed (high)
- Requirement: REQ-0003 - The customer portal must allow admins to invite users by email in bulk.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0025 scored 0.14: Ninety day customer document key rotation is implemented.

### GAP-0002: Unaddressed (high)
- Requirement: REQ-0006 - Audit logs should include actor, action, timestamp, IP address, and affected resource.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0006 scored 0.14: The searchable audit log screen is implemented in the admin console.

### GAP-0003: Partial (medium)
- Requirement: REQ-0010 - Account admins need self-service role management for standard, billing, and security roles.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0008 scored 0.40: Role management is currently read-only and self-service editing is out of scope for this release.

### GAP-0004: Partial (medium)
- Requirement: REQ-0011 - The dashboard must load within two seconds for accounts with up to ten thousand users.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0004 scored 0.22: The invite worker currently supports ten thousand CSV rows per upload.

### GAP-0005: Unaddressed (high)
- Requirement: REQ-0014 - The system should detect suspicious login spikes and alert security admins.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0009 scored 0.12: The user list supports filtering by status, role, and last login date.

### GAP-0006: Unaddressed (high)
- Requirement: REQ-0024 - Support tickets should attach the current page URL and account id automatically.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0023 scored 0.17: Monday account activity digest emails are implemented.

### GAP-0007: Unaddressed (high)
- Requirement: REQ-0032 - The digest should summarize new users, deleted users, failed logins, and billing changes.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0023 scored 0.17: Monday account activity digest emails are implemented.

### GAP-0008: Unaddressed (high)
- Requirement: REQ-0033 - The system must support regional data residency for EU customers.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0009: Unaddressed (high)
- Requirement: REQ-0034 - EU customer data should remain in EU storage and compute regions.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0024 scored 0.17: Customer documents are encrypted at rest using managed cloud keys.

### GAP-0010: Unaddressed (high)
- Requirement: REQ-0035 - Backups must run every day and support point-in-time recovery.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0025 scored 0.14: Ninety day customer document key rotation is implemented.

### GAP-0011: Unaddressed (high)
- Requirement: REQ-0036 - Recovery point objective should be no more than fifteen minutes.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0012: Unaddressed (high)
- Requirement: REQ-0039 - The analytics export must not include customer secrets or authentication tokens.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0024 scored 0.14: Customer documents are encrypted at rest using managed cloud keys.

### GAP-0013: Unaddressed (high)
- Requirement: REQ-0040 - Analytics records should be pseudonymized before export.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0012 scored 0.12: Daily usage metrics are exported to the analytics warehouse using the batch pipeline.

### GAP-0014: Unaddressed (high)
- Requirement: REQ-0042 - CSV import errors must identify the row number and failed field.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0004 scored 0.12: The invite worker currently supports ten thousand CSV rows per upload.

### GAP-0015: Partial (medium)
- Requirement: REQ-0043 - The portal needs a read-only auditor role.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.80: Read-only auditor role is implemented for reports and logs.

### GAP-0016: Partial (medium)
- Requirement: REQ-0044 - Auditor users should see reports and logs but cannot change settings.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.43: Read-only auditor role is implemented for reports and logs.

### GAP-0017: Unaddressed (high)
- Requirement: REQ-0045 - The application must support legal hold for selected customer accounts.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0024 scored 0.14: Customer documents are encrypted at rest using managed cloud keys.

### GAP-0018: Unaddressed (high)
- Requirement: REQ-0046 - Legal hold should prevent deletion until the hold is removed.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0017 scored 0.17: Data deletion workflow is implemented with a thirty day SLA.

### GAP-0019: Partial (medium)
- Requirement: REQ-0048 - Deployment status should show version, environment, region, and last deploy time.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0009 scored 0.22: The user list supports filtering by status, role, and last login date.

### GAP-0020: Partial (medium)
- Requirement: REQ-0049 - The mobile layout must support the billing summary and usage dashboard.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0027 scored 0.57: Mobile usage dashboard is deferred until the responsive layout sprint.

### GAP-0021: Unaddressed (high)
- Requirement: REQ-0050 - Mobile pages should preserve the same permission model as desktop.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0027 scored 0.14: Mobile usage dashboard is deferred until the responsive layout sprint.

### GAP-0022: Unaddressed (high)
- Requirement: REQ-0054 - We require response time under two seconds for dashboard page loads.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0031 scored 0.14: Dashboard optimization is deferred until the next performance sprint.

### GAP-0023: Partial (medium)
- Requirement: REQ-0055 - The roadmap needs self-service role management for account administrators.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0008 scored 0.57: Role management is currently read-only and self-service editing is out of scope for this release.
