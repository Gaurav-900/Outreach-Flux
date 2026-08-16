# Graph Report - Outreach-flux  (2026-08-17)

## Corpus Check
- 40 files · ~10,222 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 232 nodes · 435 edges · 17 communities (15 shown, 2 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 53 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0cf98ef`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- OutreachGeneratorService
- DiscoveryProfile
- Gaurav Sharma
- get_candidate_profile
- NormalizedContact
- candidate.py
- SendingOrchestrator
- main.py
- frontend/README.md
- App.tsx
- Query: how many .env files we have?
- Q: how many .env files we have?
- README.md
- start.sh

## God Nodes (most connected - your core abstractions)
1. `Gaurav Sharma` - 27 edges
2. `DiscoveryProfile` - 22 edges
3. `SendingOrchestrator` - 16 edges
4. `get_candidate_profile()` - 15 edges
5. `ProviderSearchResult` - 15 edges
6. `IDiscoveryProvider` - 15 edges
7. `NormalizedCompany` - 14 edges
8. `CompanyTarget` - 14 edges
9. `OutreachGeneratorService` - 14 edges
10. `FreeHireAdapter` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Gaurav Sharma Resume PDF (Backend Config)` --is_identical_copy_of--> `Gaurav Sharma Resume PDF (Config)`  [INFERRED]
  backend/config/Gaurav_Sharma_resume.pdf → config/Gaurav_Sharma_resume.pdf
- `Gaurav Sharma Resume PDF (Backend Config)` --describes_person--> `Gaurav Sharma`  [EXTRACTED]
  backend/config/Gaurav_Sharma_resume.pdf → config/Gaurav_Sharma_resume.pdf
- `trigger_sending()` --uses--> `SendingOrchestrator`  [INFERRED]
  backend/app/main.py → backend/app/services/sending_policy.py
- `MatchingService` --uses--> `DiscoveryProfile`  [INFERRED]
  backend/app/services/matching.py → backend/app/models/candidate.py
- `run_tests()` --uses--> `FreeHireAdapter`  [INFERRED]
  backend/scripts/test_regression.py → backend/app/providers/freehire.py

## Import Cycles
- None detected.

## Communities (17 total, 2 thin omitted)

### Community 0 - "OutreachGeneratorService"
Cohesion: 0.14
Nodes (14): _build_prompt(), CompanyContext, DeepSeekAdapter, EmailBatchResponse, EmailDraft, GeminiAdapter, LLMProvider, ABC (+6 more)

### Community 1 - "DiscoveryProfile"
Cohesion: 0.15
Nodes (14): DiscoveryProfile, AdzunaAdapter, AIDevJobsAdapter, CompanyTarget, IDiscoveryProvider, NormalizedCompany, ProviderSearchResult, ABC (+6 more)

### Community 2 - "Gaurav Sharma"
Cohesion: 0.11
Nodes (28): Gaurav Sharma Resume PDF (Backend Config), Gaurav Sharma Resume PDF (Config), Poddar International College — Bachelor of Computer Applications, St. Anselm's Sr. Sec. School — 12th Grade, worksforgauravsharma@gmail.com, Full-Stack Developer — Advance Control Systems, AI Agents Training Program — Coplur, Gaurav Sharma (+20 more)

### Community 3 - "get_candidate_profile"
Cohesion: 0.15
Nodes (11): get_candidate_profile(), CandidateFile, MatchingService, MatchResult, Any, BaseModel, ResearchService, run_discovery_tick() (+3 more)

### Community 4 - "NormalizedContact"
Cohesion: 0.16
Nodes (8): NormalizedContact, ContactProvider, ABC, Determines if the provider is currently available (e.g., API keys are present)., Execute a search against the provider to find contacts for a company., The unique identifier for this provider., TombaAdapter, ContactService

### Community 5 - "candidate.py"
Cohesion: 0.28
Nodes (12): CandidateContact, CandidateEducation, CandidateInfo, CandidateLocation, DiscoveryPreferences, Experience, MatchingRules, OutreachPreferences (+4 more)

### Community 6 - "SendingOrchestrator"
Cohesion: 0.12
Nodes (8): AutomationOrchestrator, GmailService, Sends an email via Gmail API and returns the sent message info containing id…, DiscoveryOrchestrator, SendingOrchestrator, main(), main(), main()

### Community 8 - "main.py"
Cohesion: 0.12
Nodes (15): get_current_user(), Dependency to validate Supabase JWT and get the authenticated user., get_candidate_profile_endpoint(), health_check(), lifespan(), sync_replies(), trigger_sending(), Any (+7 more)

### Community 10 - "frontend/README.md"
Cohesion: 0.25
Nodes (7): Oxlint, React, React Compiler, TypeScript, Vite, @vitejs/plugin-react, @vitejs/plugin-react-swc

### Community 11 - "App.tsx"
Cohesion: 0.52
Nodes (3): App(), Login(), supabase

### Community 12 - "Query: how many .env files we have?"
Cohesion: 0.70
Nodes (5): backend .env, Query: how many .env files we have?, Three .env files configuration, frontend .env, root .env

### Community 13 - "Q: how many .env files we have?"
Cohesion: 0.50
Nodes (3): Answer, Outcome, Q: how many .env files we have?

## Knowledge Gaps
- **23 isolated node(s):** `start.sh script`, `Answer`, `Outcome`, `Outreach-Flux Project`, `Oxlint` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_candidate_profile()` connect `get_candidate_profile` to `main.py`, `DiscoveryProfile`, `SendingOrchestrator`, `OutreachGeneratorService`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Why does `DiscoveryOrchestrator` connect `SendingOrchestrator` to `DiscoveryProfile`, `get_candidate_profile`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `ContactService` connect `NormalizedContact` to `DiscoveryProfile`, `get_candidate_profile`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `DiscoveryProfile` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`DiscoveryProfile` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `SendingOrchestrator` (e.g. with `trigger_sending()` and `AutomationOrchestrator`) actually correct?**
  _`SendingOrchestrator` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ProviderSearchResult` (e.g. with `AdzunaAdapter` and `AIDevJobsAdapter`) actually correct?**
  _`ProviderSearchResult` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `start.sh script`, `Answer`, `Outcome` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._