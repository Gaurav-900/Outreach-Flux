---
type: community
members: 10
---

# Adzuna Discovery Adapter

**Members:** 10 nodes

## Members
- [[dot-__init__()]] - code - backend/app/services/reply_tracker.py
- [[dot-_authenticate_silently()]] - code - backend/app/services/reply_tracker.py
- [[dot-_classify_message()]] - code - backend/app/services/reply_tracker.py
- [[dot-_update_last_check()]] - code - backend/app/services/reply_tracker.py
- [[dot-check_for_replies()]] - code - backend/app/services/reply_tracker.py
- [[Any]] - code
- [[Deterministic heuristic classifier for auto vs human replies.]] - rationale - backend/app/services/reply_tracker.py
- [[Polls Gmail for new replies on SENT outreaches and updates Supabase.]] - rationale - backend/app/services/reply_tracker.py
- [[ReplyTrackerService]] - code - backend/app/services/reply_tracker.py
- [[reply_tracker.py]] - code - backend/app/services/reply_tracker.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Adzuna_Discovery_Adapter
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_AI Dev Jobs Discovery Provider]]

## Top bridge nodes
- [[ReplyTrackerService]] - degree 8, connects to 1 community