---
type: community
members: 3
---

# Global Definition of Done

**Members:** 3 nodes

## Members
- [[App()]] - code - frontend/src/App.tsx
- [[App.tsx]] - code - frontend/src/App.tsx
- [[main.tsx]] - code - frontend/src/main.tsx

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Global_Definition_of_Done
SORT file.name ASC
```
