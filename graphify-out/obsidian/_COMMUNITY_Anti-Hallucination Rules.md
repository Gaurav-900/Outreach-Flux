---
type: community
members: 2
---

# Anti-Hallucination Rules

**Members:** 2 nodes

## Members
- [[dot-is_available()_2]] - code - backend/app/providers/base.py
- [[Determines if the provider is currently available (e.g., API keys are present).]] - rationale - backend/app/providers/base.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Anti-Hallucination_Rules
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Playbook Execution & Knowledge Layer Rules]]

## Top bridge nodes
- [[dot-is_available()_2]] - degree 2, connects to 1 community