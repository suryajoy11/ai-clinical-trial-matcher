
from fastapi.testclient import TestClient

from app.main import app
from app.api import matching


client = TestClient(app)


def test_match_patient_api(monkeypatch):
    # Use synthetic trial data instead of calling ClinicalTrials.gov.
    fake_trial = {
        "nct_id": "NCT00000001",
        "title": "Type 2 Diabetes Treatment Study",
        "minimum_age": "18 Years",
        "maximum_age": "70 Years",
        "sex": "ALL",
        "eligibility_criteria": "Adults with Type 2 Diabetes.",
        "overall_status": "RECRUITING",
        "locations": [
            {
                "city": "Orlando",
                "state": "Florida",
                "country": "United States"
            }
        ]
    }

    # Replace the external API call with a local test response.
    monkeypatch.setattr(
        matching,
        "search_trials",
        lambda condition, page_size=10: {
            "studies": [{"fake": "study"}]
        }
    )

    # Replace the parser so it returns our synthetic trial.
    monkeypatch.setattr(
        matching,
        "parse_trial",
        lambda study: fake_trial
    )

    patient = {
        "patient_id": "TEST_API_001",
        "age": 57,
        "gender": "Male",
        "condition": "Type 2 Diabetes",
        "medications": ["Metformin"],
        "diagnoses": ["Hypertension"],
        "biomarkers": ["HbA1c 8.2"],
        "city": "Orlando",
        "state": "Florida",
        "country": "United States"
    }

    response = client.post("/match/", json=patient)

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["patient_id"] == "TEST_API_001"
    assert data["condition"] == "Type 2 Diabetes"
    assert data["trials_found"] == 1
    assert len(data["matches"]) == 1

    trial = data["matches"][0]

    assert trial["nct_id"] == "NCT00000001"
    assert isinstance(trial["rule_score"], (int, float))
    assert isinstance(trial["nlp_score"], (int, float))
    assert isinstance(trial["score"], (int, float))
    assert isinstance(trial["reasons"], list)
    assert isinstance(trial["warnings"], list)

def test_completed_trials_are_excluded(monkeypatch):
    fake_studies = [
        {"status": "COMPLETED"},
        {"status": "RECRUITING"}
    ]

    def fake_search(condition, page_size=10):
        return {"studies": fake_studies}

    def fake_parser(study):
        return {
            "nct_id": "NCT00000001",
            "title": "Type 2 Diabetes Study",
            "minimum_age": "18 Years",
            "maximum_age": "70 Years",
            "sex": "ALL",
            "eligibility_criteria": "Adults with Type 2 Diabetes.",
            "overall_status": study["status"],
            "locations": []
        }

    monkeypatch.setattr(matching, "search_trials", fake_search)
    monkeypatch.setattr(matching, "parse_trial", fake_parser)

    patient = {
        "patient_id": "TEST005",
        "age": 40,
        "gender": "Male",
        "condition": "Type 2 Diabetes"
    }

    response = client.post("/match/", json=patient)

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["trials_found"] == 1
    assert len(data["matches"]) == 1
    assert data["matches"][0]["status"] == "RECRUITING"