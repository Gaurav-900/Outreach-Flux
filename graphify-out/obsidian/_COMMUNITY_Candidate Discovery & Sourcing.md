---
type: community
members: 5
---

# Candidate Discovery & Sourcing

**Members:** 5 nodes

## Members
- [[Candidate JSON Config]] - document - AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- [[Discovery Profile Rotation]] - concept - AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- [[Discovery Providers (FreeHire, Adzuna, The Muse, AI Dev Jobs, Funding Signals)]] - concept - AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- [[Phase 1 - Candidate JSON]] - rationale - AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md
- [[Phase 2 - Multi-Provider Incremental Discovery]] - rationale - AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Candidate_Discovery__Sourcing
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Database Canonicalization & Matching]]

## Top bridge nodes
- [[Discovery Providers (FreeHire, Adzuna, The Muse, AI Dev Jobs, Funding Signals)]] - degree 2, connects to 1 community