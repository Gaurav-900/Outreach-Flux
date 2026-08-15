# Graph Report - Outreach-flux  (2026-08-15)

## Corpus Check
- 33 files · ~7,643 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 191 nodes · 386 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 51 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5235b5e7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DiscoveryProfile
- ReplyTrackerService
- OutreachGeneratorService
- NormalizedContact
- get_candidate_profile
- AutomationOrchestrator
- candidate.py
- frontend/README.md
- App.tsx
- Query: how many .env files we have?
- Q: how many .env files we have?
- README.md

## God Nodes (most connected - your core abstractions)
1. `DiscoveryProfile` - 25 edges
2. `ProviderSearchResult` - 18 edges
3. `NormalizedCompany` - 17 edges
4. `NormalizedOpportunity` - 17 edges
5. `IDiscoveryProvider` - 17 edges
6. `get_candidate_profile()` - 15 edges
7. `FreeHireAdapter` - 12 edges
8. `TheMuseAdapter` - 12 edges
9. `NormalizedContact` - 11 edges
10. `AutomationOrchestrator` - 11 edges

## Surprising Connections (you probably didn't know these)
- `MatchingService` --uses--> `DiscoveryProfile`  [INFERRED]
  backend/app/services/matching.py → backend/app/models/candidate.py
- `run_tests()` --uses--> `FreeHireAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/freehire.py
- `run_tests()` --uses--> `TheMuseAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/themuse.py
- `AutomationOrchestrator` --uses--> `OutreachGeneratorService`  [INFERRED]
  backend/app/services/automation.py → backend/app/services/outreach_generator.py
- `AutomationOrchestrator` --uses--> `ReplyTrackerService`  [INFERRED]
  backend/app/services/automation.py → backend/app/services/reply_tracker.py

## Import Cycles
- None detected.

## Communities (14 total, 2 thin omitted)

### Community 0 - "DiscoveryProfile"
Cohesion: 0.14
Nodes (15): DiscoveryProfile, AdzunaAdapter, AIDevJobsAdapter, IDiscoveryProvider, NormalizedCompany, NormalizedOpportunity, ProviderSearchResult, ABC (+7 more)

### Community 1 - "ReplyTrackerService"
Cohesion: 0.15
Nodes (11): get_candidate_profile_endpoint(), health_check(), lifespan(), sync_replies(), Any, Deterministic heuristic classifier for auto vs human replies., Polls Gmail for new replies on SENT outreaches and updates Supabase., ReplyTrackerService (+3 more)

### Community 2 - "OutreachGeneratorService"
Cohesion: 0.16
Nodes (13): _build_prompt(), DeepSeekAdapter, EmailBatchResponse, EmailDraft, GeminiAdapter, LLMProvider, OpportunityContext, ABC (+5 more)

### Community 3 - "NormalizedContact"
Cohesion: 0.16
Nodes (8): NormalizedContact, ContactProvider, ABC, Determines if the provider is currently available (e.g., API keys are present)., Execute a search against the provider to find contacts for a company., The unique identifier for this provider., TombaAdapter, ContactService

### Community 4 - "get_candidate_profile"
Cohesion: 0.15
Nodes (11): get_candidate_profile(), CandidateFile, MatchingService, MatchResult, Any, BaseModel, ResearchService, run_discovery_tick() (+3 more)

### Community 5 - "AutomationOrchestrator"
Cohesion: 0.15
Nodes (5): AutomationOrchestrator, GmailService, Sends an email via Gmail API and returns the sent message info containing id…, DiscoveryOrchestrator, SendingOrchestrator

### Community 6 - "candidate.py"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 7 - "frontend/README.md"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 9 - "Query: how many .env files we have?"
Cohesion: 0.70
Nodes (5): backend .env, Query: how many .env files we have?, Three .env files configuration, frontend .env, root .env

### Community 10 - "Q: how many .env files we have?"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: how many .env files we have?

## Knowledge Gaps
- **10 isolated node(s):** `Answer`, `Outcome`, `Outreach-Flux Project`, `Oxlint`, `React` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_candidate_profile()` connect `get_candidate_profile` to `DiscoveryProfile`, `ReplyTrackerService`, `OutreachGeneratorService`, `AutomationOrchestrator`?**
  _High betweenness centrality (0.274) - this node is a cross-community bridge._
- **Why does `DiscoveryOrchestrator` connect `AutomationOrchestrator` to `DiscoveryProfile`, `get_candidate_profile`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `ContactService` connect `NormalizedContact` to `DiscoveryProfile`, `get_candidate_profile`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedCompany` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedCompany` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `NormalizedOpportunity` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`NormalizedOpportunity` has 5 INFERRED edges - model-reasoned connections that need verification._