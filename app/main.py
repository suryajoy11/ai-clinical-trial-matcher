from fastapi import FastAPI

from app.api.patients import router as patient_router
from app.api.matching import router as matching_router


app = FastAPI(
    title="AI Clinical Trial Matching System",
    description="AI-powered patient-to-clinical-trial matching system",
    version="1.0.0"
)


app.include_router(patient_router)
app.include_router(matching_router)


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