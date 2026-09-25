from app.services.nlp_similarity import calculate_text_similarity
from app.utils.preprocessing import extract_age


def calculate_match_score(patient, trial):
    score = 0
    reasons = []
    warnings = []

    # -------------------------
    # 1. Condition matching
    # -------------------------
    condition = patient.condition.lower()
    title = (trial.get("title") or "").lower()
    criteria = (trial.get("eligibility_criteria") or "").lower()

    if condition in title:
        score += 30
        reasons.append("Patient condition matches trial title")

    elif condition in criteria:
        score += 20
        reasons.append("Patient condition appears in eligibility criteria")

    else:
        warnings.append("Exact condition match was not found")

    # -------------------------
    
    # 2. Age eligibility
    minimum_age = extract_age(trial.get("minimum_age"))
    maximum_age = extract_age(trial.get("maximum_age"))

    patient_age_months = patient.age * 12
    age_eligible = True

    if minimum_age is not None and patient_age_months < minimum_age:
        age_eligible = False
        warnings.append("Patient is below minimum age")

    if maximum_age is not None and patient_age_months > maximum_age:
        age_eligible = False
        warnings.append("Patient exceeds maximum age")

    if age_eligible:
        if minimum_age is None or maximum_age is None:
            warnings.append(
                "Some age eligibility information is unavailable"
            )
        else:
            score += 25
            reasons.append("Patient meets trial age requirements")

# -------------------------
    # 3. Sex eligibility
    # -------------------------
    trial_sex = (trial.get("sex") or "").upper()
    patient_sex = patient.gender.upper()

    if trial_sex == "ALL":
        score += 15
        reasons.append("Trial accepts all sexes")

    elif trial_sex == patient_sex:
        score += 15
        reasons.append("Patient sex matches trial requirement")

    else:
        warnings.append("Patient sex may not meet trial requirement")

    # -------------------------
    # 4. Recruitment status
    # -------------------------
    status = trial.get("overall_status")

    if status == "RECRUITING":
        score += 30
        reasons.append("Trial is currently recruiting")

    elif status in [
        "NOT_YET_RECRUITING",
        "ACTIVE_NOT_RECRUITING"
    ]:
        score += 10
        reasons.append(
            f"Trial status is {status}"
        )

    else:
        warnings.append(
            f"Trial is not currently recruiting: {status}"
        )

    # -------------------------
    # 5. Location matching
    # -------------------------
    patient_state = (patient.state or "").lower()
    patient_country = (patient.country or "").lower()

    location_match = False

    for location in trial.get("locations", []):
        trial_state = (location.get("state") or "").lower()
        trial_country = (location.get("country") or "").lower()

        if patient_state and patient_state == trial_state:
            score += 15
            reasons.append(
                "Trial has a location in the patient's state"
            )
            location_match = True
            break

        if patient_country and patient_country == trial_country:
            score += 5
            reasons.append(
                "Trial has a location in the patient's country"
            )
            location_match = True
            break

    if not location_match:
        warnings.append(
            "No nearby trial location match found"
        )

    # -------------------------
    # 6. NLP similarity
    # -------------------------
    nlp_score = calculate_text_similarity(
        patient,
        trial
    )

    if nlp_score >= 70:
        reasons.append(
            "Strong NLP similarity between patient profile and trial"
        )

    elif nlp_score >= 40:
        reasons.append(
            "Moderate NLP similarity between patient profile and trial"
        )

    else:
        warnings.append(
            "Low NLP similarity between patient profile and trial"
        )

    # -------------------------
    # 7. Final hybrid score
    # -------------------------

    # Prevent rule score from going above 100
    normalized_rule_score = min(score, 100)

    final_score = (
        normalized_rule_score * 0.70
        +
        nlp_score * 0.30
    )

    return {
        "rule_score": normalized_rule_score,
        "nlp_score": nlp_score,
        "score": round(final_score, 2),
        "reasons": reasons,
        "warnings": warnings
    }