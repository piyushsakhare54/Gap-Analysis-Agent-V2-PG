# Requirements Gap Analysis Report

## Metadata
- Mode: large
- Generated at: 2026-06-02T15:00:58.127155+00:00
- Requirements: 60
- Solutions: 30
- Gaps: 30
- Chunks: 4
- Embedding provider: hashing
- Embedding model: BAAI/bge-m3
- Top k: 5
- Min score: 0.15

## Pipeline Audit
- requirements_extractor: heuristic
- solution_extractor: heuristic
- gap_analyzer: heuristic
- gap_critic: heuristic
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
- **REQ-0037** Customer document encryption keys must rotate every ninety days.
- **REQ-0038** Admins must receive a Monday account activity digest email.
- **REQ-0039** The digest must summarize new users, deleted users, failed logins, and billing changes.
- **REQ-0040** Customers need an in-app support ticket widget.
- **REQ-0041** Support tickets must attach current page URL and account id automatically.
- **REQ-0042** Workspace-level feature flags must be editable by internal operators only.
- **REQ-0043** Internal operators need deployment status visibility.
- **REQ-0044** Deployment status must show version, environment, region, and last deploy time.
- **REQ-0045** The mobile layout must support billing summary pages.
- **REQ-0046** The mobile layout must support the usage dashboard.
- **REQ-0047** Mobile pages must preserve the same permission model as desktop.
- **REQ-0048** The system must provide dark mode for the admin console.
- **REQ-0049** Admin console pages must meet WCAG 2.1 AA contrast requirements.
- **REQ-0050** All interactive controls must be keyboard accessible.
- **REQ-0051** The product must include live chat support inside the portal.
- **REQ-0052** Customers must be able to configure custom domains for the portal.
- **REQ-0053** Custom domains must support automatic TLS certificate provisioning.
- **REQ-0054** Customers must export all account data as a ZIP archive.
- **REQ-0055** The export archive must include users, roles, audit logs, invoices, and support tickets.
- **REQ-0056** Admins must configure webhook endpoints for account events.
- **REQ-0057** Webhook delivery must sign payloads with an HMAC secret.
- **REQ-0058** Failed webhook deliveries must retry with exponential backoff.
- **REQ-0059** The portal must support SCIM user provisioning.
- **REQ-0060** SCIM provisioning must support create, update, deactivate, and group assignment events.

## Solutions
- **SOL-0001** SAML SSO is implemented for administrator accounts using the authentication service.
- **SOL-0002** Certificate validation is implemented for uploaded SAML metadata.
- **SOL-0003** Bulk user invitation through CSV upload is implemented with async workers.
- **SOL-0004** The CSV invite worker supports ten thousand rows per file.
- **SOL-0005** Human readable CSV error messages are deferred to a later usability sprint.
- **SOL-0006** Searchable audit log screen is implemented in the admin console.
- **SOL-0007** Monthly billing CSV export is implemented.
- **SOL-0008** Payment method expiration alerts are implemented for thirty days, seven days, and one day before expiration.
- **SOL-0009** Self-service role management is partially implemented for standard and billing roles.
- **SOL-0010** Read-only auditor role is implemented.
- **SOL-0011** User list filtering supports status, role, and last login date.
- **SOL-0012** Dashboard performance optimization is deferred until after the analytics migration.
- **SOL-0013** Failed SSO setup notification emails are implemented.
- **SOL-0014** Suspicious login spike detection is planned but not implemented.
- **SOL-0015** Usage export includes active users, API calls, storage usage, and workspace count.
- **SOL-0016** Public API health endpoint is implemented.
- **SOL-0017** The health endpoint reports database, Redis cache, and queue status.
- **SOL-0018** Custom branding supports logo upload and primary color.
- **SOL-0019** Custom email footer text is not implemented.
- **SOL-0020** Customer documents are encrypted at rest using managed cloud keys.
- **SOL-0021** Ninety day key rotation is implemented for customer document encryption keys.
- **SOL-0022** Monday account activity digest emails are implemented.
- **SOL-0023** In-app support ticket widget is implemented.
- **SOL-0024** Mobile billing summary page is implemented.
- **SOL-0025** Mobile usage dashboard is deferred to the responsive layout sprint.
- **SOL-0026** Account ZIP export is partially implemented for users, roles, and invoices.
- **SOL-0027** Webhook endpoint configuration is implemented for account events.
- **SOL-0028** Webhook HMAC payload signing is implemented.
- **SOL-0029** Failed webhook delivery retries with exponential backoff are implemented.
- **SOL-0030** SCIM user provisioning is not implemented.

## Verified Gaps
### GAP-0001: Partial (medium)
- Requirement: REQ-0005 - CSV import errors should show row number, field name, and a human readable message.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0005 scored 0.33: Human readable CSV error messages are deferred to a later usability sprint.

