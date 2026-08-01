---
doc_id: wiki-011
source_type: wiki
audience: all
last_updated: 2025-10-19
---

# On-Call Basics for Platform Engineering

## Overview

All Platform Engineering team members rotate through on-call duty. The schedule is managed in PagerDuty and syncs with our Slack channel #platform-oncall. Each rotation is one week, starting Monday at 9 AM EST.

On-call engineers are responsible for responding to production incidents across ClaimsFlow, CareBridge, PulseBoard, and TimeTrax. Response time SLA is 15 minutes for critical incidents (P1), 30 minutes for high priority (P2).

## Getting Started

**Before your rotation:**
- Review the runbook in Confluence: "Platform Engineering Runbooks" (last updated March 2023—some sections may reference old infrastructure)
- Ensure you have VPN access, AWS console access, and GitHub permissions
- Add your phone number and email to your PagerDuty profile
- Test your notification settings (phone calls, SMS, Slack)

**During your rotation:**
- Check #platform-oncall each morning for handoff notes
- Keep your laptop within reach during business hours
- For after-hours, you can be on-call from home but should be reachable

## Incident Response Flow

1. **Alert received** → PagerDuty notifies you via phone/SMS/Slack
2. **Acknowledge** → Click the acknowledge button in PagerDuty within 5 minutes
3. **Assess** → Check PulseBoard for error rates and system status. Join the incident Slack channel (auto-created as #incident-XXXX)
4. **Escalate if needed** → After 10 minutes without progress on P1s, escalate to the secondary on-call engineer (see PagerDuty rotation)
5. **Resolve** → Update #platform-oncall with resolution details and post-incident follow-up link

## Common Issues & Quick Fixes

**ClaimsFlow API timeouts:** Usually caused by database connection pool exhaustion. SSH into claims-prod-1 and check `SELECT COUNT(*) FROM pg_stat_activity;` Check Jira ticket CLAIMSFLOW-2847 for full troubleshooting steps.

**CareBridge data sync delays:** Restart the sync service via Kubernetes: `kubectl rollout restart deployment/carebridge-sync -n production`. Takes about 3 minutes.

**PulseBoard dashboard slow:** Clear Redis cache: `redis-cli -h pulseBoard-redis FLUSHDB`. Coordinate with Data & Analytics if this is recurring.

**TimeTrax scheduler not triggering:** Check GitHub Actions logs in the timetrax-scheduler repo. Often a failed dependency update. Rollback to previous commit if needed.

## Handoff & Documentation

At the end of your rotation:
- Post a summary in #platform-oncall with incident counts and any ongoing issues
- Update the runbook if you discovered new fixes
- Schedule a brief 15-minute handoff call with your replacement (use Calendly: link in Confluence)

## Escalation

- **Technical questions:** Message #platform-engineering or tag @marcus-devops
- **Customer impact:** Notify #claims-ops or #care-coordination team leads immediately
- **Multiple systems down:** Contact VP of Engineering (currently Sarah Chen) and page the secondary on-call

## Time Off & Swaps

Request time off in PagerDuty at least 2 weeks in advance. Find your own swap or contact @platform-team-leads in Slack. Do not skip your rotation without coverage.