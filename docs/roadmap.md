# Roadmap

1. **Prototype** - FastAPI chat UI with CSV ingestion and prompt generation.
2. **Document/Data Retrieval** - Add search APIs for domain documents and table
   queries.
3. **State Management** - Persist conversation history and user sessions in a
   database. Trim stored history to manage the LLM context window.
4. **Logging & Error Handling** - Capture AWS Bedrock calls and gracefully
   handle failures or rate limits.
5. **Authentication** - Restrict access to data and documents based on user
   roles and ensure data privacy.
6. **Query Tools** - Provide SQL query APIs with row limits and summarization.
