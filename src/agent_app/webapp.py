"""FastAPI web application exposing a chat endpoint."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .data_ingestion import schema_metadata
from .agent import ChatAgent
from .database import execute_query

logger = logging.getLogger(__name__)
app = FastAPI(title="LLM Data Analyst")

# In-memory store of agents per session ID
_sessions: Dict[str, ChatAgent] = {}


def get_agent(session_id: str) -> ChatAgent:
    if session_id not in _sessions:
        csv_dir = Path("data")
        db_path = Path(f"{session_id}.db")
        schema_info = schema_metadata(csv_dir, db_path)
        agent = ChatAgent(
            domain_description="Operations data analysis for the supply chain domain",
            schema_info=schema_info,
            model_id="anthropic.claude-v3",
            db_path=db_path,
        )
        _sessions[session_id] = agent
    return _sessions[session_id]


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


class QueryRequest(BaseModel):
    session_id: str
    sql: str
    limit: int = 100


class QueryResponse(BaseModel):
    row_count: int
    rows: List[Dict[str, Any]]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    agent = get_agent(req.session_id)
    try:
        reply = agent.chat(req.message)
    except Exception as exc:  # pragma: no cover - runtime error path
        logger.error("Chat failed: %s", exc)
        raise HTTPException(status_code=500, detail="LLM call failed")
    return ChatResponse(response=reply)


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    agent = get_agent(req.session_id)
    try:
        count, rows = execute_query(agent.db_path, req.sql, req.limit)
    except Exception as exc:  # pragma: no cover - runtime error path
        logger.error("Query failed: %s", exc)
        raise HTTPException(status_code=500, detail="Query failed")
    return QueryResponse(row_count=count, rows=rows)
