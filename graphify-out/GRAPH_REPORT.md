# Graph Report - Outreach-flux  (2026-08-15)

## Corpus Check
- 32 files · ~11,796 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 229 nodes · 407 edges · 20 communities (13 shown, 7 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fb3bad33`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AI Job Outreach Assistant — Phase Playbook
- DiscoveryProfile
- get_candidate_profile
- NormalizedContact
- DiscoveryProvider Architecture
- candidate.py
- frontend/README.md
- LLM Batch Email Generation
- AI Job Outreach Project Memory
- OpportunityContext
- App.tsx
- Q: how many .env files we have?
- supabase.ts
- README.md
- Company Research System
- Graphify Knowledge & Memory Layer
- Opportunity Status Lifecycle
- Oracle Cloud Always Free VPS Infrastructure

## God Nodes (most connected - your core abstractions)
1. `DiscoveryProfile` - 25 edges
2. `ProviderSearchResult` - 18 edges
3. `NormalizedCompany` - 17 edges
4. `NormalizedOpportunity` - 17 edges
5. `IDiscoveryProvider` - 17 edges
6. `AI Job Outreach Assistant — Phase Playbook` - 17 edges
7. `get_candidate_profile()` - 14 edges
8. `FreeHireAdapter` - 12 edges
9. `TheMuseAdapter` - 12 edges
10. `Phase 2 — Multi-Provider Incremental Discovery` - 12 edges

## Surprising Connections (you probably didn't know these)
- `MatchingService` --uses--> `DiscoveryProfile`  [INFERRED]
  backend/app/services/matching.py → backend/app/models/candidate.py
- `run_tests()` --uses--> `FreeHireAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/freehire.py
- `run_tests()` --uses--> `TheMuseAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/themuse.py
- `Deterministic Candidate Matching` --reads_candidate_skills--> `Candidate Profile Model`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Deterministic Candidate Matching` --evaluates_opportunity--> `Opportunity Canonical Model`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md

## Import Cycles
- None detected.

## Communities (20 total, 7 thin omitted)

### Community 0 - "AI Job Outreach Assistant — Phase Playbook"
Cohesion: 0.06
Nodes (47): 3-Hour Discovery Scheduler, Adzuna API Adapter, AI Dev Jobs API Adapter, Controlled Background Automation, config/candidate.json, Company & Opportunity Research, Contact Discovery, Database Canonicalization (+39 more)

### Community 1 - "DiscoveryProfile"
Cohesion: 0.14
Nodes (15): DiscoveryProfile, AdzunaAdapter, AIDevJobsAdapter, IDiscoveryProvider, NormalizedCompany, NormalizedOpportunity, ProviderSearchResult, ABC (+7 more)

### Community 2 - "get_candidate_profile"
Cohesion: 0.11
Nodes (17): Any, get_candidate_profile(), get_candidate_profile_endpoint(), health_check(), lifespan(), CandidateFile, MatchingService, MatchResult (+9 more)

### Community 3 - "NormalizedContact"
Cohesion: 0.16
Nodes (8): NormalizedContact, ContactProvider, ABC, Determines if the provider is currently available (e.g., API keys are present)., Execute a search against the provider to find contacts for a company., The unique identifier for this provider., TombaAdapter, ContactService

### Community 4 - "DiscoveryProvider Architecture"
Cohesion: 0.15
Nodes (13): Deterministic Candidate Matching, config/candidate.json, Candidate Profile Model, Company Canonical Model, DiscoveryProvider Architecture, Opportunity Canonical Model, 3-Hour Discovery Profile Rotation, Adzuna Discovery Source (+5 more)

### Community 5 - "candidate.py"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 6 - "frontend/README.md"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 7 - "LLM Batch Email Generation"
Cohesion: 0.29
Nodes (7): Contact Discovery Priority Hierarchy, EVA Email Verification, Gmail API & Controlled Sending Policy, LLM Batch Email Generation, LLM Usage Restriction Rationale, Reply Detection & Classification, Tomba Enrichment Fallback

### Community 8 - "AI Job Outreach Project Memory"
Cohesion: 0.50
Nodes (4): Anti-Hallucination Rules, Canonical Pipeline Flow, AI Job Outreach Project Memory, Technology Stack Specification

### Community 9 - "OpportunityContext"
Cohesion: 0.16
Nodes (13): _build_prompt(), DeepSeekAdapter, EmailBatchResponse, EmailDraft, GeminiAdapter, LLMProvider, OpportunityContext, ABC (+5 more)

### Community 11 - "Q: how many .env files we have?"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: how many .env files we have?

## Knowledge Gaps
- **57 isolated node(s):** `supabase`, `Answer`, `Outcome`, `3-Hour Discovery Scheduler`, `Adzuna API Adapter` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_candidate_profile()` connect `get_candidate_profile` to `DiscoveryProfile`, `OpportunityContext`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `DiscoveryProfile` connect `DiscoveryProfile` to `get_candidate_profile`, `candidate.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `ContactService` connect `NormalizedContact` to `DiscoveryProfile`, `get_candidate_profile`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedOpportunity` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedOpportunity` has 5 INFERRED edges - model-reasoned connections that need verification._