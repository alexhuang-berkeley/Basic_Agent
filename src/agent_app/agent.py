"""Simple chat agent that maintains conversation history and calls Bedrock."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict
from pathlib import Path
import logging

from .prompts import system_prompt
from .llm import invoke_bedrock
from .database import execute_query, format_rows

logger = logging.getLogger(__name__)


@dataclass
class ChatAgent:
    """LLM-powered chat agent."""

    domain_description: str
    schema_info: str
    model_id: str
    db_path: Path
    max_history_chars: int = 8000
    history: List[Dict[str, str]] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        self._trim_history()

    def _trim_history(self) -> None:
        """Ensure the history stays within the max character limit."""
        text = "\n".join(f"{m['role']}: {m['content']}" for m in self.history)
        while len(text) > self.max_history_chars and self.history:
            self.history.pop(0)
            text = "\n".join(f"{m['role']}: {m['content']}" for m in self.history)

    def build_prompt(self, user_message: str) -> str:
        lines = [system_prompt(self.domain_description), self.schema_info]
        for msg in self.history:
            lines.append(f"{msg['role']}: {msg['content']}")
        lines.append(f"user: {user_message}")
        return "\n".join(lines)

    def chat(self, message: str) -> str:
        """Send a message to the agent and return the response."""
        prompt = self.build_prompt(message)
        try:
            reply = invoke_bedrock(prompt, self.model_id)
        except Exception as exc:  # pragma: no cover - runtime error path
            logger.error("LLM call failed: %s", exc)
            raise
        self.add_message("user", message)
        self.add_message("assistant", reply)
        return reply

    def query_db(self, sql: str, max_rows: int = 100) -> str:
        """Execute a SQL query and return formatted results."""
        try:
            count, rows = execute_query(self.db_path, sql, max_rows)
        except Exception as exc:  # pragma: no cover - runtime error path
            logger.error("Query failed: %s", exc)
            raise
        return format_rows(count, rows, max_rows)
