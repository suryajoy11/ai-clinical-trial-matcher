from app.services.clinical_trials import search_trials
from app.services.trial_parser import parse_trial


data = search_trials(
    "Type 2 Diabetes",
    page_size=5
)

studies = data.get("studies", [])

print(f"Trials found: {len(studies)}")
print()

for study in studies:
    trial = parse_trial(study)

    print("NCT ID:", trial["nct_id"])
    print("Title:", trial["title"])
    print("Status:", trial["overall_status"])
    print("Minimum Age:", trial["minimum_age"])
    print("Maximum Age:", trial["maximum_age"])
    print("Sex:", trial["sex"])
    print("Phase:", trial["phases"])
    print("-" * 70)