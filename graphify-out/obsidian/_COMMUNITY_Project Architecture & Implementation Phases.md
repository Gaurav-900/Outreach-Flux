---
type: community
members: 36
---

# Project Architecture & Implementation Phases

**Members:** 36 nodes

## Members
- [[dot-__init__()_4]] - code - backend/app/services/automation.py
- [[dot-__init__()_7]] - code - backend/app/services/outreach_generator.py
- [[dot-_process_follow_ups()]] - code - backend/app/services/automation.py
- [[dot-_run_discovery()]] - code - backend/app/services/automation.py
- [[dot-generate_batch()]] - code - backend/app/services/outreach_generator.py
- [[dot-generate_drafts()_2]] - code - backend/app/providers/llm.py
- [[dot-generate_drafts()_1]] - code - backend/app/providers/llm.py
- [[dot-generate_drafts()]] - code - backend/app/providers/llm.py
- [[dot-is_available()_9]] - code - backend/app/providers/llm.py
- [[dot-is_available()_8]] - code - backend/app/providers/llm.py
- [[dot-is_available()_7]] - code - backend/app/providers/llm.py
- [[dot-name()_10]] - code - backend/app/providers/llm.py
- [[dot-name()_9]] - code - backend/app/providers/llm.py
- [[dot-name()_8]] - code - backend/app/providers/llm.py
- [[dot-run_automation_tick()]] - code - backend/app/services/automation.py
- [[ABC_3]] - code
- [[AutomationOrchestrator]] - code - backend/app/services/automation.py
- [[BaseModel_1]] - code
- [[DeepSeekAdapter]] - code - backend/app/providers/llm.py
- [[Determines if the provider is currently available.]] - rationale - backend/app/providers/llm.py
- [[EmailBatchResponse]] - code - backend/app/providers/llm.py
- [[EmailDraft]] - code - backend/app/providers/llm.py
- [[GeminiAdapter]] - code - backend/app/providers/llm.py
- [[Generate personalized email drafts for a batch of opportunities.]] - rationale - backend/app/providers/llm.py
- [[LLMProvider]] - code - backend/app/providers/llm.py
- [[OpportunityContext]] - code - backend/app/providers/llm.py
- [[OutreachGeneratorService]] - code - backend/app/services/outreach_generator.py
- [[The unique identifier for this provider._2]] - rationale - backend/app/providers/llm.py
- [[_build_prompt()]] - code - backend/app/providers/llm.py
- [[automation.py]] - code - backend/app/services/automation.py
- [[llm.py]] - code - backend/app/providers/llm.py
- [[main()_1]] - code - backend/test_full_pipeline.py
- [[main()_2]] - code - backend/test_gen.py
- [[outreach_generator.py]] - code - backend/app/services/outreach_generator.py
- [[test_full_pipeline.py]] - code - backend/test_full_pipeline.py
- [[test_gen.py]] - code - backend/test_gen.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Project_Architecture__Implementation_Phases
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_AI Dev Jobs Discovery Provider]]

## Top bridge nodes
- [[AutomationOrchestrator]] - degree 7, connects to 1 community