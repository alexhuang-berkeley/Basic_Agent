"""Entry point to run the FastAPI web application."""

from __future__ import annotations

import uvicorn


def main() -> None:
    uvicorn.run("agent_app.webapp:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
