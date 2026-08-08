import requests

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"


def search_trials(condition: str, page_size: int = 10):
    params = {
        "query.cond": condition,
        "pageSize": page_size,
        "format": "json"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()