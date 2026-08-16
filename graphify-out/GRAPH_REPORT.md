# Graph Report - .  (2026-08-16)

## Corpus Check
- 14 files · ~8,371 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 231 nodes · 375 edges · 25 communities (17 shown, 8 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.51)
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
- System Core Purpose & Goals
- Frontend Linting Configuration
- Community 20
- Community 21
- Community 23

## God Nodes (most connected - your core abstractions)
1. `Gaurav Sharma` - 27 edges
2. `DiscoveryProfile` - 19 edges
3. `ProviderSearchResult` - 15 edges
4. `IDiscoveryProvider` - 14 edges
5. `NormalizedCompany` - 14 edges
6. `NormalizedOpportunity` - 14 edges
7. `OutreachGeneratorService` - 14 edges
8. `FreeHireAdapter` - 11 edges
9. `TheMuseAdapter` - 11 edges
10. `AdzunaAdapter` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Gaurav Sharma Resume PDF (Backend Config)` --is_identical_copy_of--> `Gaurav Sharma Resume PDF (Config)`  [INFERRED]
  backend/config/Gaurav_Sharma_resume.pdf → config/Gaurav_Sharma_resume.pdf
- `Gaurav Sharma Resume PDF (Backend Config)` --describes_person--> `Gaurav Sharma`  [EXTRACTED]
  backend/config/Gaurav_Sharma_resume.pdf → config/Gaurav_Sharma_resume.pdf
- `run_tests()` --uses--> `FreeHireAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/freehire.py
- `run_tests()` --uses--> `TheMuseAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/themuse.py
- `sync_replies()` --uses--> `ReplyTrackerService`  [INFERRED]
  backend/app/main.py → backend/app/services/reply_tracker.py

## Import Cycles
- None detected.

## Communities (25 total, 8 thin omitted)

### Community 0 - "Project Architecture & Implementation Phases"
Cohesion: 0.11
Nodes (16): ABC, _build_prompt(), DeepSeekAdapter, EmailBatchResponse, EmailDraft, GeminiAdapter, LLMProvider, OpportunityContext (+8 more)

### Community 1 - "Candidate Schemas & Validation Models"
Cohesion: 0.15
Nodes (14): DiscoveryProfile, AdzunaAdapter, AIDevJobsAdapter, IDiscoveryProvider, NormalizedCompany, NormalizedOpportunity, ProviderSearchResult, ABC (+6 more)

### Community 2 - "Backend Application & Config Services"
Cohesion: 0.11
Nodes (28): Gaurav Sharma Resume PDF (Backend Config), Gaurav Sharma Resume PDF (Config), Poddar International College — Bachelor of Computer Applications, St. Anselm's Sr. Sec. School — 12th Grade, worksforgauravsharma@gmail.com, Full-Stack Developer — Advance Control Systems, AI Agents Training Program — Coplur, Gaurav Sharma (+20 more)

### Community 3 - "AI Dev Jobs Discovery Provider"
Cohesion: 0.15
Nodes (12): get_candidate_profile(), get_candidate_profile_endpoint(), health_check(), lifespan(), sync_replies(), DiscoveryOrchestrator, run_discovery_tick(), start_scheduler() (+4 more)

### Community 4 - "Discovery Base Interfaces & Normalized Models"
Cohesion: 0.21
Nodes (7): NormalizedContact, ContactProvider, ABC, Determines if the provider is currently available (e.g., API keys are present)., Execute a search against the provider to find contacts for a company., The unique identifier for this provider., TombaAdapter

### Community 5 - "The Muse Provider & Discovery Orchestration"
Cohesion: 0.26
Nodes (13): CandidateContact, CandidateEducation, CandidateFile, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules (+5 more)

### Community 6 - "Research Service & Intelligence Layer"
Cohesion: 0.22
Nodes (3): GmailService, Sends an email via Gmail API and returns the sent message info containing id…, SendingOrchestrator

### Community 7 - "Project Memory & Root Documentation"
Cohesion: 0.22
Nodes (7): Any, MatchingService, MatchResult, BaseModel, run_verification(), CandidateFile, DiscoveryProfile

### Community 8 - "Adzuna Discovery Adapter"
Cohesion: 0.27
Nodes (4): Any, Deterministic heuristic classifier for auto vs human replies., Polls Gmail for new replies on SENT outreaches and updates Supabase., ReplyTrackerService

### Community 10 - "Signalbase Discovery Adapter"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 12 - "Playbook Execution & Knowledge Layer Rules"
Cohesion: 0.70
Nodes (5): backend .env, Query: how many .env files we have?, Three .env files configuration, frontend .env, root .env

### Community 13 - "Backend Supabase Client"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: how many .env files we have?

## Knowledge Gaps
- **23 isolated node(s):** `Answer`, `Outcome`, `Outreach-Flux Project`, `Oxlint`, `React` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_candidate_profile()` connect `AI Dev Jobs Discovery Provider` to `The Muse Provider & Discovery Orchestration`, `Project Memory & Root Documentation`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Why does `AutomationOrchestrator` connect `Project Architecture & Implementation Phases` to `AI Dev Jobs Discovery Provider`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `IDiscoveryProvider` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`IDiscoveryProvider` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Answer`, `Outcome`, `Outreach-Flux Project` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._