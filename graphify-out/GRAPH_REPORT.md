# Graph Report - .  (2026-08-15)

## Corpus Check
- 2 files · ~10,023 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 147 nodes · 293 edges · 26 communities (14 shown, 12 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.51)
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
- Vite App Build Configuration
- Community 20
- Community 21
- Community 22
- Community 23

## God Nodes (most connected - your core abstractions)
1. `DiscoveryProfile` - 29 edges
2. `ProviderSearchResult` - 19 edges
3. `NormalizedCompany` - 18 edges
4. `NormalizedOpportunity` - 18 edges
5. `IDiscoveryProvider` - 18 edges
6. `DiscoveryOrchestrator` - 14 edges
7. `AI Job Outreach Phase Playbook` - 14 edges
8. `FreeHireAdapter` - 13 edges
9. `TheMuseAdapter` - 13 edges
10. `get_candidate_profile()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `AI Job Outreach Phase Playbook` --references--> `AI Job Outreach Project Memory`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 3 — Database Canonicalization + Matching + Research` --canonicalizes--> `Company Canonical Model`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 4 — Contact Discovery` --uses_fallback--> `Tomba Enrichment Fallback`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 6 — AI Outreach Batch Generation` --fallback_llm--> `DeepSeek LLM Provider Fallback`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 6 — AI Outreach Batch Generation` --calls_llm--> `Gemini LLM Provider`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md

## Import Cycles
- None detected.

## Communities (26 total, 12 thin omitted)

### Community 0 - "Project Architecture & Implementation Phases"
Cohesion: 0.19
Nodes (11): get_candidate_profile(), get_candidate_profile_endpoint(), health_check(), lifespan(), DiscoveryOrchestrator, ResearchService, run_discovery_tick(), start_scheduler() (+3 more)

### Community 1 - "Candidate Schemas & Validation Models"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 2 - "Backend Application & Config Services"
Cohesion: 0.22
Nodes (11): Phase 0 — Foundation, Phase 1 — Candidate JSON, Phase 2 — Multi-Provider Incremental Discovery, config/candidate.json, DiscoveryProvider Architecture, 3-Hour Discovery Profile Rotation, Adzuna Discovery Source, AI Dev Jobs Discovery Source (+3 more)

### Community 3 - "AI Dev Jobs Discovery Provider"
Cohesion: 0.27
Nodes (6): Any, CandidateFile, MatchingService, MatchResult, BaseModel, run_verification()

### Community 4 - "Discovery Base Interfaces & Normalized Models"
Cohesion: 0.24
Nodes (10): Phase 6 — AI Outreach Batch Generation, Phase 7 — Gmail + Sending Policy, Phase 8 — Tracking + Reply Classification, config/resume.pdf, DeepSeek LLM Provider Fallback, Gemini LLM Provider, Gmail API & Controlled Sending Policy, LLM Batch Email Generation (+2 more)

### Community 6 - "Research Service & Intelligence Layer"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 7 - "Project Memory & Root Documentation"
Cohesion: 0.43
Nodes (3): ProviderSearchResult, BaseModel, FreeHireAdapter

### Community 8 - "Adzuna Discovery Adapter"
Cohesion: 0.40
Nodes (6): Global Definition of Done, AI Job Outreach Phase Playbook, Graphify Codebase Knowledge Layer, Phase 10 — Oracle Deployment, Phase 9 — Automation, Oracle Cloud Always Free VPS Infrastructure

### Community 9 - "Free Hire Discovery Adapter"
Cohesion: 0.47
Nodes (6): Phase 3 — Database Canonicalization + Matching + Research, Candidate Profile Model, Company Canonical Model, Deterministic Candidate Matching, Opportunity Canonical Model, Supabase PostgreSQL Database

### Community 13 - "Backend Supabase Client"
Cohesion: 0.50
Nodes (3): ABC, IDiscoveryProvider, Execute a search against the provider.

### Community 14 - "Frontend Supabase Client"
Cohesion: 0.60
Nodes (5): Phase 4 — Contact Discovery, Phase 5 — Email Verification, Contact Discovery Priority Hierarchy, EVA Email Verification, Tomba Enrichment Fallback

### Community 15 - "Global Definition of Done"
Cohesion: 0.50
Nodes (4): Anti-Hallucination Rules, Canonical Pipeline Flow, AI Job Outreach Project Memory, Technology Stack Specification

## Knowledge Gaps
- **27 isolated node(s):** `supabase`, `Outreach-Flux Project`, `React`, `TypeScript`, `Vite` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DiscoveryProfile` connect `The Muse Provider & Discovery Orchestration` to `Candidate Schemas & Validation Models`, `AI Dev Jobs Discovery Provider`, `Project Memory & Root Documentation`, `Signalbase Discovery Adapter`, `Frontend React Entrypoint & UI`, `Playbook Execution & Knowledge Layer Rules`, `Backend Supabase Client`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `get_candidate_profile()` connect `Project Architecture & Implementation Phases` to `Signalbase Discovery Adapter`, `AI Dev Jobs Discovery Provider`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `AI Job Outreach Phase Playbook` connect `Adzuna Discovery Adapter` to `Backend Application & Config Services`, `Discovery Base Interfaces & Normalized Models`, `Free Hire Discovery Adapter`, `Frontend Supabase Client`, `Global Definition of Done`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `NormalizedOpportunity` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedOpportunity` has 6 INFERRED edges - model-reasoned connections that need verification._