# Architecture Overview

This project aims to build a domain-specific data analyst agent that communicates
via a web-based chat interface. The core components include:

- **Web Framework**: A FastAPI application provides HTTP endpoints and auto-
  generated docs. Uvicorn runs the server.
- **State Management**: Chat history is stored in memory per session. Future
  versions will persist this data in a database. A simple character-based limit
  trims history to keep the context window manageable.
- **Data Ingestion**: CSV files are loaded into a SQLite database. Schema
  metadata from this database is supplied to the LLM to ground responses. SQL
  queries are executed with a row limit so large result sets do not overflow the
  context window.
- **LLM Integration**: The agent calls AWS Bedrock (e.g., Claude v3) using
  boto3. Logging and error handling capture request metadata and failures.
- **Agent Logic**: `ChatAgent` composes prompts from the system description,
  schema information, and conversation history before invoking Bedrock. Database
  queries are executed through helper utilities that limit returned rows and
  format results for the LLM.

Future enhancements include authentication, richer logging, and expanded data
sources.
