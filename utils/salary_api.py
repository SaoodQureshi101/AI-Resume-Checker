import requests

DATA_USA_URL = "https://datausa.io/api/data"

OCCUPATION_MAP = {
    "Data Analyst": "15-2051",
    "Junior Software Developer": "15-1252",
    "Network Technician": "15-1244",
    "Help Desk Technician": "15-1232",
    "CRM Administrator": "15-1241",
    "IT Support Specialist": "15-1232"
}


def fetch_average_wage(occupation, place="United States"):
    """Fetch average wage data for an occupation from Data USA."""
    code = OCCUPATION_MAP.get(occupation)
    if not code:
        return None

    params = {
        "Geography": place,
        "Year": "latest",
        "Occupation": code,
        "Measure": "Average Wage",
        "drilldowns": "Occupation,Geography",
        "required": "Occupation"
    }

    try:
        response = requests.get(DATA_USA_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        if not data:
            return None

        wage = data[0].get("Average Wage")
        if wage is not None:
            return float(wage)

    except Exception:
        return None

    return None
