def parse_trial(study):
    protocol = study.get("protocolSection", {})

    identification = protocol.get("identificationModule", {})
    eligibility = protocol.get("eligibilityModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    contacts = protocol.get("contactsLocationsModule", {})

    locations = contacts.get("locations", [])

    parsed_locations = []

    for location in locations:
        parsed_locations.append({
            "facility": location.get("facility"),
            "city": location.get("city"),
            "state": location.get("state"),
            "country": location.get("country")
        })

    return {
        "nct_id": identification.get("nctId"),
        "title": identification.get("briefTitle"),
        "minimum_age": eligibility.get("minimumAge"),
        "maximum_age": eligibility.get("maximumAge"),
        "sex": eligibility.get("sex"),
        "eligibility_criteria": eligibility.get("eligibilityCriteria"),
        "overall_status": status.get("overallStatus"),
        "phases": design.get("phases", []),
        "locations": parsed_locations
    }