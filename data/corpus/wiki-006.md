---
doc_id: wiki-006
source_type: wiki
audience: all
last_updated: 2026-02-14
---

# Engineering Team Structure & Ownership

## Overview

Platform Engineering at Meridian Health Partners is organized into four primary teams, each responsible for specific systems and platforms. As of Q3 2024, the team consists of approximately 45 engineers across these groups.

## ClaimsFlow Team (12 engineers)

**Lead:** Marcus Chen

This team owns the end-to-end claims processing system. Responsibilities include:

- API layer for claim submission and validation
- Database schema for claims records and audit trails
- Integration with third-party insurance verification services
- Batch processing jobs that run nightly for claims reconciliation
- Performance optimization (SLA target: claims processed within 4 hours)

The team uses a microservices architecture built on Node.js and PostgreSQL. They deploy to AWS via GitHub Actions. Primary Jira board: `CLAIMS-PLATFORM`.

## CareBridge Team (11 engineers)

**Lead:** Sarah Rodriguez

CareBridge handles real-time care coordination across our network of providers and patients.

- Real-time messaging and notification system
- Care plan creation and tracking workflows
- Provider directory and network management
- Patient engagement features (mobile app APIs)
- Integration with EHR systems (currently Cerner and Epic)

Tech stack: Python backend services, React frontend, MongoDB for flexible data models. Deploys weekly on Mondays. See Confluence space: `CAREBRIDGE-ARCHITECTURE`.

## PulseBoard & Data Platform Team (14 engineers)

**Lead:** James Wu

Largest engineering team, responsible for analytics infrastructure and reporting.

- Data warehouse (Snowflake-based)
- ETL pipelines pulling from ClaimsFlow and CareBridge
- Dashboard development and visualization (Tableau, custom React dashboards)
- Data quality monitoring and alerting
- Business intelligence tools for executive reporting

This team also maintains TimeTrax data integrations. They work closely with Data & Analytics team on requirements. Jira board: `DATA-PLATFORM`.

## Infrastructure & DevOps Team (8 engineers)

**Lead:** Devon Patel

Smaller team providing platform-wide support.

- Kubernetes cluster management (3 production clusters)
- CI/CD pipeline maintenance and GitHub Actions workflows
- Security and compliance tooling
- Monitoring and observability (DataDog, PagerDuty)
- On-call rotation for production incidents

## Cross-Functional Responsibilities

- **All teams** participate in quarterly architecture reviews
- **All teams** maintain runbooks for their services in Confluence
- **All teams** follow the change management process outlined in `PLATFORM-GOVERNANCE`

## Communication & Standups

- Platform-wide standup: Mondays 10 AM (Slack Huddle)
- Team-specific standups: Daily, 9:30 AM
- Engineering leadership sync: Thursdays 2 PM (Marcus, Sarah, James, Devon, VP Eng)

## Current Gaps & Known Issues

- TimeTrax ownership is split between CareBridge (scheduling logic) and Data Platform (reporting)—this was supposed to be resolved in Q2 but got pushed
- Infrastructure team is understaffed for the scale we're operating at; we're hiring 2 more SREs

See also: `PLATFORM-ROADMAP-2024`, `ONBOARDING-GUIDE-ENGINEERING`