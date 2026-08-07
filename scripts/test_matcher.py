from app.models.patient import Patient
from app.services.clinical_trials import search_trials
from app.services.trial_parser import parse_trial
from app.services.matcher import calculate_match_score


patient = Patient(
    patient_id="P001",
    age=57,
    gender="Male",
    condition="Type 2 Diabetes",
    medications=["Metformin"],
    diagnoses=["Hypertension"],
    biomarkers=["HbA1c 8.2"],
    city="Orlando",
    state="Florida"
)


data = search_trials(
    patient.condition,
    page_size=10
)


results = []


for study in data.get("studies", []):
    trial = parse_trial(study)

    match = calculate_match_score(
        patient,
        trial
    )

    results.append({
        "nct_id": trial["nct_id"],
        "title": trial["title"],
        "score": match["score"],
        "reasons": match["reasons"]
    })


results.sort(
    key=lambda x: x["score"],
    reverse=True
)


for result in results:
    print("=" * 70)
    print("NCT ID:", result["nct_id"])
    print("Title:", result["title"])
    print("Score:", result["score"])

    print("Reasons:")

    for reason in result["reasons"]:
        print("-", reason)