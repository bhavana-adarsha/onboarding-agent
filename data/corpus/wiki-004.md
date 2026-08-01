---
doc_id: wiki-004
source_type: wiki
audience: all
last_updated: 2026-04-18
---

# PulseBoard Dashboard: Reports & Ownership

## Overview

PulseBoard is our central reporting dashboard for operational metrics across Claims Ops, Care Coordination, and Finance. All teams have read access; report owners are responsible for accuracy and updates. Reports refresh daily at 2 AM EST except where noted.

## Claims Operations Reports

### Claims Processing Pipeline
**Owner:** Marcus Chen (Claims Ops Lead)  
**Last Updated:** March 2024

Tracks daily claim volume, processing time by document type, and approval rates. Displays metrics for:
- Inbound claims (EDI and paper)
- Average processing time (target: <48 hours)
- Rejection rate by denial reason
- Pending claims by insurance carrier

Used by Claims Ops for daily standup and weekly management reporting.

### Denial Analysis Dashboard
**Owner:** Sarah Okonkwo (Senior Claims Analyst)  
**Last Updated:** January 2024 ⚠️ *needs refresh*

Shows denial patterns by reason code, trending denials month-over-month, and appeals success rates. **Note:** This report may have stale data—Sarah is on extended leave. Contact Claims Ops Lead for current metrics.

### Carrier Performance Scorecard
**Owner:** Claims Ops team (rotational)  
**Last Updated:** February 2024

Monthly comparison of payment speed, error rates, and communication timeliness for our top 12 insurance carriers. Helps identify partnership issues and renegotiation opportunities.

## Care Coordination Reports

### Patient Engagement Metrics
**Owner:** Dr. Jamal Williams (Care Coordination Director)  
**Last Updated:** April 2024

Tracks care plan enrollment, patient outreach completion, and engagement scores by program:
- Chronic disease management programs (3 active)
- Post-discharge follow-up completion rates
- Patient satisfaction survey scores

Refreshes weekly on Mondays due to data processing delays in CareBridge.

### Utilization & Readmission Dashboard
**Owner:** Lisa Park (Clinical Operations Manager)  
**Last Updated:** April 2024

30-day and 60-day readmission rates by condition, ER visit trends, and average length of stay comparisons. Used for quality reporting to payers.

## Finance & Executive Reports

### Revenue Recognition Summary
**Owner:** Janet Morrison (Controller)  
**Last Updated:** March 2024

Monthly revenue by service line, contract performance against projections, and aged receivables. Restricted to Finance and Executive team.

### Headcount & Utilization
**Owner:** HR/People Ops (via Workday integration)  
**Last Updated:** Real-time

Current FTE count by department, billable vs. non-billable hours, and utilization rates. Automatically syncs with Workday daily.

## Accessing & Requesting Changes

All reports accessible via Slack integration (`/pulseBoard view`). For questions about specific metrics, contact the report owner directly or post in #data-analytics-support.

**To request new reports or modify existing ones:**
1. Submit ticket in Jira (project: `PULSE`)
2. Tag Data & Analytics team
3. Include business justification and stakeholders

## Known Issues

- Denial Analysis Dashboard has not been updated since January
- CareBridge integration sometimes delays Care Coordination data by 24 hours
- Historical data before January 2023 unavailable due to system migration