### GAP-0002: Unaddressed (high)
- Requirement: REQ-0006 - Administrator audit logs must be retained for seven years.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0001 scored 0.17: SAML SSO is implemented for administrator accounts using the authentication service.

### GAP-0003: Unaddressed (high)
- Requirement: REQ-0007 - Audit logs must include actor, action, timestamp, IP address, and affected resource.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0004: Unaddressed (high)
- Requirement: REQ-0010 - Billing exports must include account id, invoice id, tax, credits, and total due.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.12: Account ZIP export is partially implemented for users, roles, and invoices.

### GAP-0005: Partial (medium)
- Requirement: REQ-0012 - Account admins must manage user roles without contacting support.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.25: Account ZIP export is partially implemented for users, roles, and invoices.

### GAP-0006: Partial (medium)
- Requirement: REQ-0013 - The portal must include a read-only auditor role.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0010 scored 0.80: Read-only auditor role is implemented.

### GAP-0007: Partial (medium)
- Requirement: REQ-0014 - Auditor users must view reports and logs but cannot change account settings.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.25: Account ZIP export is partially implemented for users, roles, and invoices.

### GAP-0008: Partial (medium)
- Requirement: REQ-0015 - Dashboard pages must load in under two seconds for accounts with up to ten thousand users.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0004 scored 0.22: The CSV invite worker supports ten thousand rows per file.

### GAP-0009: Partial (medium)
- Requirement: REQ-0018 - The system must detect suspicious login spikes and alert security admins.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0014 scored 0.25: Suspicious login spike detection is planned but not implemented.

### GAP-0010: Unaddressed (high)
- Requirement: REQ-0021 - Analytics exports must exclude customer secrets and authentication tokens.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0021 scored 0.14: Ninety day key rotation is implemented for customer document encryption keys.

### GAP-0011: Partial (medium)
- Requirement: REQ-0022 - Analytics records must be pseudonymized before export.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0007 scored 0.20: Monthly billing CSV export is implemented.

### GAP-0012: Partial (medium)
- Requirement: REQ-0028 - Customer data deletion requests must complete within thirty days.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0008 scored 0.25: Payment method expiration alerts are implemented for thirty days, seven days, and one day before expiration.

### GAP-0013: Unaddressed (high)
- Requirement: REQ-0029 - Data deletion must create an immutable evidence record.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0014: Unaddressed (high)
- Requirement: REQ-0030 - The application must support legal hold for selected customer accounts.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0001 scored 0.14: SAML SSO is implemented for administrator accounts using the authentication service.

### GAP-0015: Unaddressed (high)
- Requirement: REQ-0031 - Legal hold must prevent deletion until the hold is removed.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0012 scored 0.17: Dashboard performance optimization is deferred until after the analytics migration.

### GAP-0016: Unaddressed (high)
- Requirement: REQ-0032 - EU customers must have regional data residency.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0017: Unaddressed (high)
- Requirement: REQ-0033 - EU customer data must remain in EU storage and compute regions.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0018: Unaddressed (high)
- Requirement: REQ-0034 - Backups must run every day.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0019: Partial (medium)
- Requirement: REQ-0035 - Backups must support point-in-time recovery with fifteen minute recovery point objective.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0023 scored 0.20: In-app support ticket widget is implemented.

### GAP-0020: Unaddressed (high)
- Requirement: REQ-0039 - The digest must summarize new users, deleted users, failed logins, and billing changes.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.12: Account ZIP export is partially implemented for users, roles, and invoices.

### GAP-0021: Unaddressed (high)
- Requirement: REQ-0041 - Support tickets must attach current page URL and account id automatically.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0026 scored 0.12: Account ZIP export is partially implemented for users, roles, and invoices.

### GAP-0022: Unaddressed (high)
- Requirement: REQ-0042 - Workspace-level feature flags must be editable by internal operators only.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0023: Unaddressed (high)
- Requirement: REQ-0043 - Internal operators need deployment status visibility.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0024: Partial (medium)
- Requirement: REQ-0044 - Deployment status must show version, environment, region, and last deploy time.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0011 scored 0.22: User list filtering supports status, role, and last login date.

### GAP-0025: Partial (medium)
- Requirement: REQ-0046 - The mobile layout must support the usage dashboard.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0025 scored 0.80: Mobile usage dashboard is deferred to the responsive layout sprint.

### GAP-0026: Unaddressed (high)
- Requirement: REQ-0047 - Mobile pages must preserve the same permission model as desktop.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0025 scored 0.14: Mobile usage dashboard is deferred to the responsive layout sprint.

### GAP-0027: Unaddressed (high)
- Requirement: REQ-0050 - All interactive controls must be keyboard accessible.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0028: Unaddressed (high)
- Requirement: REQ-0051 - The product must include live chat support inside the portal.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0029: Unaddressed (high)
- Requirement: REQ-0052 - Customers must be able to configure custom domains for the portal.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0030: Unaddressed (high)
- Requirement: REQ-0053 - Custom domains must support automatic TLS certificate provisioning.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.
