# Graph Report - .  (2026-08-15)

## Corpus Check
- Corpus is ~9,999 words - fits in a single context window. You may not need a graph.

## Summary
- 140 nodes · 289 edges · 22 communities (13 shown, 9 thin omitted)
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

## God Nodes (most connected - your core abstractions)
1. `DiscoveryProfile` - 29 edges
2. `ProviderSearchResult` - 19 edges
3. `NormalizedCompany` - 18 edges
4. `NormalizedOpportunity` - 18 edges
5. `IDiscoveryProvider` - 18 edges
6. `DiscoveryOrchestrator` - 14 edges
7. `AI Job Outreach Assistant — Phase Playbook` - 14 edges
8. `FreeHireAdapter` - 13 edges
9. `TheMuseAdapter` - 13 edges
10. `get_candidate_profile()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `AI Job Outreach Assistant — Phase Playbook` --references--> `AI Job Outreach Assistant — Project Memory`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 2 — Multi-Provider Incremental Discovery` --implements--> `Discovery Architecture & 3-Hour Profile Rotation`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 3 — Database Canonicalization + Matching + Research` --implements--> `Database Canonicalization & Schema`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 3 — Database Canonicalization + Matching + Research` --implements--> `Deterministic Candidate Matching Engine`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 4 — Contact Discovery` --implements--> `Public Contact Discovery`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md

## Import Cycles
- None detected.

## Communities (22 total, 9 thin omitted)

### Community 0 - "Project Architecture & Implementation Phases"
Cohesion: 0.12
Nodes (17): Any, get_candidate_profile(), get_candidate_profile_endpoint(), health_check(), lifespan(), CandidateFile, MatchingService, MatchResult (+9 more)

### Community 1 - "Candidate Schemas & Validation Models"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 2 - "Backend Application & Config Services"
Cohesion: 0.31
Nodes (9): Global Definition of Done, AI Job Outreach Assistant — Phase Playbook, Graphify Memory Layer Rule, Phase 0 — Foundation, Phase 1 — Candidate JSON, Phase 2 — Multi-Provider Incremental Discovery, Phase 3 — Database Canonicalization + Matching + Research, config/candidate.json Candidate Model (+1 more)

### Community 4 - "Discovery Base Interfaces & Normalized Models"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 5 - "The Muse Provider & Discovery Orchestration"
Cohesion: 0.33
Nodes (7): Phase 10 — Oracle Deployment, Phase 7 — Gmail + Sending Policy, Phase 8 — Tracking + Reply Classification, Phase 9 — Automation, Gmail API & Google OAuth Integration, Oracle Cloud Always Free Deployment, Gmail Reply Detection & Classification

### Community 6 - "Research Service & Intelligence Layer"
Cohesion: 0.43
Nodes (3): ProviderSearchResult, BaseModel, FreeHireAdapter

### Community 7 - "Project Memory & Root Documentation"
Cohesion: 0.33
Nodes (6): Adzuna API Provider, AI Dev Jobs Provider, Discovery Architecture & 3-Hour Profile Rotation, FreeHire API Provider, Funding Signals Provider, The Muse API Provider

### Community 8 - "Adzuna Discovery Adapter"
Cohesion: 0.33
Nodes (6): Anti-Hallucination Rules, Public Contact Discovery, AI Job Outreach Assistant — Project Memory, Graphify Knowledge Memory Layer, Supabase PostgreSQL Infrastructure, Tomba Contact Adapter

### Community 12 - "Playbook Execution & Knowledge Layer Rules"
Cohesion: 0.50
Nodes (3): ABC, IDiscoveryProvider, Execute a search against the provider.

### Community 13 - "Backend Supabase Client"
Cohesion: 0.40
Nodes (5): Phase 4 — Contact Discovery, Phase 5 — Email Verification, Phase 6 — AI Outreach — Batch Generation, DeepSeek LLM Fallback Provider, Gemini Batch LLM Email Generator

### Community 14 - "Frontend Supabase Client"
Cohesion: 0.40
Nodes (5): companies & company_sources Tables, contacts Table, Database Canonicalization & Schema, EVA Email Verification Provider, opportunities & opportunity_sources Tables

## Knowledge Gaps
- **23 isolated node(s):** `supabase`, `Outreach-Flux Project`, `React`, `TypeScript`, `Vite` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DiscoveryProfile` connect `AI Dev Jobs Discovery Provider` to `Project Architecture & Implementation Phases`, `Candidate Schemas & Validation Models`, `Research Service & Intelligence Layer`, `Free Hire Discovery Adapter`, `Signalbase Discovery Adapter`, `Frontend React Entrypoint & UI`, `Playbook Execution & Knowledge Layer Rules`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `get_candidate_profile()` connect `Project Architecture & Implementation Phases` to `Free Hire Discovery Adapter`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `AI Job Outreach Assistant — Phase Playbook` connect `Backend Application & Config Services` to `Adzuna Discovery Adapter`, `Backend Supabase Client`, `The Muse Provider & Discovery Orchestration`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `NormalizedOpportunity` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedOpportunity` has 6 INFERRED edges - model-reasoned connections that need verification._