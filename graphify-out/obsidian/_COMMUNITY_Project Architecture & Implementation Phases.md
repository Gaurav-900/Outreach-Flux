---
type: community
members: 40
---

# Project Architecture & Implementation Phases

**Members:** 40 nodes

## Members
- [[dot-is_available()]] - code - backend/app/providers/adzuna.py
- [[dot-is_available()_1]] - code - backend/app/providers/aidevjobs.py
- [[dot-is_available()_2]] - code - backend/app/providers/base.py
- [[dot-is_available()_3]] - code - backend/app/providers/freehire.py
- [[dot-is_available()_4]] - code - backend/app/providers/signalbase.py
- [[dot-is_available()_5]] - code - backend/app/providers/themuse.py
- [[dot-keywords()]] - code - backend/app/models/candidate.py
- [[dot-name()]] - code - backend/app/models/candidate.py
- [[dot-name()_1]] - code - backend/app/providers/adzuna.py
- [[dot-name()_2]] - code - backend/app/providers/aidevjobs.py
- [[dot-name()_4]] - code - backend/app/providers/freehire.py
- [[dot-name()_5]] - code - backend/app/providers/signalbase.py
- [[dot-name()_6]] - code - backend/app/providers/themuse.py
- [[dot-search()]] - code - backend/app/providers/adzuna.py
- [[dot-search()_1]] - code - backend/app/providers/aidevjobs.py
- [[dot-search()_2]] - code - backend/app/providers/base.py
- [[dot-search()_3]] - code - backend/app/providers/freehire.py
- [[dot-search()_4]] - code - backend/app/providers/signalbase.py
- [[dot-search()_5]] - code - backend/app/providers/themuse.py
- [[ABC]] - code
- [[AIDevJobsAdapter]] - code - backend/app/providers/aidevjobs.py
- [[AdzunaAdapter]] - code - backend/app/providers/adzuna.py
- [[BaseModel]] - code
- [[Determines if the provider is currently available (e.g., API keys are present).]] - rationale - backend/app/providers/base.py
- [[DiscoveryProfile]] - code - backend/app/models/candidate.py
- [[Execute a search against the provider.]] - rationale - backend/app/providers/base.py
- [[FreeHireAdapter]] - code - backend/app/providers/freehire.py
- [[IDiscoveryProvider]] - code - backend/app/providers/base.py
- [[NormalizedCompany]] - code - backend/app/providers/base.py
- [[NormalizedOpportunity]] - code - backend/app/providers/base.py
- [[ProviderSearchResult]] - code - backend/app/providers/base.py
- [[SignalbaseAdapter]] - code - backend/app/providers/signalbase.py
- [[TheMuseAdapter]] - code - backend/app/providers/themuse.py
- [[adzuna.py]] - code - backend/app/providers/adzuna.py
- [[aidevjobs.py]] - code - backend/app/providers/aidevjobs.py
- [[base.py]] - code - backend/app/providers/base.py
- [[freehire.py]] - code - backend/app/providers/freehire.py
- [[orchestrator.py]] - code - backend/app/services/orchestrator.py
- [[signalbase.py]] - code - backend/app/providers/signalbase.py
- [[themuse.py]] - code - backend/app/providers/themuse.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Project_Architecture__Implementation_Phases
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Discovery Base Interfaces & Normalized Models]]
- 3 edges to [[_COMMUNITY_AI Dev Jobs Discovery Provider]]
- 2 edges to [[_COMMUNITY_Research Service & Intelligence Layer]]
- 1 edge to [[_COMMUNITY_Frontend React Entrypoint & UI]]

## Top bridge nodes
- [[DiscoveryProfile]] - degree 25, connects to 2 communities
- [[orchestrator.py]] - degree 11, connects to 2 communities
- [[IDiscoveryProvider]] - degree 17, connects to 1 community
- [[FreeHireAdapter]] - degree 12, connects to 1 community
- [[TheMuseAdapter]] - degree 12, connects to 1 community