---
type: community
members: 15
---

# Discovery Base Interfaces & Normalized Models

**Members:** 15 nodes

## Members
- [[dot-find_contacts()]] - code - backend/app/providers/contact.py
- [[dot-find_contacts()_1]] - code - backend/app/providers/tomba.py
- [[dot-is_available()_5]] - code - backend/app/providers/contact.py
- [[dot-is_available()_6]] - code - backend/app/providers/tomba.py
- [[dot-name()_6]] - code - backend/app/providers/contact.py
- [[dot-name()_7]] - code - backend/app/providers/tomba.py
- [[ABC_2]] - code
- [[ContactProvider]] - code - backend/app/providers/contact.py
- [[Determines if the provider is currently available (e.g., API keys are present)._1]] - rationale - backend/app/providers/contact.py
- [[Execute a search against the provider to find contacts for a company.]] - rationale - backend/app/providers/contact.py
- [[NormalizedContact]] - code - backend/app/providers/base.py
- [[The unique identifier for this provider._1]] - rationale - backend/app/providers/contact.py
- [[TombaAdapter]] - code - backend/app/providers/tomba.py
- [[providerscontact.py]] - code - backend/app/providers/contact.py
- [[tomba.py]] - code - backend/app/providers/tomba.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Discovery_Base_Interfaces__Normalized_Models
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Candidate Schemas & Validation Models]]

## Top bridge nodes
- [[NormalizedContact]] - degree 8, connects to 1 community