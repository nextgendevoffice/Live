import requests
from datetime import date

BASE_URL = "https://api.football-data.org/v2"
HEADERS = {
    "X-Auth-Token": "886eb5facd814d229f3ab17c41323a0d"  # Replace with your API key
}

def get_today_matches(league_code):
    today = date.today().strftime("%Y-%m-%d")
    endpoint = f"{BASE_URL}/matches?competitions={league_code}&dateFrom={today}&dateTo={today}"
    response = requests.get(endpoint, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {"matches": []}

def get_league_table(league_code):
    endpoint = f"{BASE_URL}/competitions/{league_code}/standings"
    response = requests.get(endpoint, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {"standings": []}

def get_leagues():
    endpoint = f"{BASE_URL}/competitions"
    response = requests.get(endpoint, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return {"competitions": []}
