from typing import List, Optional
from pydantic import BaseModel


class TrialMatch(BaseModel):
    nct_id: str
    title: str
    status: Optional[str] = None
    rule_score: float
    nlp_score: float
    score: float
    reasons: List[str]
    warnings: List[str]


class MatchResponse(BaseModel):
    patient_id: str
    condition: str
    trials_found: int
    matches: List[TrialMatch]