from fastapi import APIRouter

from app.models.patient import Patient


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("/")
def create_patient(patient: Patient):
    return {
        "message": "Patient received successfully",
        "patient": patient
    }