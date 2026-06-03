# Requirements Gap Analysis Report

## Metadata
- Mode: large
- Generated at: 2026-06-02T10:48:34.045849+00:00
- Requirements: 5
- Solutions: 5
- Gaps: 2
- Chunks: 2
- Embedding provider: hashing
- Embedding model: BAAI/bge-m3
- Top k: 5
- Min score: 0.15

## Requirements
- **REQ-0001** The customer portal must support passwordless login for enterprise users.
- **REQ-0002** We need audit logs retained for at least seven years for regulated customers.
- **REQ-0003** The system should export monthly billing reports in CSV format.
- **REQ-0004** We require response time under two seconds for dashboard page loads.
- **REQ-0005** The roadmap needs self-service role management for account administrators.

## Solutions
- **SOL-0001** We implemented passwordless login using email magic links and FastAPI endpoints.
- **SOL-0002** Audit logging is built with Postgres tables and retention policies for seven years.
- **SOL-0003** The billing service supports CSV export for monthly invoice reports.
- **SOL-0004** Dashboard optimization is deferred until the next performance sprint.
- **SOL-0005** Role management is out of scope for this release and only read-only roles are included.

## Verified Gaps
### GAP-0001: Unaddressed (high)
- Requirement: REQ-0004 - We require response time under two seconds for dashboard page loads.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - No candidate solution was available for this requirement.

### GAP-0002: Partial (medium)
- Requirement: REQ-0005 - The roadmap needs self-service role management for account administrators.
- Recommendation: Confirm ownership and add an engineering solution that explicitly covers this requirement.
- Verified: True
- Evidence:
  - Closest solution SOL-0005 scored 0.29: Role management is out of scope for this release and only read-only roles are included.
