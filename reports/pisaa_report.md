# Requirements Gap Analysis Report

## Metadata
- Mode: large
- Generated at: 2026-06-03T09:04:39.948025+00:00
- Requirements: 55
- Solutions: 48
- Gaps: 25
- Chunks: 6
- Embedding provider: sentence_transformers
- Embedding model: BAAI/bge-m3
- Top k: 3
- Min score: 0.15

## Warnings
- Ollama critic returned no kept gap decisions; preserving analyzer gaps instead of dropping all results.

## Pipeline Audit
- requirements_extractor: ollama
- solution_extractor: ollama
- gap_analyzer: ollama
- gap_critic: ollama
- retrieval: cosine

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
- **REQ-0052** Audit logs must be retained for at least seven years for regulated customers.
- **REQ-0053** The system should export monthly billing reports in CSV format.
- **REQ-0054** Dashboard page loads must have a response time under two seconds.
- **REQ-0055** The roadmap needs self-service role management for account administrators.

## Solutions
- **SOL-0001** SSO login for enterprise administrators
- **SOL-0002** SAML service for identity provider
- **SOL-0003** Bulk user invites with CSV parsing
- **SOL-0004** Invite worker for CSV uploads
- **SOL-0005** Administrator audit logging
- **SOL-0006** Audit event storage
- **SOL-0007** Searchable audit log screen
- **SOL-0008** Invoice summary CSV export
- **SOL-0009** Billing exports fields
- **SOL-0010** Role management
- **SOL-0011** User list filtering
- **SOL-0012** Dashboard performance work
- **SOL-0013** Failed SSO setup emails
- **SOL-0014** Suspicious login spike detection
- **SOL-0015** Daily usage metrics export
- **SOL-0016** API health endpoint
- **SOL-0017** Custom branding
- **SOL-0018** Data deletion workflow
- **SOL-0019** Deletion evidence records
- **SOL-0020** In-app support ticket widget
- **SOL-0021** Ticket creation metadata
- **SOL-0022** Workspace-level feature flags
- **SOL-0023** Feature flag permissions
- **SOL-0024** Public API rate limiting
- **SOL-0025** Per-contract enterprise rate limit
- **SOL-0026** Payment method expiration notifications
- **SOL-0027** Monday account activity digest
- **SOL-0028** Regional data residency for EU
- **SOL-0029** EU-only storage and compute isolation
- **SOL-0030** Alerts are sent thirty days, seven days, and one day before expiration
- **SOL-0031** Digest includes new users, deleted users, failed logins, and billing changes
- **SOL-0032** Daily backups are running with point-in-time recovery support
- **SOL-0033** Current recovery point objective is fifteen minutes
- **SOL-0034** Customer documents are encrypted at rest using managed cloud keys
- **SOL-0035** Ninety day customer document key rotation is implemented
- **SOL-0036** Analytics export excludes secrets and authentication tokens
- **SOL-0037** Analytics records are pseudonymized before warehouse export
- **SOL-0038** CSV import error messages identify row number and failed field
- **SOL-0039** The CSV import screen shows validation errors before submit
- **SOL-0040** Auditor permissions block changes to settings
- **SOL-0041** Deployment status is visible to internal operators
- **SOL-0042** Deployment status shows version, environment, region, and last deploy time
- **SOL-0043** Mobile billing summary is implemented
- **SOL-0044** Mobile usage dashboard is deferred until the responsive layout sprint
- **SOL-0045** Mobile routes reuse the same permission checks as desktop
- **SOL-0046** passwordless login
- **SOL-0047** billing service
- **SOL-0048** dashboard optimization

## Verified Gaps
### GAP-0001: Partial (medium)
- Requirement: REQ-0001 - The enterprise onboarding flow must support SSO login for all customer administrators.
- Recommendation: Ensure the SSO login solution explicitly supports all customer administrators as per the requirement.
- Verified: True
- Evidence:
  - Solution SOL-0001 mentions SSO login for enterprise administrators but does not explicitly support all customer administrators as required. The requirement is not fully addressed.

### GAP-0002: Partial (medium)
- Requirement: REQ-0006 - Audit logs should include actor, action, timestamp, IP address, and affected resource.
- Recommendation: Ensure audit event storage includes all required fields explicitly.
- Verified: True
- Evidence:
  - SOL-0007 and SOL-0006 do not explicitly mention including actor, action, timestamp, IP address, and affected resource. SOL-0005 mentions audit logging but lacks details on required fields.

