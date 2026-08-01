---
doc_id: wiki-001
source_type: wiki
audience: all
last_updated: 2026-03-10
---

# ClaimsFlow System Overview

## Purpose

ClaimsFlow is Meridian Health Partners' primary claims processing platform, handling the end-to-end lifecycle of insurance claims from initial submission through payment reconciliation. The system processes approximately 12,000–15,000 claims monthly across our managed care and administrative services contracts. ClaimsFlow integrates with major payers (Aetna, Cigna, UnitedHealth) and reduces manual processing time by an estimated 40% compared to our legacy system.

**Key objectives:**
- Automate routine claim submissions and status tracking
- Reduce claim denial rates and improve first-pass accuracy
- Provide real-time visibility into claims aging and bottlenecks
- Ensure compliance with HIPAA and payer-specific requirements

## Main Modules

**Intake & Validation**
Receives claims data from provider EDI feeds and manual uploads. Performs real-time eligibility checks and fee schedule validation. Flags claims with missing or invalid data for Claims Ops review. Currently processes ~95% of claims without manual intervention.

**Submission Management**
Routes validated claims to appropriate payers using configured submission rules. Supports both 837 EDI and web portal submissions. Maintains audit trails for all submission attempts. Re-submission workflows handle initial rejections automatically when possible.

**Status Tracking & Adjudication**
Monitors claim status through payer systems via automated feeds (typically updated daily). Categorizes claims as pending, approved, denied, or requires additional information. Tracks denial reasons and remittance advice (RA) data. Integration with our accounting system pushes approved claims to revenue cycle.

**Appeals & Rework**
Enables Claims Ops to document appeal justifications and supporting documentation. Routes appealed claims back to payers with required attachments. Tracks appeal outcomes and success rates by denial category.

**Reporting & Analytics**
Provides dashboards through PulseBoard integration. Standard reports include claims volume, denial rates by payer, days-to-payment metrics, and aging bucket analysis. Data warehouse updates nightly.

## Who Uses ClaimsFlow

**Claims Operations Team** (~25 people)
Primary users. Handles claim intake, manual validation exceptions, appeals, and day-to-day operations. Uses ClaimsFlow 6–8 hours daily. Team lead is Marcus Chen (marcus.chen@meridianhealth.com).

**Care Coordination Team** (~40 people)
Views claim status for enrolled members to inform care planning and identify gaps. Read-only access to member-specific claims. Limited daily usage.

**Finance & Revenue Cycle** (~8 people)
Monitors claim aging, reconciles approved claims to payments, and handles payer disputes. Uses reporting module and weekly exports.

**Data & Analytics Team**
Maintains ClaimsFlow data warehouse, creates custom reports, and monitors system performance. Handles quarterly audits and compliance checks.

**Platform Engineering**
Manages infrastructure, integrations with payer feeds, and system upgrades. Contact: platform-eng@meridianhealth.com.

## Access & Support

Request access through Workday or contact your manager. Most issues should be logged in Jira under the "ClaimsFlow-Ops" project. For urgent production issues, ping #claimsflow-support on Slack.