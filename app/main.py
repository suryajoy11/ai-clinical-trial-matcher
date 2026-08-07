from fastapi import FastAPI

app = FastAPI(
    title="AI Clinical Trial Matching System",
    description="AI-powered system for matching patients with clinical trials",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "application": "AI Clinical Trial Matching System",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
