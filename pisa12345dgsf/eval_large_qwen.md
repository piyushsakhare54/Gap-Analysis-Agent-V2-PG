# Requirements Gap Analysis Report

## Metadata
- Mode: large
- Generated at: 2026-06-02T16:43:50.956474+00:00
- Requirements: 60
- Solutions: 46
- Gaps: 34
- Chunks: 4
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
- **SOL-0011** Billing exports with account id, invoice id, tax, credits, and total due
- **SOL-0012** Payment method expiration alerts
- **SOL-0013** Self-service role management for standard and billing roles
- **SOL-0014** Security role editing requires support intervention
- **SOL-0015** Read-only auditor role
- **SOL-0016** Auditor permissions for reports and logs
- **SOL-0017** User list filtering by status, role, and last login date
- **SOL-0018** Dashboard performance optimization
- **SOL-0019** Failed SSO setup notification emails
- **SOL-0020** Suspicious login spike detection
- **SOL-0021** Daily usage metrics export to analytics warehouse
- **SOL-0022** Usage export with active users, API calls, storage usage, and workspace count
- **SOL-0023** Analytics export excludes customer secrets and authentication tokens
- **SOL-0024** Public API health endpoint
- **SOL-0025** Per-contract rate limit configuration
- **SOL-0026** Custom branding with logo upload and primary color
- **SOL-0027** Custom email footer text
- **SOL-0028** Data deletion workflow within thirty days
- **SOL-0029** Immutable deletion evidence in audit table
- **SOL-0030** Legal hold
- **SOL-0031** Daily backups are running
- **SOL-0032** Point-in-time recovery is configured with a fifteen minute recovery point objective
- **SOL-0033** Customer documents are encrypted at rest using managed cloud keys
- **SOL-0034** Ninety day key rotation is implemented for customer document encryption keys
- **SOL-0035** Monday account activity digest emails are implemented
- **SOL-0036** Digest emails summarize new users, deleted users, failed logins, and billing changes
- **SOL-0037** In-app support ticket widget is implemented
- **SOL-0038** Ticket creation attaches current page URL and account id
- **SOL-0039** Workspace-level feature flags are editable only by internal operators
- **SOL-0040** Deployment status is visible to internal operators
- **SOL-0041** Deployment status shows version, environment, region, and last deploy time
- **SOL-0042** Mobile billing summary page is implemented
- **SOL-0043** Mobile routes reuse the same permission checks as desktop
- **SOL-0044** Webhook endpoint configuration is implemented for account events
- **SOL-0045** Webhook HMAC payload signing is implemented
- **SOL-0046** Failed webhook delivery retries with exponential backoff are implemented

## Verified Gaps
### GAP-0001: Partial (medium)
- Requirement: REQ-0001 - The enterprise portal must support SAML SSO for all administrator accounts.
- Recommendation: Verify that the authentication service explicitly supports SAML SSO for all administrator accounts.
- Verified: True
- Evidence:
  - SOL-0001 mentions SAML SSO for administrator accounts but does not explicitly confirm support for all administrator accounts.

### GAP-0002: Partial (medium)
- Requirement: REQ-0002 - SAML setup must allow identity provider metadata upload and certificate validation.
- Recommendation: Ensure certificate validation is explicitly included in the SAML setup flow.
- Verified: True
- Evidence:
  - SOL-0002 covers metadata upload but does not explicitly mention certificate validation.

### GAP-0003: Partial (medium)
- Requirement: REQ-0003 - Admins need bulk user invitation through CSV upload.
- Recommendation: Ensure that the CSV upload functionality is fully implemented without deferral.
- Verified: True
- Evidence:
  - SOL-0003 covers bulk user invitation through CSV upload, but SOL-0006 is deferred to a later sprint.

### GAP-0004: Partial (medium)
- Requirement: REQ-0005 - CSV import errors should show row number, field name, and a human readable message.
- Recommendation: Ensure that the CSV import errors include both row number, field name, and human-readable messages.
- Verified: True
- Evidence:
  - SOL-0005 covers row number and field name but does not explicitly mention human-readable messages.

### GAP-0005: Partial (medium)
- Requirement: REQ-0006 - Administrator audit logs must be retained for seven years.
- Recommendation: Implement a retention policy in Postgres or use a separate archival solution to ensure logs are retained for seven years.
- Verified: True
- Evidence:
  - Solution SOL-0007 stores audit logs in Postgres but does not specify retention period or mechanism for seven-year retention.

### GAP-0006: Partial (medium)
- Requirement: REQ-0009 - Monthly billing reports must export as CSV and PDF.
- Recommendation: Add PDF export capability to the monthly billing reports to fully satisfy the requirement.
- Verified: True
- Evidence:
  - Solution SOL-0010 provides CSV export but does not mention PDF export, which is required by the requirement.

