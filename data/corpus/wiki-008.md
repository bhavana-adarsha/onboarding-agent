---
doc_id: wiki-008
source_type: wiki
audience: all
last_updated: 2025-12-12
---

# Common Meridian Acronyms

This page defines acronyms you'll encounter across Meridian Health Partners. When in doubt, ask in #general-slack or check Confluence.

## Claims & Operations

**EOB** - Explanation of Benefits. When a claim is processed through ClaimsFlow, the EOB is generated for the member within 24-48 hours.

**ERA** - Electronic Remittance Advice. Payers send us ERAs daily; the Claims Ops team reconciles these in ClaimsFlow by 5 PM EST.

**CCLF** - Claim-level Cost and Utilization File. We submit CCLFs to CMS quarterly for our Medicare Advantage contracts. Data & Analytics owns this in PulseBoard.

**MIPS** - Merit-based Incentive Payment System. Our providers track MIPS scores; Care Coordination uses CareBridge to monitor progress against our Q4 targets.

**NAP** - Network Adequacy Plan. Updated annually in January; Platform Engineering maintains NAP data in our provider directory system.

## Care Coordination

**PCP** - Primary Care Physician. When members enroll, CareBridge auto-assigns them to a PCP based on geography and availability.

**TCM** - Transitional Care Management. After hospital discharge, our TCM nurses use CareBridge to schedule 14-day follow-ups; 87% completion rate as of November.

**BH** - Behavioral Health. Our BH team coordinates with external partners; referrals are logged in CareBridge with a 3-day callback target.

**SDOH** - Social Determinants of Health. CareBridge now flags SDOH risk factors. In 2024, we identified 12,400 members with housing instability.

## Technology & Operations

**SLA** - Service Level Agreement. ClaimsFlow has a 99.2% uptime SLA; Platform Engineering tracks this on PulseBoard every hour.

**SFTP** - Secure File Transfer Protocol. Payers submit claim files to our SFTP server nightly; automated scripts in GitHub validate these files at 2 AM.

**ETL** - Extract, Transform, Load. Data & Analytics runs six ETL jobs daily to populate PulseBoard with fresh metrics from our database.

**MFA** - Multi-Factor Authentication. All employees must enable MFA in Workday per our 2023 security mandate.

**RTO/RPO** - Recovery Time Objective / Recovery Point Objective. Our disaster recovery plan targets RTO of 4 hours and RPO of 1 hour for all critical systems.

## HR & Scheduling

**PTO** - Paid Time Off. TimeTrax integrates with Workday; submit PTO requests at least 14 days in advance.

**FTE** - Full-Time Equivalent. Our Claims Ops team operates at 47 FTE; HR uses this metric for budget planning.

**OT** - Overtime. During March peak season, Care Coordination staff may accrue OT; TimeTrax flags this automatically for approval.

## General

**QA** - Quality Assurance. Every 50th claim processed in ClaimsFlow is pulled for QA review by a second Claims Ops analyst.

**UAT** - User Acceptance Testing. Before any ClaimsFlow release, Claims Ops runs UAT for 5 business days in our staging environment.

**ROI** - Return on Investment. CareBridge's ROI was 2.3x in 2023 based on readmission reduction alone.