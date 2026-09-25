
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


ALLOWED_STATUSES = {
    "RECRUITING",
    "NOT_YET_RECRUITING",
    "ENROLLING_BY_INVITATION"
}


@router.post("/", response_model=MatchResponse)
def match_patient_to_trials(patient: Patient):
    try:
        # Retrieve studies from ClinicalTrials.gov
        data = search_trials(
            patient.condition,
            page_size=10
        )

        results = []

        # Parse, filter and score each study
        for study in data.get("studies", []):
            trial = parse_trial(study)

            # Exclude trials outside the selected statuses
            if trial.get("overall_status") not in ALLOWED_STATUSES:
                continue

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

        # Rank highest scores first
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
        raise HTTPException(
            status_code=500,
            detail="Clinical trial matching failed"
        ) from exc