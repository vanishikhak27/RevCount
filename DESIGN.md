

\# RevCount — System Design



\## 1. Project Overview



RevCount is an AI-powered financial reporting assistant for auto-sector reporters covering Indian two-wheeler companies, including TVS Motor, Bajaj Auto, and Hero MotoCorp.



The current backend uses FastAPI and Google's Gemini API to answer questions. Annual-report retrieval, persistent storage, and caching are planned enhancements and are not yet implemented.



\## 2. Architecture



```text

User / Reporter

&#x20;     |

&#x20;     v

FastAPI Backend

&#x20;     |

&#x20;     v

Question Validation

&#x20;     |

&#x20;     v

Gemini API + RevCount Context

&#x20;     |

&#x20;     v

Answer + Token Usage

&#x20;     |

&#x20;     v

JSON Response

```



The backend also provides a health endpoint and process-local usage statistics.



\## 3. API Endpoints



| Method | Endpoint | Purpose |

|--------|----------|---------|

| GET | `/` | Return basic application information |

| GET | `/health` | Check application health |

| POST | `/api/ask` | Send a question to Gemini |

| GET | `/usage` | View request counts and token usage |



\### POST /api/ask



Example request:



```json

{

&#x20; "question": "What is the purpose of RevCount?"

}

```



Successful response structure:



```json

{

&#x20; "answer": "Generated answer",

&#x20; "source": "gemini",

&#x20; "usage": {

&#x20;   "input\_tokens": 9,

&#x20;   "output\_tokens": 7,

&#x20;   "total\_tokens": 16

&#x20; }

}

```



Token counts vary with each request.



\### GET /usage



Reports total requests, successful requests, fallback requests, input tokens, output tokens, and total tokens.



Usage counters are currently stored in application memory and reset when the process restarts. Cost estimation is not implemented yet.



\## 4. Data Model



The current application does not use a database. The following tables are proposed for a future persistent implementation.



\### Company



| Field | Purpose |

|-------|---------|

| company\_id | Unique company identifier |

| name | Company name |

| ticker | Stock ticker, where applicable |



\### FinancialReport



| Field | Purpose |

|-------|---------|

| report\_id | Unique report identifier |

| company\_id | Reference to Company |

| report\_type | Annual or quarterly report |

| reporting\_period | Period covered |

| document\_path | Stored report location |

| uploaded\_at | Upload timestamp |



\### ReportChunk



| Field | Purpose |

|-------|---------|

| chunk\_id | Unique text chunk identifier |

| report\_id | Reference to FinancialReport |

| page\_number | Source page number |

| content | Extracted report text |

| embedding | Optional vector representation for retrieval |



These tables are proposed and have not yet been created.



\## 5. Technology Stack



\- Python

\- FastAPI

\- Pydantic Settings

\- Google GenAI Python SDK

\- Gemini API

\- Pytest

\- Ruff

\- Docker

\- GitHub Actions



\## 6. Error Handling



\- Validate questions before processing.

\- Return a fallback response if the AI request fails.

\- Avoid exposing API keys in error logs.

\- Track successful and failed requests.



\## 7. Planned Improvements



1\. Extract text and tables from official financial reports.

2\. Implement retrieval-augmented generation (RAG).

3\. Include report and page citations in answers.

4\. Add persistent database storage.

5\. Add Redis caching and cache invalidation.

6\. Calculate API costs using verified model pricing.

7\. Deploy the API and perform load testing.



