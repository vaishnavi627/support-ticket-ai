from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from app.ingestion import initialize_database, validate_database
from app.schemas import QueryRequest, QueryResponse, HealthResponse
from app.query_engine import QueryEngine
from app.anomaly_engine import AnomalyEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    validate_database()
    yield

app = FastAPI(
    title="AI Support Ticket Analytics",
    description="AI-powered customer support ticket analytics system.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        return QueryEngine().execute(request.question)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/anomalies")
def anomalies():
    try:
        results = AnomalyEngine().detect()
        return {"total_anomalies": len(results), "anomalies": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
