from app.models.patient import Patient
from app.services.matcher import calculate_match_score


def test_matching_engine():
    patient = Patient(
        patient_id="TEST001",
        age=57,
        gender="Male",
        condition="Type 2 Diabetes",
        medications=["Metformin"],
        diagnoses=["Hypertension"],
        biomarkers=["HbA1c 8.2"],
        city="Orlando",
        state="Florida",
        country="United States"
    )

    trial = {
        "nct_id": "NCT00000001",
        "title": "Type 2 Diabetes Treatment Study",
        "minimum_age": "18 Years",
        "maximum_age": "70 Years",
        "sex": "ALL",
        "eligibility_criteria": (
            "Adults with Type 2 Diabetes may participate."
        ),
        "overall_status": "RECRUITING",
        "locations": [
            {
                "facility": "Test Medical Center",
                "city": "Orlando",
                "state": "Florida",
                "country": "United States"
            }
        ]
    }

    result = calculate_match_score(patient, trial)

    assert result["score"] >= 0
    assert result["score"] <= 100
    assert result["rule_score"] >= 0
    assert result["nlp_score"] >= 0

    assert isinstance(result["reasons"], list)
    assert isinstance(result["warnings"], list)
def test_patient_below_minimum_age():
    patient = Patient(
        patient_id="TEST002",
        age=15,
        gender="Male",
        condition="Type 2 Diabetes",
        medications=[],
        diagnoses=[],
        biomarkers=[],
        city="Orlando",
        state="Florida",
        country="United States"
    )

    trial = {
        "nct_id": "NCT00000002",
        "title": "Type 2 Diabetes Study",
        "minimum_age": "18 Years",
        "maximum_age": "70 Years",
        "sex": "ALL",
        "eligibility_criteria": "Adults with Type 2 Diabetes.",
        "overall_status": "RECRUITING",
        "locations": []
    }

    result = calculate_match_score(patient, trial)

    assert any(
        "below minimum age" in warning.lower()
        for warning in result["warnings"]
        
    )

def test_completed_trial_warning():
    patient = Patient(
        patient_id="TEST003",
        age=40,
        gender="Male",
        condition="Type 2 Diabetes"
    )

    trial = {
        "nct_id": "NCT00000003",
        "title": "Type 2 Diabetes Study",
        "minimum_age": "18 Years",
        "maximum_age": "65 Years",
        "sex": "ALL",
        "eligibility_criteria": "Adults with Type 2 Diabetes.",
        "overall_status": "COMPLETED",
        "locations": []
    }

    result = calculate_match_score(patient, trial)

    assert any(
        "not currently recruiting" in warning.lower()
        for warning in result["warnings"]
    )


def test_patient_at_minimum_age():
    patient = Patient(
        patient_id="TEST004",
        age=18,
        gender="Female",
        condition="Type 2 Diabetes"
    )

    trial = {
        "nct_id": "NCT00000004",
        "title": "Type 2 Diabetes Study",
        "minimum_age": "18 Years",
        "maximum_age": "65 Years",
        "sex": "ALL",
        "eligibility_criteria": "Adults with Type 2 Diabetes.",
        "overall_status": "RECRUITING",
        "locations": []
    }

    result = calculate_match_score(patient, trial)

    assert any(
        "meets trial age requirements" in reason.lower()
        for reason in result["reasons"]
    )

def test_missing_age_information():
    patient = Patient(
        patient_id="TEST006",
        age=35,
        gender="Male",
        condition="Type 2 Diabetes"
    )

    trial = {
        "nct_id": "NCT00000006",
        "title": "Type 2 Diabetes Study",
        "minimum_age": None,
        "maximum_age": None,
        "sex": "ALL",
        "eligibility_criteria": "Adults with Type 2 Diabetes.",
        "overall_status": "RECRUITING",
        "locations": []
    }

    result = calculate_match_score(patient, trial)

    assert any(
        "age eligibility information is unavailable"
        in warning.lower()
        for warning in result["warnings"]
    )

    assert not any(
        "meets trial age requirements" in reason.lower()
        for reason in result["reasons"]
    )