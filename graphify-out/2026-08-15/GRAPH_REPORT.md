# Graph Report - .  (2026-08-15)

## Corpus Check
- 7 files · ~7,643 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 192 nodes · 372 edges · 16 communities (12 shown, 4 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 47 edges (avg confidence: 0.5)
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
- Frontend Supabase Client

## God Nodes (most connected - your core abstractions)
1. `DiscoveryProfile` - 25 edges
2. `ProviderSearchResult` - 18 edges
3. `IDiscoveryProvider` - 17 edges
4. `NormalizedCompany` - 17 edges
5. `NormalizedOpportunity` - 17 edges
6. `FreeHireAdapter` - 12 edges
7. `TheMuseAdapter` - 12 edges
8. `NormalizedContact` - 11 edges
9. `GmailService` - 11 edges
10. `ReplyTrackerService` - 11 edges

## Surprising Connections (you probably didn't know these)
- `MatchingService` --uses--> `DiscoveryProfile`  [INFERRED]
  backend/app/services/matching.py → backend/app/models/candidate.py
- `run_tests()` --uses--> `FreeHireAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/freehire.py
- `run_tests()` --uses--> `TheMuseAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/themuse.py
- `AutomationOrchestrator` --uses--> `GmailService`  [INFERRED]
  backend/app/services/automation.py → backend/app/services/gmail.py
- `AdzunaAdapter` --uses--> `DiscoveryProfile`  [INFERRED]
  backend/app/providers/adzuna.py → backend/app/models/candidate.py

## Import Cycles
- None detected.

## Communities (16 total, 4 thin omitted)

### Community 0 - "Project Architecture & Implementation Phases"
Cohesion: 0.15
Nodes (14): DiscoveryProfile, AdzunaAdapter, AIDevJobsAdapter, IDiscoveryProvider, NormalizedCompany, NormalizedOpportunity, ProviderSearchResult, ABC (+6 more)

### Community 1 - "Candidate Schemas & Validation Models"
Cohesion: 0.11
Nodes (14): Any, get_candidate_profile_endpoint(), health_check(), lifespan(), sync_replies(), AutomationOrchestrator, Deterministic heuristic classifier for auto vs human replies., Polls Gmail for new replies on SENT outreaches and updates Supabase. (+6 more)

### Community 2 - "Backend Application & Config Services"
Cohesion: 0.16
Nodes (13): _build_prompt(), DeepSeekAdapter, EmailBatchResponse, EmailDraft, GeminiAdapter, LLMProvider, OpportunityContext, ABC (+5 more)

### Community 3 - "AI Dev Jobs Discovery Provider"
Cohesion: 0.16
Nodes (8): NormalizedContact, ContactProvider, ABC, Determines if the provider is currently available (e.g., API keys are present)., Execute a search against the provider to find contacts for a company., The unique identifier for this provider., TombaAdapter, ContactService

### Community 4 - "Discovery Base Interfaces & Normalized Models"
Cohesion: 0.16
Nodes (10): get_candidate_profile(), CandidateFile, MatchingService, MatchResult, Any, BaseModel, DiscoveryOrchestrator, ResearchService (+2 more)

### Community 5 - "The Muse Provider & Discovery Orchestration"
Cohesion: 0.22
Nodes (3): GmailService, Sends an email via Gmail API and returns the sent message info containing id…, SendingOrchestrator

### Community 6 - "Research Service & Intelligence Layer"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 7 - "Project Memory & Root Documentation"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 9 - "Free Hire Discovery Adapter"
Cohesion: 0.70
Nodes (5): backend .env, Query: how many .env files we have?, Three .env files configuration, frontend .env, root .env

### Community 10 - "Signalbase Discovery Adapter"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: how many .env files we have?

## Knowledge Gaps
- **10 isolated node(s):** `Answer`, `Outcome`, `Outreach-Flux Project`, `Oxlint`, `React` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_discovery_tick()` connect `Candidate Schemas & Validation Models` to `Discovery Base Interfaces & Normalized Models`?**
  _High betweenness centrality (0.273) - this node is a cross-community bridge._
- **Why does `get_candidate_profile()` connect `Discovery Base Interfaces & Normalized Models` to `Project Architecture & Implementation Phases`, `Backend Application & Config Services`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Why does `AutomationOrchestrator` connect `Candidate Schemas & Validation Models` to `The Muse Provider & Discovery Orchestration`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `IDiscoveryProvider` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`IDiscoveryProvider` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 5 INFERRED edges - model-reasoned connections that need verification._