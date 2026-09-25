
from fastapi import APIRouter, HTTPException

from app.models.patient import Patient
from app.models.match import MatchResponse
from app.services.clinical_trials import search_trials
from app.services.trial_parser import parse_trial
from app.services.matcher import calculate_match_score


router = APIRouter(
    prefix="/match",
    tags=["Clinical Trial Matching"]
)


@router.post("/", response_model=MatchResponse)
def match_patient_to_trials(patient: Patient):
    try:
        # Search ClinicalTrials.gov
        data = search_trials(
            patient.condition,
            page_size=10
        )

        results = []

        # Parse and score every trial
        for study in data.get("studies", []):
            trial = parse_trial(study)

            match = calculate_match_score(
                patient,
                trial
            )

            results.append({
                "nct_id": trial["nct_id"],
                "title": trial["title"],
                "status": trial["overall_status"],
                "rule_score": float(match["rule_score"]),
                "nlp_score": float(match["nlp_score"]),
                "score": float(match["score"]),
                "reasons": match["reasons"],
                "warnings": match["warnings"]
            })
        # Highest score first
        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return {
            "patient_id": patient.patient_id,
            "condition": patient.condition,
            "trials_found": len(results),
            "matches": results
        }

    except Exception as exc:
        import traceback
    traceback.print_exc()
    raise HTTPException(
        status_code=500,
        detail=f"Trial matching failed: {str(exc)}"
    )