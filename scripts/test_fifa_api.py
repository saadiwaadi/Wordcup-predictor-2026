import requests
import json

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
url = "https://api.fifa.com/api/v3/calendar/matches?idCompetition=17&idSeason=285023&count=104&language=en-GB"

try:
    r = requests.get(url, headers=headers)
    print("Status:", r.status_code)
    data = r.json()
    print("Total matches:", len(data.get("Results", [])))
    if data.get("Results"):
        print("Sample Match:", json.dumps(data["Results"][0], indent=2)[:2000])
except Exception as e:
    print("Error:", e)
