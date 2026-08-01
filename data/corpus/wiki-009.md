---
doc_id: wiki-009
source_type: wiki
audience: all
last_updated: 2026-03-28
---

# Data & Analytics Team: Overview

## Team Composition

The Data & Analytics team sits under Platform Engineering and currently has 12 people: 2 data engineers, 4 analytics engineers, 3 business analysts, 1 analytics manager (Priya Chen), and 2 data scientists (though one is on leave through Q2). We sit on the 3rd floor near the server room.

## Primary Data Sources

**Production Databases:**
- ClaimsFlow (PostgreSQL, ~2.8TB) - updated real-time
- CareBridge (PostgreSQL, ~1.2TB) - updated real-time
- TimeTrax (MySQL, ~340GB) - batch synced nightly at 2 AM
- Workday (via API) - batch synced every 4 hours

**Data Warehouse:**
We maintain a Snowflake instance (prod-dw-01) that consolidates everything. Schema is organized by domain: `claims`, `operations`, `hr`, `scheduling`. This is the system of record for reporting.

**External Data:**
- Member eligibility feeds from insurance partners (SFTP, daily 6 AM)
- Billing data from our accounting system (Deltek, API sync every 6 hours)
- PulseBoard pulls exclusively from Snowflake

## Data Pipeline Architecture

**ETL Flow:**
All pipelines are orchestrated via Apache Airflow (running on prod-dw-01). Critical pipelines:

1. **claims_daily_load** - Runs 3 AM, 15 min SLA, pulls from ClaimsFlow, transforms, loads to `claims.processed_claims`
2. **care_coordination_hourly** - Runs every hour on the hour, syncs CareBridge member interactions
3. **hr_monthly_sync** - Runs first day of month at 1 AM, pulls Workday employee data
4. **member_eligibility_ingest** - Runs 7 AM, validates and loads SFTP feeds

Transformation code lives in GitHub (`meridian/data-pipelines`, main branch is protected). All transformations are written in dbt. Lineage documentation is in Confluence (see Data Lineage Spec v2.3).

**Data Quality:**
We run Great Expectations checks on all tables post-load. Failures trigger Slack alerts in #data-alerts. SLA breaches also post there.

## Data Request Process

**For ad-hoc requests:**

1. Submit ticket in Jira under project `ANALYTICS` with label `data-request`
2. Include: business question, required metrics, deadline, and intended use
3. Analytics team triages during Monday morning standup (10 AM)
4. Simple requests (existing reports, <4 hours work) get committed same day
5. Complex requests enter backlog; prioritized with stakeholder input

**For recurring reports:**
Submit a "Report Request" form in Confluence (linked from Data & Analytics homepage). Priya reviews monthly. Once approved, we build into PulseBoard or create scheduled queries.

**SLAs:**
- Simple ad-hoc: 2 business days
- Complex analysis: 5-10 business days (negotiable)
- Report bugs: 1 business day

**Questions?**
Slack us in #data-team or email data-analytics@meridian.local. Priya's office hours are Wednesdays 2-3 PM.