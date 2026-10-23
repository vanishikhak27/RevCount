# RevCount

## Product

I am developing **RevCount**, an AI-powered financial reporting assistant that helps reporters find answers about India's two-wheeler companies using official financial reports. My goal is to make answers faster and reduce repeated AI model calls using caching.

## Target User

My target users are auto-sector reporters working at Tamil business news websites who need to answer readers' questions quickly during quarterly results announcements.

## Problem

During quarterly results announcements, thousands of readers ask similar questions about TVS Motor, Bajaj Auto, Hero MotoCorp, Eicher Motors and Ather Energy. Answering every question separately using an AI model can increase response time and operating costs. I want to solve this problem by building a system that reuses cached answers, handles similar questions efficiently, and provides source references so users can verify financial information.

## Solution

To solve this problem, I plan to:

- Collect and process official financial reports from the five companies.
- Use Retrieval-Augmented Generation (RAG) to answer questions based on report content.
- Implement exact-match caching and semantic caching using Redis.
- Invalidate outdated cached answers when new reports are uploaded.
- Store structured financial data in PostgreSQL and generate comparison charts.
- Implement a Results-day mode that preloads answers to 50 frequently asked questions.
- Test the system under a simulated workload of 10,000 users and measure response time, cache hit rate and errors.

## Dataset Source

I am collecting financial reports from official company websites.

**Primary source — TVS Motor Company:**

https://www.tvsmotor.com/annual-report

I plan to collect annual reports, Business Responsibility and Sustainability Reports (BRSRs), and quarterly results PDFs covering three years.

## Planned Dataset Size

My target dataset consists of:

- 15 annual reports
- 60 quarterly results PDFs
- More than 5,000 pages of financial and business information

I will record the source URL, document name, financial year and page count for each collected document.

**10 real questions**

See docs/QUESTIONS.md.

## Week 1 Data Collection

**Source URL:** https://www.tvsmotor.com/annual-report

I am starting my data collection with TVS Motor's official annual reports. I will then expand the dataset to include quarterly results and reports from the other four companies.

**Collected documents:**
- PDF filename: Annual_Report_FY_2020-21.pdf
- Financial year: 2020-21
- Page count: 226

**Total pages collected:** 226 pages.

**Current dataset status:** I have collected one TVS Motor annual report for FY 2020–21, containing 226 pages. This is my initial dataset. I plan to expand it with more recent annual reports, quarterly results and reports from the other four companies to reach my target of 5,000+ pages.

My Week 1 target was to collect at least 50 pages of official source material and document the dataset details. I have collected 226 pages from the official TVS Motor annual report, exceeding my initial target.

## Week 1 Deliverables

- Create the GitHub repository using the Examate template.
- Complete the project README.
- Document 10 realistic questions, including one unanswerable question.
- Collect at least 50 pages of official financial reports.
- Record the dataset sources, document names and page counts.
- Create and push the `week-1` Git tag.

## Expected Outcome

Through RevCount, I aim to build a financial reporting assistant that delivers faster answers, reduces unnecessary AI calls, handles high traffic efficiently and provides reliable source references for financial information.


## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link
<Added in Week 2>
