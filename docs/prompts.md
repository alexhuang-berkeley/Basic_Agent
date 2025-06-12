# Prompt Design

Prompts guide the LLM on how to behave and what data is available.

## System Prompt
The system prompt summarizes the agent's role and the domain context. It is
assembled using the `system_prompt` function in `agent_app.prompts` and is the
first message sent to the LLM.

## Schema Information
When CSV files are ingested, their table names and columns are formatted with the
`schema_prompt` function. This string is included when the `ChatAgent` composes
a prompt so the LLM knows which tables are available and what columns they
contain.
