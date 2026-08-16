---
type: community
members: 5
---

# Playbook Execution & Knowledge Layer Rules

**Members:** 5 nodes

## Members
- [[Query how many .env files we have]] - document - graphify-out/memory/query_20260815_154958_how_many__env_files_we_have.md
- [[Three .env files configuration]] - concept - graphify-out/memory/query_20260815_154958_how_many__env_files_we_have.md
- [[backend .env]] - concept - graphify-out/memory/query_20260815_154958_how_many__env_files_we_have.md
- [[frontend .env]] - concept - graphify-out/memory/query_20260815_154958_how_many__env_files_we_have.md
- [[root .env]] - concept - graphify-out/memory/query_20260815_154958_how_many__env_files_we_have.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Playbook_Execution__Knowledge_Layer_Rules
SORT file.name ASC
```
