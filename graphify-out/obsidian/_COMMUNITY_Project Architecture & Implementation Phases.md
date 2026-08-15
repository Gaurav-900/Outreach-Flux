---
type: community
members: 30
---

# Project Architecture & Implementation Phases

**Members:** 30 nodes

## Members
- [[dot-__init__()]] - code - backend/app/services/matching.py
- [[dot-__init__()_1]] - code - backend/app/services/orchestrator.py
- [[dot-evaluate_opportunity()]] - code - backend/app/services/matching.py
- [[dot-process_opportunity()]] - code - backend/app/services/orchestrator.py
- [[dot-research_opportunity()]] - code - backend/app/services/research.py
- [[dot-run_discovery_for_profile()]] - code - backend/app/services/orchestrator.py
- [[Any]] - code
- [[BaseModel_2]] - code
- [[CandidateFile]] - code - backend/app/models/candidate.py
- [[DiscoveryOrchestrator]] - code - backend/app/services/orchestrator.py
- [[FastAPI]] - code
- [[MatchResult]] - code - backend/app/services/matching.py
- [[MatchingService]] - code - backend/app/services/matching.py
- [[ResearchService]] - code - backend/app/services/research.py
- [[config.py]] - code - backend/app/core/config.py
- [[get]] - code
- [[get_candidate_profile()]] - code - backend/app/core/config.py
- [[get_candidate_profile_endpoint()]] - code - backend/app/main.py
- [[health_check()]] - code - backend/app/main.py
- [[lifespan()]] - code - backend/app/main.py
- [[main.py]] - code - backend/app/main.py
- [[matching.py]] - code - backend/app/services/matching.py
- [[research.py]] - code - backend/app/services/research.py
- [[run_discovery_tick()]] - code - backend/app/services/scheduler.py
- [[run_tests()]] - code - backend/scripts/test_regression.py
- [[run_verification()]] - code - backend/scripts/verify_golden.py
- [[scheduler.py]] - code - backend/app/services/scheduler.py
- [[start_scheduler()]] - code - backend/app/services/scheduler.py
- [[test_regression.py]] - code - backend/scripts/test_regression.py
- [[verify_golden.py]] - code - backend/scripts/verify_golden.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Project_Architecture__Implementation_Phases
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Free Hire Discovery Adapter]]
- 5 edges to [[_COMMUNITY_AI Dev Jobs Discovery Provider]]
- 3 edges to [[_COMMUNITY_Research Service & Intelligence Layer]]
- 3 edges to [[_COMMUNITY_Frontend React Entrypoint & UI]]
- 2 edges to [[_COMMUNITY_Candidate Schemas & Validation Models]]
- 1 edge to [[_COMMUNITY_Signalbase Discovery Adapter]]
- 1 edge to [[_COMMUNITY_Playbook Execution & Knowledge Layer Rules]]

## Top bridge nodes
- [[DiscoveryOrchestrator]] - degree 14, connects to 6 communities
- [[MatchingService]] - degree 10, connects to 2 communities
- [[test_regression.py]] - degree 6, connects to 2 communities
- [[run_tests()]] - degree 5, connects to 2 communities
- [[get_candidate_profile()]] - degree 12, connects to 1 community