### GAP-0003: Unaddressed (high)
- Requirement: REQ-0008 - The billing area should export invoice summaries in CSV and PDF format.
- Recommendation: Implement invoice summary CSV and PDF export by the next billing milestone.
- Verified: True
- Evidence:
  - SOL-0008 is deferred until the next billing milestone, and no other solution addresses CSV and PDF export for invoice summaries.

### GAP-0004: Partial (medium)
- Requirement: REQ-0009 - Monthly billing exports must include account id, invoice id, tax, credits, and total due.
- Recommendation: Ensure billing exports fields include all required fields explicitly.
- Verified: True
- Evidence:
  - SOL-0009 and SOL-0008 do not explicitly mention including account id, invoice id, tax, credits, and total due. SOL-0047 is unrelated to the requirement.

### GAP-0005: Partial (medium)
- Requirement: REQ-0010 - Account admins need self-service role management for standard, billing, and security roles.
- Recommendation: Clarify and expand scope limits to ensure full self-service role management for all specified roles.
- Verified: True
- Evidence:
  - SOL-0010 has scope limits on self-service editing and role management, which may not fully satisfy the requirement for self-service role management for standard, billing, and security roles.

### GAP-0006: Partial (medium)
- Requirement: REQ-0011 - The dashboard must load within two seconds for accounts with up to ten thousand users.
- Recommendation: Implement dashboard optimization to ensure the dashboard loads within two seconds for accounts with up to ten thousand users.
- Verified: True
- Evidence:
  - Dashboard optimization is deferred, and no solution explicitly addresses the two-second load time requirement for up to ten thousand users.

### GAP-0007: Partial (medium)
- Requirement: REQ-0016 - Usage metrics must include active users, API calls, storage usage, and workspace count.
- Recommendation: Implement a solution that explicitly captures active users, API calls, storage usage, and workspace count.
- Verified: True
- Evidence:
  - SOL-0015 includes metrics but does not explicitly mention active users, API calls, storage usage, and workspace count. SOL-0031 and SOL-0027 are unrelated to usage metrics.

### GAP-0008: Unaddressed (high)
- Requirement: REQ-0018 - The health endpoint must report database, cache, and queue status.
- Recommendation: Implement a solution that explicitly reports database, cache, and queue status through the health endpoint.
- Verified: True
- Evidence:
  - None of the candidate solutions explicitly report database, cache, and queue status. SOL-0016 only provides an API health endpoint without the required details.

### GAP-0009: Partial (medium)
- Requirement: REQ-0020 - Branding should include logo upload, primary color, and email footer text.
- Recommendation: Implement a solution that explicitly supports logo upload, primary color, and email footer text for branding.
- Verified: True
- Evidence:
  - SOL-0017 mentions custom branding but does not explicitly include logo upload, primary color, and email footer text. Other solutions are unrelated.

### GAP-0010: Partial (medium)
- Requirement: REQ-0021 - Data deletion requests must complete within thirty days.
- Recommendation: Implement a solution that explicitly ensures data deletion requests complete within thirty days, such as a dedicated deletion task scheduler with monitoring.
- Verified: True
- Evidence:
  - SOL-0030 mentions alerts sent thirty days before expiration, but does not explicitly ensure data deletion requests complete within thirty days. SOL-0018 and SOL-0035 are not directly related to the completion of deletion requests within thirty days.

### GAP-0011: Partial (medium)
- Requirement: REQ-0022 - The deletion workflow should create an immutable evidence record.
- Recommendation: Implement a solution that explicitly creates an immutable evidence record for deletion workflows, such as using blockchain or cryptographic hashing.
- Verified: True
- Evidence:
  - SOL-0018 and SOL-0019 are related to deletion and evidence records, but do not explicitly mention creating an immutable evidence record. SOL-0007 is about audit logs, not immutable records.

### GAP-0012: Partial (medium)
- Requirement: REQ-0024 - Support tickets should attach the current page URL and account id automatically.
- Recommendation: Implement a solution that explicitly ensures support tickets automatically attach the current page URL and account ID, such as integrating metadata collection into the widget.
- Verified: True
- Evidence:
  - SOL-0020 mentions an in-app support ticket widget, but does not explicitly state that it automatically attaches the current page URL and account ID. SOL-0021 and SOL-0046 are not directly related to this requirement.

### GAP-0013: Partial (medium)
- Requirement: REQ-0026 - Feature flags should be editable by internal operators only.
- Recommendation: Clarify and implement feature flag permissions to ensure only internal operators can edit them.
- Verified: True
- Evidence:
  - Solution SOL-0023 mentions feature flag permissions but does not explicitly state that they are editable by internal operators only. Solutions SOL-0022 and SOL-0041 are unrelated to the requirement.

