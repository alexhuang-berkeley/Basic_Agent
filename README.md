# Basic Agent

This repository contains a prototype of a domain-focused data analyst agent. It
provides a chat-based web interface backed by an LLM hosted on AWS Bedrock. The
agent relies on domain documents and ingested CSV data tables to answer
questions.

## Features

- Prompt templates describing the agent's purpose and available table schema.
- Utilities for ingesting CSV files into a SQLite database.
- FastAPI web application exposing `/chat` and `/query` endpoints.
- Simple chat memory per session stored in memory with a configurable
  context window size.
- Helper utilities to run SQL queries with row limits to control context
  length.
- Placeholder integration with AWS Bedrock including logging and error handling.
- Documentation outlining the architecture and future roadmap.

## Setup

1. Install Python 3.10 or newer.
2. Install dependencies with `pip install -r requirements.txt`.
3. Place CSV files inside a `data/` directory at the project root.
4. Run `python -m agent_app.main` and navigate to `http://localhost:8000/docs`
   to interact with the API.

## Roadmap

See `docs/roadmap.md` for planned enhancements including persistent chat
storage, document retrieval, richer logging around AWS Bedrock calls, and
authentication.
