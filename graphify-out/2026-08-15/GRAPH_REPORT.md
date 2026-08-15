# Graph Report - .  (2026-08-15)

## Corpus Check
- 8 files · ~10,834 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 201 nodes · 337 edges · 22 communities (11 shown, 11 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Project Architecture & Implementation Phases
- Candidate Schemas & Validation Models
- Backend Application & Config Services
- AI Dev Jobs Discovery Provider
- Discovery Base Interfaces & Normalized Models
- The Muse Provider & Discovery Orchestration
- Research Service & Intelligence Layer
- Project Memory & Root Documentation
- Adzuna Discovery Adapter
- Free Hire Discovery Adapter
- Signalbase Discovery Adapter
- Frontend React Entrypoint & UI
- Playbook Execution & Knowledge Layer Rules
- Backend Supabase Client
- Frontend Supabase Client
- Global Definition of Done
- Anti-Hallucination Rules
- System Core Purpose & Goals
- Frontend Linting Configuration
- Community 20

## God Nodes (most connected - your core abstractions)
1. `DiscoveryProfile` - 22 edges
2. `ProviderSearchResult` - 18 edges
3. `NormalizedCompany` - 17 edges
4. `NormalizedOpportunity` - 17 edges
5. `IDiscoveryProvider` - 17 edges
6. `AI Job Outreach Assistant — Phase Playbook` - 17 edges
7. `Phase 2 — Multi-Provider Incremental Discovery` - 12 edges
8. `FreeHireAdapter` - 11 edges
9. `TheMuseAdapter` - 11 edges
10. `NormalizedContact` - 11 edges

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

## Communities (22 total, 11 thin omitted)

### Community 0 - "Project Architecture & Implementation Phases"
Cohesion: 0.06
Nodes (47): 3-Hour Discovery Scheduler, Adzuna API Adapter, AI Dev Jobs API Adapter, Controlled Background Automation, config/candidate.json, Company & Opportunity Research, Contact Discovery, Database Canonicalization (+39 more)

### Community 1 - "Candidate Schemas & Validation Models"
Cohesion: 0.15
Nodes (14): DiscoveryProfile, AdzunaAdapter, AIDevJobsAdapter, IDiscoveryProvider, NormalizedCompany, NormalizedOpportunity, ProviderSearchResult, ABC (+6 more)

### Community 2 - "Backend Application & Config Services"
Cohesion: 0.12
Nodes (16): Any, get_candidate_profile(), get_candidate_profile_endpoint(), health_check(), lifespan(), CandidateFile, MatchingService, MatchResult (+8 more)

### Community 3 - "AI Dev Jobs Discovery Provider"
Cohesion: 0.16
Nodes (8): NormalizedContact, ContactProvider, ABC, Determines if the provider is currently available (e.g., API keys are present)., Execute a search against the provider to find contacts for a company., The unique identifier for this provider., TombaAdapter, ContactService

### Community 4 - "Discovery Base Interfaces & Normalized Models"
Cohesion: 0.15
Nodes (13): Deterministic Candidate Matching, config/candidate.json, Candidate Profile Model, Company Canonical Model, DiscoveryProvider Architecture, Opportunity Canonical Model, 3-Hour Discovery Profile Rotation, Adzuna Discovery Source (+5 more)

### Community 5 - "The Muse Provider & Discovery Orchestration"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 6 - "Research Service & Intelligence Layer"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 7 - "Project Memory & Root Documentation"
Cohesion: 0.29
Nodes (7): Contact Discovery Priority Hierarchy, EVA Email Verification, Gmail API & Controlled Sending Policy, LLM Batch Email Generation, LLM Usage Restriction Rationale, Reply Detection & Classification, Tomba Enrichment Fallback

### Community 8 - "Adzuna Discovery Adapter"
Cohesion: 0.50
Nodes (4): Anti-Hallucination Rules, Canonical Pipeline Flow, AI Job Outreach Project Memory, Technology Stack Specification

## Knowledge Gaps
- **55 isolated node(s):** `supabase`, `Candidate Profile Model`, `Company Canonical Model`, `Adzuna Discovery Source`, `AI Dev Jobs Discovery Source` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DiscoveryProfile` connect `Candidate Schemas & Validation Models` to `Backend Application & Config Services`, `The Muse Provider & Discovery Orchestration`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `IDiscoveryProvider` connect `Candidate Schemas & Validation Models` to `Backend Application & Config Services`, `Frontend React Entrypoint & UI`, `Playbook Execution & Knowledge Layer Rules`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `NormalizedContact` connect `AI Dev Jobs Discovery Provider` to `Candidate Schemas & Validation Models`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedOpportunity` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedOpportunity` has 5 INFERRED edges - model-reasoned connections that need verification._