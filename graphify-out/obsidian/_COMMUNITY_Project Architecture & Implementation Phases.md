---
type: community
members: 19
---

# Project Architecture & Implementation Phases

**Members:** 19 nodes

## Members
- [[dot-__init__()_1]] - code - backend/app/services/orchestrator.py
- [[dot-process_opportunity()]] - code - backend/app/services/orchestrator.py
- [[dot-research_opportunity()]] - code - backend/app/services/research.py
- [[dot-run_discovery_for_profile()]] - code - backend/app/services/orchestrator.py
- [[DiscoveryOrchestrator]] - code - backend/app/services/orchestrator.py
- [[FastAPI]] - code
- [[ResearchService]] - code - backend/app/services/research.py
- [[get]] - code
- [[get_candidate_profile()]] - code - backend/app/core/config.py
- [[get_candidate_profile_endpoint()]] - code - backend/app/main.py
- [[health_check()]] - code - backend/app/main.py
- [[lifespan()]] - code - backend/app/main.py
- [[main.py]] - code - backend/app/main.py
- [[research.py]] - code - backend/app/services/research.py
- [[run_discovery_tick()]] - code - backend/app/services/scheduler.py
- [[run_tests()]] - code - backend/scripts/test_regression.py
- [[scheduler.py]] - code - backend/app/services/scheduler.py
- [[start_scheduler()]] - code - backend/app/services/scheduler.py
- [[test_regression.py]] - code - backend/scripts/test_regression.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Project_Architecture__Implementation_Phases
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_AI Dev Jobs Discovery Provider]]
- 4 edges to [[_COMMUNITY_Signalbase Discovery Adapter]]
- 3 edges to [[_COMMUNITY_Project Memory & Root Documentation]]
- 3 edges to [[_COMMUNITY_Playbook Execution & Knowledge Layer Rules]]
- 1 edge to [[_COMMUNITY_Frontend React Entrypoint & UI]]
- 1 edge to [[_COMMUNITY_Backend Supabase Client]]
- 1 edge to [[_COMMUNITY_The Muse Provider & Discovery Orchestration]]

## Top bridge nodes
- [[DiscoveryOrchestrator]] - degree 14, connects to 7 communities
- [[get_candidate_profile()]] - degree 12, connects to 2 communities
- [[test_regression.py]] - degree 6, connects to 2 communities
- [[run_tests()]] - degree 5, connects to 2 communities
- [[ResearchService]] - degree 5, connects to 1 community