### GAP-0014: Partial (medium)
- Requirement: REQ-0028 - API rate limits must be configurable per enterprise contract.
- Recommendation: Ensure API rate limits are explicitly configurable per enterprise contract.
- Verified: True
- Evidence:
  - Solution SOL-0025 mentions per-contract enterprise rate limit but does not explicitly state that API rate limits are configurable per enterprise contract. Solution SOL-0024 is for public API rate limiting and is unrelated.

### GAP-0015: Partial (medium)
- Requirement: REQ-0031 - Admins need an account activity digest email every Monday.
- Recommendation: Implement a solution that explicitly sends Monday account activity digest emails.
- Verified: True
- Evidence:
  - SOL-0027 mentions Monday account activity digest but does not explicitly confirm email delivery. SOL-0031 and SOL-0030 are unrelated to email delivery.

### GAP-0016: Partial (medium)
- Requirement: REQ-0041 - The admin console should show clear error messages for failed CSV imports.
- Recommendation: Implement a solution that explicitly shows clear error messages for failed CSV imports, including row number and field identification.
- Verified: True
- Evidence:
  - SOL-0039 shows validation errors before submit, but does not explicitly mention clear error messages for failed CSV imports. SOL-0038 addresses error messages but does not mention row number or field identification. SOL-0013 is unrelated.

### GAP-0017: Partial (medium)
- Requirement: REQ-0043 - The portal needs a read-only auditor role.
- Recommendation: Define and implement a read-only auditor role with explicit permissions.
- Verified: True
- Evidence:
  - SOL-0040 blocks changes to settings, but does not explicitly mention a read-only auditor role. SOL-0007 and SOL-0005 are related to audit logs but do not define the auditor role.

### GAP-0018: Unaddressed (high)
- Requirement: REQ-0045 - The application must support legal hold for selected customer accounts.
- Recommendation: Implement a legal hold feature that allows selected customer accounts to be placed under hold.
- Verified: True
- Evidence:
  - None of the candidate solutions address legal hold support for selected customer accounts.

### GAP-0019: Unaddressed (high)
- Requirement: REQ-0046 - Legal hold should prevent deletion until the hold is removed.
- Recommendation: Implement a legal hold feature that explicitly prevents deletion until the hold is removed.
- Verified: True
- Evidence:
  - None of the candidate solutions explicitly address the legal hold preventing deletion until the hold is removed. The solutions focus on deletion evidence records, data deletion workflow, and alerts before expiration, which are not directly related to the legal hold functionality.

### GAP-0020: Partial (medium)
- Requirement: REQ-0049 - The mobile layout must support the billing summary and usage dashboard.
- Recommendation: Ensure the mobile layout supports the billing summary and usage dashboard without deferral.
- Verified: True
- Evidence:
  - SOL-0044 and SOL-0048 are deferred until future sprints, indicating incomplete coverage for the mobile layout supporting the billing summary and usage dashboard.

### GAP-0021: Partial (medium)
- Requirement: REQ-0051 - The customer portal must support passwordless login for enterprise users.
- Recommendation: Implement passwordless login specifically for enterprise users with the required constraints.
- Verified: True
- Evidence:
  - SOL-0046 mentions passwordless login but does not specify support for enterprise users, and no other solution addresses passwordless login for enterprise users.

### GAP-0022: Unaddressed (high)
- Requirement: REQ-0052 - Audit logs must be retained for at least seven years for regulated customers.
- Recommendation: Implement a solution that ensures audit logs are retained for at least seven years for regulated customers.
- Verified: True
- Evidence:
  - None of the candidate solutions explicitly address the retention of audit logs for seven years for regulated customers.

### GAP-0023: Partial (medium)
- Requirement: REQ-0053 - The system should export monthly billing reports in CSV format.
- Recommendation: Ensure the monthly billing report export is implemented without deferral to meet the requirement.
- Verified: True
- Evidence:
  - SOL-0008 is deferred until the next billing milestone, which may affect the timely delivery of the monthly billing report export.

### GAP-0024: Partial (high)
- Requirement: REQ-0054 - Dashboard page loads must have a response time under two seconds.
- Recommendation: Prioritize and implement dashboard optimization to ensure response times meet the two-second threshold.
- Verified: True
- Evidence:
  - All solutions for dashboard performance are deferred to future sprints, which may not meet the two-second response time requirement.

### GAP-0025: Partial (medium)
- Requirement: REQ-0055 - The roadmap needs self-service role management for account administrators.
- Recommendation: Implement self-service role management without the specified scope limitations.
- Verified: True
- Evidence:
  - SOL-0010 has scope limits that restrict self-service role management, and no other solution addresses this requirement fully.
