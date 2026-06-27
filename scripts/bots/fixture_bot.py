import os
import sys
import json
import hashlib
import requests
from datetime import datetime, timedelta, timezone

# Add parent directory to path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import COMPETITION_CONFIG

def parse_kickoff_utc(date_str, time_str):
    if not time_str:
        return f"{date_str}T00:00:00Z"
    try:
        parts = time_str.split(" ")
        time_part = parts[0]
        offset_hours = 0
        if len(parts) > 1:
            tz_part = parts[1]
            if "UTC" in tz_part:
                offset_str = tz_part.replace("UTC", "").strip()
                if offset_str:
                    offset_hours = int(offset_str)
                    
        dt = datetime.strptime(f"{date_str} {time_part}", "%Y-%m-%d %H:%M")
        dt = dt.replace(tzinfo=timezone.utc)
        dt = dt - timedelta(hours=offset_hours)
        return dt.isoformat().replace("+00:00", "Z")
    except Exception:
        # Fallback if parsing fails
        return f"{date_str}T{time_str}"

def generate_match_id(home, away, date):
    unique_str = f"{home.lower()}_vs_{away.lower()}_{date}"
    return hashlib.md5(unique_str.encode('utf-8')).hexdigest()[:12]

def fetch_and_normalize_fixtures():
    url = COMPETITION_CONFIG["openfootball_url"]
    headers = {"User-Agent": COMPETITION_CONFIG["user_agent"]}
    
    print(f"Fetching fixtures from: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Error: Server returned status code {r.status_code}", file=sys.stderr)
            sys.exit(1)
        data = r.json()
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
        
    matches = data.get("matches", [])
    if not matches:
        print("Error: No matches found in JSON response", file=sys.stderr)
        sys.exit(1)
        
    fixtures = []
    for m in matches:
        stage = m.get("round", "Unknown Stage")
        home = m.get("team1")
        away = m.get("team2")
        date_str = m.get("date")
        time_str = m.get("time", "")
        
        if not home or not away or not date_str:
            continue
            
        match_id = generate_match_id(home, away, date_str)
        kickoff_utc = parse_kickoff_utc(date_str, time_str)
        
        # Extract venue details (uses 'ground' in the openfootball schema)
        venue = m.get("ground", "Unknown Venue")
        result = m.get("score") if "score" in m else None
        
        fixtures.append({
            "match_id": match_id,
            "home_team": home,
            "away_team": away,
            "kickoff_utc": kickoff_utc,
            "stage": stage,
            "venue": venue,
            "result": result
        })
        
    # Sort fixtures chronologically
    fixtures.sort(key=lambda x: x["kickoff_utc"])
    
    output_path = COMPETITION_CONFIG["fixtures_path"]
    existing_fixtures = []
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_fixtures = json.load(f)
        except Exception:
            pass
            
    if existing_fixtures != fixtures:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(fixtures, f, indent=2, ensure_ascii=False)
        print(f"updated: {len(fixtures)} matches")
    else:
        print("no changes detected")

if __name__ == "__main__":
    fetch_and_normalize_fixtures()