### GAP-0007: Partial (medium)
- Requirement: REQ-0011 - Billing owners must receive payment method expiration alerts thirty days, seven days, and one day before expiration.
- Recommendation: Define the exact timing for alerts in the solution.
- Verified: True
- Evidence:
  - Solution SOL-0012 mentions payment method expiration alerts but does not specify the exact timing (thirty days, seven days, and one day before expiration).

### GAP-0008: Unaddressed (high)
- Requirement: REQ-0012 - Account admins must manage user roles without contacting support.
- Recommendation: Implement self-service role management for user roles.
- Verified: True
- Evidence:
  - None of the candidate solutions explicitly allow account admins to manage user roles without contacting support.

### GAP-0009: Partial (high)
- Requirement: REQ-0015 - Dashboard pages must load in under two seconds for accounts with up to ten thousand users.
- Recommendation: Ensure dashboard performance optimization is implemented before analytics migration.
- Verified: True
- Evidence:
  - Solution SOL-0018 is deferred until after analytics migration, which may impact the requirement for dashboard pages to load under two seconds.

### GAP-0010: Partial (medium)
- Requirement: REQ-0016 - User list pages must filter by status, role, and last login date.
- Recommendation: Implement SOL-0017 without deferral to fully satisfy REQ-0016.
- Verified: True
- Evidence:
  - SOL-0017 covers filtering by status, role, and last login date but is deferred, which indicates incomplete coverage.

### GAP-0011: Unaddressed (high)
- Requirement: REQ-0018 - The system must detect suspicious login spikes and alert security admins.
- Recommendation: Implement SOL-0020 to detect suspicious login spikes and alert security admins.
- Verified: True
- Evidence:
  - SOL-0020 is marked as 'not implemented', indicating no solution covers the requirement.

### GAP-0012: Partial (medium)
- Requirement: REQ-0019 - Daily usage metrics must export to the analytics warehouse.
- Recommendation: Implement SOL-0018 without deferral to fully satisfy REQ-0019.
- Verified: True
- Evidence:
  - SOL-0021 and SOL-0022 cover the export of daily usage metrics but SOL-0018 is deferred, indicating incomplete coverage.

### GAP-0013: Partial (medium)
- Requirement: REQ-0022 - Analytics records must be pseudonymized before export.
- Recommendation: Implement pseudonymization logic in analytics exports.
- Verified: True
- Evidence:
  - SOL-0023 only excludes secrets and tokens, not pseudonymizing records.

### GAP-0014: Unaddressed (high)
- Requirement: REQ-0024 - The health endpoint must report database, cache, and queue status.
- Recommendation: Implement health endpoint to report database, cache, and queue status.
- Verified: True
- Evidence:
  - No candidate solution explicitly reports database, cache, and queue status.

### GAP-0015: Partial (high)
- Requirement: REQ-0025 - Public API endpoints must have configurable per-contract rate limits.
- Recommendation: Implement configurable per-contract rate limits for public API endpoints.
- Verified: True
- Evidence:
  - SOL-0025 is deferred with 'not available yet' scope limit.

### GAP-0016: Partial (medium)
- Requirement: REQ-0026 - Enterprise customers must configure custom branding.
- Recommendation: Implement the custom email footer text as part of the branding configuration.
- Verified: True
- Evidence:
  - Solution SOL-0027 has scope_limits: ["not implemented"]

### GAP-0017: Unaddressed (high)
- Requirement: REQ-0027 - Branding must include logo upload, primary color, and email footer text.
- Recommendation: Implement the custom email footer text to fully satisfy the branding requirement.
- Verified: True
- Evidence:
  - Solution SOL-0027 has scope_limits: ["not implemented"]

### GAP-0018: Unaddressed (high)
- Requirement: REQ-0030 - The application must support legal hold for selected customer accounts.
- Recommendation: Implement the legal hold feature to support the requirement.
- Verified: True
- Evidence:
  - Solution SOL-0030 has scope_limits: ["not implemented"]

### GAP-0019: Unaddressed (high)
- Requirement: REQ-0031 - Legal hold must prevent deletion until the hold is removed.
- Recommendation: Implement a legal hold feature that prevents deletion until the hold is removed.
- Verified: True
- Evidence:
  - Solution SOL-0030 is marked as 'not implemented' in scope_limits, and other solutions do not address legal hold preventing deletion.

### GAP-0020: Unaddressed (high)
- Requirement: REQ-0032 - EU customers must have regional data residency.
- Recommendation: Implement regional data residency for EU customers in designated storage and compute regions.
- Verified: True
- Evidence:
  - None of the candidate solutions address regional data residency for EU customers.

### GAP-0021: Unaddressed (high)
- Requirement: REQ-0033 - EU customer data must remain in EU storage and compute regions.
- Recommendation: Implement data residency controls to ensure EU customer data is stored and processed only in EU regions.
- Verified: True
- Evidence:
  - None of the candidate solutions ensure EU customer data remains in EU storage and compute regions.

