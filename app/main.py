from fastapi import FastAPI

app = FastAPI(title="Agentic FastAPI App")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
