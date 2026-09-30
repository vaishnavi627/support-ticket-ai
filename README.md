# AI Support Ticket Analytics

AI-powered customer support ticket analytics system built for the DOTMappers AI Intern Assessment.

## Architecture

```text
support_tickets.csv
        |
        v
  Data Ingestion
        |
        v
     DuckDB
      /   \
     /     \
    v       v
Query Engine  Anomaly Engine
    |
    v
   Groq LLM
    |
    v
SQL Validator
    |
    v
   DuckDB
    |
    +----------+
    |          |
    v          v
 FastAPI   Streamlit
 :8000      :8501
```

Natural-language query flow:

`User -> Streamlit -> FastAPI -> Groq -> SQL Validator -> DuckDB -> Result`

## Features

- CSV ingestion into DuckDB
- Natural-language data questions using Groq
- SQL validation before execution
- Anomaly detection:
  - unusually long resolution times
  - unresolved High/Critical tickets older than 24 hours
  - unusually slow response times
- REST API
- Streamlit UI
- Health check endpoint
- Automated tests

## Requirements

- Docker Desktop with Docker Compose
- A Groq API key using an allowed/free-tier account

No paid API or external database service is required.

## Recommended one-command startup

1. Create a file named `.env` in the project root using `.env.example` as a template.
2. Put your Groq API key in `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

3. Start the complete system with one command:

```bash
docker compose up
```

Docker Compose starts both the FastAPI backend and Streamlit UI. The UI waits for the API health check before starting.

Open:

- Streamlit UI: `http://localhost:8501`
- FastAPI docs: `http://localhost:8001/docs`
- Health: `http://localhost:8001/health`

Stop the system with `Ctrl+C`.

## Local Python setup (optional)

Python 3.11+ is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example`, then run the API:

```bash
uvicorn app.main:app --reload
```

In another terminal, run the UI:

```bash
streamlit run ui/streamlit_app.py
```

## Example Questions

- How many tickets are currently open?
- How many critical tickets are unresolved?
- Which agent resolved the most tickets?
- Which agent has the lowest average customer rating?
- What is the average customer rating for Technical tickets?
- Show all Critical tickets not resolved within 12 hours.

## API

### Health

`GET /health`

### Natural-language query

`POST /query`

```json
{
  "question": "How many critical tickets are unresolved?"
}
```

### Anomalies

`GET /anomalies`

## Security

The LLM is instructed to generate read-only SQL against the `tickets` table. Generated SQL is validated before execution. Destructive SQL operations and unauthorized tables are rejected.

## Known Limitations

- Groq requires a valid API key.
- The current anomaly rules are intentionally simple and deterministic.
- The current query layer focuses on structured ticket analytics.
- Semantic search over `issue_summary` could be added later.
- Relative time phrases such as “this week” are interpreted using the dataset timeline rather than assuming the real-world current date.

## Testing

Run:

```bash
pytest
```

The tests cover SQL validation and anomaly-engine behavior.
