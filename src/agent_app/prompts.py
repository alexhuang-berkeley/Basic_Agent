"""Prompt templates for the LLM agent."""

from typing import List


def system_prompt(domain_description: str) -> str:
    """Return the system prompt describing the agent's purpose."""
    return (
        "You are a data analyst assistant. "
        f"Domain description: {domain_description}. "
        "Use provided documents and data tables to answer questions."
    )


def schema_prompt(tables: List[dict]) -> str:
    """Format table schema metadata for inclusion in prompts.

    Args:
        tables: List of dictionaries with keys 'name' and 'columns'.
    """
    lines = ["Available tables and columns:"]
    for table in tables:
        cols = ", ".join(table.get("columns", []))
        lines.append(f"- {table['name']}: {cols}")
    return "\n".join(lines)
