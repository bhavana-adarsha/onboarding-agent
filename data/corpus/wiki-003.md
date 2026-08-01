---
doc_id: wiki-003
source_type: wiki
audience: all
last_updated: 2025-11-05
---

# CareBridge & ClaimsFlow Integration

## What is CareBridge?

CareBridge is our care coordination platform that manages patient workflows across episodes of care. Built in 2021, it tracks everything from initial patient intake through discharge, including provider assignments, care plans, and patient touchpoints. The system currently manages ~45,000 active patient records across our network.

CareBridge is owned and maintained by the **Care Coordination team**, with Platform Engineering providing backend support.

## Key CareBridge Functions

- **Patient Intake**: Captures demographics, insurance info, and clinical flags
- **Care Plan Management**: Assigns care coordinators and tracks interventions
- **Provider Network**: Maintains our contracted provider directory (~2,800 providers)
- **Touchpoint Logging**: Records calls, visits, and patient interactions
- **Discharge Planning**: Manages transitions to post-acute care or primary care

## How CareBridge Connects to ClaimsFlow

When a patient is enrolled in CareBridge, their care journey eventually generates claims. Here's how the two systems talk:

### Data Flow (High Level)

1. **Patient Enrollment** → CareBridge creates a patient record with insurance details
2. **Care Events** → Interventions logged in CareBridge (e.g., "diabetes education session")
3. **Claim Generation** → ClaimsFlow pulls eligible events and creates claim line items
4. **Claim Status** → ClaimsFlow updates are pushed back to CareBridge for visibility

### Technical Details

CareBridge sends **daily batch files** to ClaimsFlow at 2:00 AM EST via SFTP. The file format is CSV and includes:

- Patient ID (MRN)
- Service date
- Service code (CPT/HCPCS)
- Provider NPI
- Units of service
- Authorization reference (if applicable)

**File naming convention**: `carebridge_claims_YYYYMMDD.csv`

ClaimsFlow processes these files through our standard validation rules and flags issues in the **CareBridge Claims Integration** Jira board (maintained by Claims Ops).

### Common Integration Issues

- **Missing authorization numbers**: CareBridge sometimes doesn't capture auth IDs before discharge. This causes claim rejections in ClaimsFlow.
- **Provider NPI mismatches**: Provider data drifts between systems. We reconcile quarterly.
- **Duplicate claims**: If a care event is logged twice in CareBridge, ClaimsFlow may create duplicate line items. The Claims Ops team manually deduplicates these.

## Support & Contacts

- **CareBridge questions**: Slack #carebridge-support or contact Maria Chen (Care Coordination lead)
- **Integration issues**: Jira ticket in **CareBridge Claims Integration** board
- **ClaimsFlow side**: Contact the Claims Ops team

## Related Documentation

- ClaimsFlow Overview (see wiki)
- Provider Network Maintenance Process
- Patient Intake Checklist (Confluence)
- Daily Batch File SLA (updated Feb 2024)

---

*Last updated: March 2024 by Care Coordination team*  
*Next review: September 2024*