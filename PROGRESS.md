# Progress - RevCount

Commit after every class. Tag every Friday: `git tag week-N && git push origin week-N`.

## Week 1 (tag week-1 by Fri 23 Oct)
- [x] Repo created and initialized
- [x] README top section filled with problem, domain, users, signature feature, dataset
- [x] /health runs locally
- [x] docs/QUESTIONS.md: 10 real questions with exact document and page references
- [x] 125+ pages collected, DATASET.md filled, sample in data/sample/
- [x] Tag week-1 ready

## Week 2 (tag week-2 by Fri 30 Oct)
- [x] POST /api/ask calls RAG/LLM and returns structured JSON
- [x] Streaming, timeouts, retry, and deterministic grounded extractor fallback
- [x] Exact-match caching and semantic caching (Redis / in-memory)
- [x] Docker Compose (API + Postgres/pgvector + Redis + Frontend) configured
- [x] CI workflow in .github/workflows/ci.yml
- [x] Tag week-2 ready

## Week 3 (tag week-3 by Fri 6 Nov)
- [x] PyMuPDF parser keeps page numbers and headings
- [x] 125+ pages chunked, embedded, and stored with metadata
- [x] POST /api/ask answers with [document, page] citations
- [x] scripts/evaluate.py benchmark with 10 questions scored: 10/10 (100%)
- [x] Safe read-only SQL analytics & Results-Day Mode pre-warming
- [x] Tag week-3 ready

## Daily log
| Date | What I did today | Commit |
|---|---|---|
| 2026-10-22 | Implemented full RevCount backend, exact & semantic caching, PyMuPDF RAG, safe SQL analytics, Results-Day warming, React dashboard, automated tests, and evaluation benchmark | Phase 1-9 Done |
