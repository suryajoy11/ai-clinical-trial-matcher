
import re


def extract_age(age_string):
    """Convert a ClinicalTrials.gov age string to months."""
    if not age_string:
        return None

    match = re.fullmatch(
        r"\s*(\d+)\s*(years?|months?|weeks?|days?)\s*",
        age_string,
        flags=re.IGNORECASE
    )

    if not match:
        return None

    number = int(match.group(1))
    unit = match.group(2).lower()

    if unit.startswith("year"):
        return number * 12

    if unit.startswith("month"):
        return number

    if unit.startswith("week"):
        return number * 12 / 52.1775

    if unit.startswith("day"):
        return number * 12 / 365.2425

    return None