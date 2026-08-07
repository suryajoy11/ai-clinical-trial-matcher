from typing import List, Optional
from pydantic import BaseModel, Field


class Patient(BaseModel):
    patient_id: str

    age: int = Field(..., ge=0, le=120)

    gender: str

    condition: str

    medications: List[str] = []

    diagnoses: List[str] = []

    biomarkers: List[str] = []

    city: Optional[str] = None

    state: Optional[str] = None

    country: str = "United States"
