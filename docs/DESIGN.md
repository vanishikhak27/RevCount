# RevCount — API and Database Design

## 1. Overview

RevCount is an AI-powered financial reporting assistant for answering questions about automotive companies using financial reports and language models.

## 2. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/hello` | Basic application greeting |
| GET | `/health` | Checks whether the API is running |
| GET | `/ready` | Checks API readiness and PostgreSQL connectivity |
| GET | `/usage` | Returns tracked LLM token usage and estimated cost |
| POST | `/chat` | Accepts a chat question and returns an AI response |

## 3. Database Design

### Current implementation

- PostgreSQL is configured through the `DATABASE_URL` environment variable.
- The API uses `/ready` to verify database connectivity with a simple query.
- No application-specific tables have been defined yet.

### Planned tables

| Table | Purpose |
|---|---|
| `companies` | Company names and identifiers |
| `documents` | Financial report metadata, source, and version |
| `financial_metrics` | Extracted financial values by company and period |
| `llm_usage` | Token usage and estimated cost records, if persisted |

These tables are planned and are not yet implemented.

## 4. Caching

Redis caching is planned for repeated questions and responses. Cache entries should be associated with document versions to prevent stale answers after reports are updated.

## 5. AI and Retrieval

The chat endpoint uses an LLM provider with a fallback model. Retrieval-augmented generation (RAG) over financial reports is part of the planned reporting workflow.

## 6. Health and Readiness

- `/health` checks API process health.
- `/ready` checks PostgreSQL connectivity.
- `/usage` reports tracked LLM token usage and estimated cost.
