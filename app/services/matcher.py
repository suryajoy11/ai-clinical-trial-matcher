from app.utils.preprocessing import extract_age


def calculate_match_score(patient, trial):
    score = 0
    reasons = []

    # Condition match
    if patient.condition.lower() in trial["title"].lower():
        score += 40
        reasons.append("Condition appears in trial title")

    # Gender match
    trial_sex = trial.get("sex")

    if trial_sex == "ALL":
        score += 20
        reasons.append("Trial accepts all sexes")

    elif trial_sex and patient.gender.upper() == trial_sex.upper():
        score += 20
        reasons.append("Patient sex matches trial eligibility")

    # Age match
    min_age = extract_age(trial.get("minimum_age"))
    max_age = extract_age(trial.get("maximum_age"))

    if min_age is None or patient.age >= min_age:
        score += 20
        reasons.append("Patient meets minimum age requirement")

    if max_age is None or patient.age <= max_age:
        score += 20
        reasons.append("Patient meets maximum age requirement")

    return {
        "score": score,
        "reasons": reasons
    }