### GAP-0022: Partial (medium)
- Requirement: REQ-0036 - Customer documents must be encrypted at rest.
- Recommendation: Ensure encryption at rest meets industry standards and includes key rotation as per REQ-0037.
- Verified: True
- Evidence:
  - Solution SOL-0033 addresses encryption at rest but does not mention key rotation or compliance with specific encryption standards.

### GAP-0023: Partial (medium)
- Requirement: REQ-0046 - The mobile layout must support the usage dashboard.
- Recommendation: Implement a dedicated mobile layout for the usage dashboard.
- Verified: True
- Evidence:
  - SOL-0042 refers to a billing summary page, not the usage dashboard. SOL-0018 is deferred and relates to performance optimization, not dashboard support. SOL-0037 is unrelated to dashboard functionality.

### GAP-0024: Unaddressed (high)
- Requirement: REQ-0048 - The system must provide dark mode for the admin console.
- Recommendation: Implement dark mode for the admin console.
- Verified: True
- Evidence:
  - No candidate solution addresses dark mode for the admin console. All solutions are unrelated or not implemented.

### GAP-0025: Unaddressed (high)
- Requirement: REQ-0049 - Admin console pages must meet WCAG 2.1 AA contrast requirements.
- Recommendation: Ensure all admin console pages meet WCAG 2.1 AA contrast requirements.
- Verified: True
- Evidence:
  - No candidate solution addresses WCAG 2.1 AA contrast requirements for admin console pages. All solutions are unrelated or not implemented.

### GAP-0026: Unaddressed (high)
- Requirement: REQ-0050 - All interactive controls must be keyboard accessible.
- Recommendation: Ensure all interactive controls are keyboard accessible.
- Verified: True
- Evidence:
  - No candidate solution addresses keyboard accessibility for interactive controls. All solutions are unrelated or not implemented.

### GAP-0027: Partial (medium)
- Requirement: REQ-0051 - The product must include live chat support inside the portal.
- Recommendation: Implement a live chat widget within the portal as per the requirement.
- Verified: True
- Evidence:
  - The solution 'In-app support ticket widget is implemented' does not explicitly mention live chat support, only support ticket creation. The requirement is for live chat, not ticket creation.

### GAP-0028: Unaddressed (high)
- Requirement: REQ-0052 - Customers must be able to configure custom domains for the portal.
- Recommendation: Implement a feature for customers to configure custom domains for the portal.
- Verified: True
- Evidence:
  - None of the candidate solutions address the requirement for configuring custom domains. The closest solution is for custom branding, which is not equivalent to custom domain configuration.

### GAP-0029: Unaddressed (high)
- Requirement: REQ-0053 - Custom domains must support automatic TLS certificate provisioning.
- Recommendation: Implement automatic TLS certificate provisioning for custom domains.
- Verified: True
- Evidence:
  - None of the candidate solutions address the requirement for automatic TLS certificate provisioning for custom domains. The closest solution is for SAML setup, which is unrelated.

### GAP-0030: Unaddressed (high)
- Requirement: REQ-0054 - Customers must export all account data as a ZIP archive.
- Recommendation: Implement a ZIP archive export feature that includes all account data.
- Verified: True
- Evidence:
  - None of the candidate solutions address the requirement for exporting all account data as a ZIP archive. The closest solutions are for billing and analytics exports, which are not comprehensive.

### GAP-0031: Unaddressed (high)
- Requirement: REQ-0055 - The export archive must include users, roles, audit logs, invoices, and support tickets.
- Recommendation: Implement an export archive that includes all required data elements as specified in the requirement.
- Verified: True
- Evidence:
  - None of the candidate solutions address the requirement for including users, roles, audit logs, invoices, and support tickets in the export archive. The closest solutions are for billing and usage exports, which are not comprehensive.

### GAP-0032: Partial (medium)
- Requirement: REQ-0056 - Admins must configure webhook endpoints for account events.
- Recommendation: Ensure that the solution explicitly allows admins to configure webhook endpoints for account events.
- Verified: True
- Evidence:
  - SOL-0044 covers webhook endpoint configuration for account events but does not explicitly mention admin configuration. Other solutions are unrelated.

### GAP-0033: Unaddressed (high)
- Requirement: REQ-0059 - The portal must support SCIM user provisioning.
- Recommendation: Implement SCIM user provisioning in the portal.
- Verified: True
- Evidence:
  - No candidate solution explicitly supports SCIM user provisioning.

### GAP-0034: Unaddressed (high)
- Requirement: REQ-0060 - SCIM provisioning must support create, update, deactivate, and group assignment events.
- Recommendation: Implement SCIM provisioning for the specified events.
- Verified: True
- Evidence:
  - No candidate solution explicitly supports SCIM provisioning for create, update, deactivate, and group assignment events.
