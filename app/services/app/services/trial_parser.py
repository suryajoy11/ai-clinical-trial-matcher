def parse_trial(study):
    protocol = study.get("protocolSection", {})

    identification = protocol.get("identificationModule", {})
    eligibility = protocol.get("eligibilityModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})

    return {
        "nct_id": identification.get("nctId"),
        "title": identification.get("briefTitle"),
        "minimum_age": eligibility.get("minimumAge"),
        "maximum_age": eligibility.get("maximumAge"),
        "sex": eligibility.get("sex"),
        "eligibility_criteria": eligibility.get("eligibilityCriteria"),
        "overall_status": status.get("overallStatus"),
        "phases": design.get("phases", []),
    }