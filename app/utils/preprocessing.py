import re


def extract_age(age_string):
    if not age_string:
        return None

    match = re.search(r"\d+", age_string)

    if match:
        return int(match.group())

    return None