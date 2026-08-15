# Graph Report - .  (2026-08-15)

## Corpus Check
- Corpus is ~5,110 words - fits in a single context window. You may not need a graph.

## Summary
- 24 nodes · 20 edges · 8 communities (5 shown, 3 thin omitted)
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Candidate Discovery & Sourcing
- Verification & Batch Outreach
- Gmail Dispatch & Reply Tracking
- Database Canonicalization & Matching
- Contact Info Discovery
- Foundations & Knowledge Graph
- Oracle VPS Deployment
- Cron Automation & Orchestration

## God Nodes (most connected - your core abstractions)
1. `Tomba Contact Fallback` - 3 edges
2. `EVA Email Verification` - 3 edges
3. `LLM Batch Outreach Email Generation (Gemini/DeepSeek)` - 3 edges
4. `Gmail API Sending Policy & Controls` - 3 edges
5. `Phase 2 - Multi-Provider Incremental Discovery` - 2 edges
6. `Phase 3 - Database Canonicalization + Matching + Research` - 2 edges
7. `Phase 4 - Contact Discovery` - 2 edges
8. `Candidate JSON Config` - 2 edges
9. `Discovery Profile Rotation` - 2 edges
10. `Discovery Providers (FreeHire, Adzuna, The Muse, AI Dev Jobs, Funding Signals)` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Phase 1 - Candidate JSON` --implements--> `Candidate JSON Config`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 2 - Multi-Provider Incremental Discovery` --implements--> `Discovery Profile Rotation`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 2 - Multi-Provider Incremental Discovery` --implements--> `Discovery Providers (FreeHire, Adzuna, The Muse, AI Dev Jobs, Funding Signals)`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 3 - Database Canonicalization + Matching + Research` --implements--> `Database Canonicalization Layer`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md
- `Phase 3 - Database Canonicalization + Matching + Research` --implements--> `Deterministic Candidate Matching`  [EXTRACTED]
  AI_JOB_OUTREACH_PHASE_PLAYBOOK_UPDATED.md → AI_JOB_OUTREACH_PROJECT_MEMORY_UPDATED.md

## Hyperedges (group relationships)
- **AI Job Outreach End-to-End Pipeline Flow** — ai_job_outreach_project_memory_updated_candidate_json, ai_job_outreach_project_memory_updated_discovery_profile_rotation, ai_job_outreach_project_memory_updated_discovery_providers, ai_job_outreach_project_memory_updated_database_canonicalization, ai_job_outreach_project_memory_updated_deterministic_matching, ai_job_outreach_project_memory_updated_contact_discovery, ai_job_outreach_project_memory_updated_eva_email_verification, ai_job_outreach_project_memory_updated_llm_email_batch_generation, ai_job_outreach_project_memory_updated_gmail_sending_policy, ai_job_outreach_project_memory_updated_reply_tracking [EXTRACTED 1.00]

## Communities (8 total, 3 thin omitted)

### Community 0 - "Candidate Discovery & Sourcing"
Cohesion: 0.40
Nodes (5): Phase 1 - Candidate JSON, Phase 2 - Multi-Provider Incremental Discovery, Candidate JSON Config, Discovery Profile Rotation, Discovery Providers (FreeHire, Adzuna, The Muse, AI Dev Jobs, Funding Signals)

### Community 1 - "Verification & Batch Outreach"
Cohesion: 0.50
Nodes (4): Phase 5 - Email Verification, Phase 6 - AI Outreach Batch Generation, EVA Email Verification, LLM Batch Outreach Email Generation (Gemini/DeepSeek)

### Community 2 - "Gmail Dispatch & Reply Tracking"
Cohesion: 0.50
Nodes (4): Phase 7 - Gmail + Sending Policy, Phase 8 - Tracking + Reply Classification, Gmail API Sending Policy & Controls, Gmail Reply Detection & Classification

### Community 3 - "Database Canonicalization & Matching"
Cohesion: 0.67
Nodes (3): Phase 3 - Database Canonicalization + Matching + Research, Database Canonicalization Layer, Deterministic Candidate Matching

### Community 4 - "Contact Info Discovery"
Cohesion: 1.00
Nodes (3): Phase 4 - Contact Discovery, Contact Discovery Priority, Tomba Contact Fallback

## Knowledge Gaps
- **3 isolated node(s):** `Graphify Knowledge/Memory Layer`, `Deterministic Candidate Matching`, `Oracle VPS Deployment Stack`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLM Batch Outreach Email Generation (Gemini/DeepSeek)` connect `Verification & Batch Outreach` to `Gmail Dispatch & Reply Tracking`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Why does `EVA Email Verification` connect `Verification & Batch Outreach` to `Contact Info Discovery`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `Gmail API Sending Policy & Controls` connect `Gmail Dispatch & Reply Tracking` to `Verification & Batch Outreach`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `EVA Email Verification` (e.g. with `LLM Batch Outreach Email Generation (Gemini/DeepSeek)` and `Tomba Contact Fallback`) actually correct?**
  _`EVA Email Verification` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LLM Batch Outreach Email Generation (Gemini/DeepSeek)` (e.g. with `EVA Email Verification` and `Gmail API Sending Policy & Controls`) actually correct?**
  _`LLM Batch Outreach Email Generation (Gemini/DeepSeek)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Gmail API Sending Policy & Controls` (e.g. with `Gmail Reply Detection & Classification` and `LLM Batch Outreach Email Generation (Gemini/DeepSeek)`) actually correct?**
  _`Gmail API Sending Policy & Controls` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Graphify Knowledge/Memory Layer`, `Deterministic Candidate Matching`, `Oracle VPS Deployment Stack` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._