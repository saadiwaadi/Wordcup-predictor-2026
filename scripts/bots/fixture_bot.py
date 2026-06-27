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

def normalize_team_name(name):
    if not name:
        return ""
    name = name.strip()
    mapping = {
        "Korea Republic": "South Korea",
        "Côte d'Ivoire": "Ivory Coast",
        "Cabo Verde": "Cape Verde",
        "Cape Verde": "Cape Verde",
        "Türkiye": "Turkey",
        "IR Iran": "Iran",
        "Congo DR": "DR Congo",
        "United States": "USA",
        "Czechia": "Czech Republic",
        "Czech Republic": "Czech Republic",
        "Bosnia and Herzegovina": "Bosnia & Herzegovina",
        "Bosnia & Herzegovina": "Bosnia & Herzegovina",
    }
    return mapping.get(name, name)

def find_fifa_match(fixture, fifa_matches):
    # Try by kickoff date first since it's UTC and standardized
    kickoff = fixture.get("kickoff_utc")
    for m in fifa_matches:
        if m.get("Date") == kickoff:
            return m
            
    # Try by normalized home/away team names
    f_home = normalize_team_name(fixture.get("home_team")).lower()
    f_away = normalize_team_name(fixture.get("away_team")).lower()
    
    for m in fifa_matches:
        m_home_obj = m.get("Home") or {}
        m_away_obj = m.get("Away") or {}
        
        # ShortClubName
        m_home = normalize_team_name(m_home_obj.get("ShortClubName")).lower()
        m_away = normalize_team_name(m_away_obj.get("ShortClubName")).lower()
        
        if m_home == f_home and m_away == f_away:
            return m
            
        # Try abbreviations or TeamName locales if ShortClubName isn't set or doesn't match
        m_home_names = [t.get("Description", "").lower() for t in m_home_obj.get("TeamName", []) if t.get("Description")]
        m_away_names = [t.get("Description", "").lower() for t in m_away_obj.get("TeamName", []) if t.get("Description")]
        
        if (f_home in m_home_names or f_home == m_home_obj.get("Abbreviation", "").lower()) and \
           (f_away in m_away_names or f_away == m_away_obj.get("Abbreviation", "").lower()):
            return m
            
    return None

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
        
    # Fetch FIFA API matches for enrichment
    fifa_matches = []
    try:
        fifa_url = "https://api.fifa.com/api/v3/calendar/matches?idCompetition=17&idSeason=285023&count=104&language=en-GB"
        print(f"Fetching FIFA metadata from: {fifa_url}")
        fifa_headers = {
            "Accept": "application/json",
            "User-Agent": COMPETITION_CONFIG["user_agent"]
        }
        fifa_r = requests.get(fifa_url, headers=fifa_headers, timeout=15)
        if fifa_r.status_code == 200:
            fifa_matches = fifa_r.json().get("Results", [])
        else:
            print(f"Warning: FIFA API returned status code {fifa_r.status_code}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Failed to fetch FIFA match metadata: {e}", file=sys.stderr)
        
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
        
        fixture_item = {
            "match_id": match_id,
            "home_team": home,
            "away_team": away,
            "kickoff_utc": kickoff_utc,
            "stage": stage,
            "venue": venue,
            "result": result
        }

        # Try to find corresponding FIFA match
        fifa_match = find_fifa_match(fixture_item, fifa_matches)
        if fifa_match:
            # Weather
            weather = fifa_match.get("Weather") or {}
            
            # Stadium
            stadium_name = None
            stadium_obj = fifa_match.get("Stadium") or {}
            stadium_names = stadium_obj.get("Name") or []
            for n in stadium_names:
                if n.get("Locale") == "en-GB" or not stadium_name:
                    stadium_name = n.get("Description")
            
            venue = stadium_name if stadium_name else venue
            
            # Attendance
            attendance = fifa_match.get("Attendance")
            
            fixture_item["weather"] = weather
            fixture_item["venue"] = venue
            fixture_item["attendance"] = attendance

        fixtures.append(fixture_item)
        
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
