from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Agentic FastAPI App")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "time_utc": datetime.now(timezone.utc).isoformat(),
    }
