---
doc_id: wiki-007
source_type: wiki
audience: all
last_updated: 2026-05-01
---

# Jira and Confluence Usage Guidelines

## Jira Projects and Naming

We maintain four main Jira projects across Meridian:

- **CLAIMS** – ClaimsFlow development and bug fixes (Claims Ops + Platform Engineering)
- **CARE** – CareBridge features and incidents (Care Coordination + Platform Engineering)
- **DATA** – PulseBoard analytics, reporting, and data pipelines (Data & Analytics)
- **OPS** – Infrastructure, TimeTrax maintenance, cross-team initiatives (Platform Engineering)

Project keys must be uppercase. When creating tickets, use descriptive titles (not "Bug" or "Fix thing").

## Ticket Conventions

**Assignee:** Assign to yourself only when actively working. Leave unassigned during triage.

**Priority:** Use the standard scale (Highest, High, Medium, Low). Claims Ops defaults to High for customer-facing issues. Data & Analytics uses Medium for scheduled reports.

**Labels:** Add relevant labels for routing. Common ones: `frontend`, `backend`, `database`, `urgent`, `technical-debt`, `blocked`. Add your team name if cross-team: `claims-ops`, `care-coord`.

**Story Points:** Required for sprint planning. If unsure, put 3 and let the team refine it. Do not leave blank.

**Description:** Include context, steps to reproduce (for bugs), and acceptance criteria (for features). Links to Confluence docs are helpful.

## Sprint Workflow

Sprints run two weeks, Monday to Sunday. We plan on the first Monday at 10 AM (Calendar invite sent by Platform Engineering). 

Move tickets through statuses: **Backlog** → **To Do** → **In Progress** → **In Review** → **Done**. 

Update status daily. Do not skip "In Review"—this is where code review happens. Tickets stuck in In Review for 3+ days get flagged in standup.

## Confluence Organization

Confluence is organized by team space:

- **CLAIMS** – ClaimsFlow runbooks, API docs, deployment guides
- **CARE** – CareBridge workflows, onboarding materials
- **DATA** – PulseBoard data dictionary, report definitions, SQL templates
- **OPS** – Incident response, on-call rotation, infrastructure specs

**Page titles:** Use sentence case and be specific. "ClaimsFlow Reconciliation Process" not "Process."

**Templates:** Use templates for runbooks and troubleshooting guides. Templates live in each space's "Templates" folder.

**Linking:** Cross-reference related Jira tickets in Confluence pages. Use the Jira macro: `{jira:key=CLAIMS-847}`.

**Ownership:** Every page should have an owner listed at the top (use the "Owner" label). Owners review updates quarterly.

## Etiquette

- **Slack first:** Use Slack for quick questions. Jira/Confluence are for documentation and tracking.
- **No ticket spam:** Avoid creating tickets for discussions. Use Slack threads instead.
- **Archive old pages:** If a Confluence page is outdated, add an "OUTDATED" label and link to the current version. Don't delete.
- **Comment on blockers:** If a ticket is blocked, comment with `@Platform-Engineering` and explain why. Update the ticket status to "Blocked."
- **Respect sprints:** Don't add tickets mid-sprint without discussing in Slack first.

Questions? Reach out in #platform-engineering or ask your team lead.