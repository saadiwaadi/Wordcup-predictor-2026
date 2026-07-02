# pragma: no mutate start
import os
import re
from datetime import datetime, timezone

# Base directory setup relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "public", "data", "scraped")

COMPETITION_CONFIG = {
    "competition_name": "FIFA World Cup 2026",
    "year": 2026,
    "openfootball_url": "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2026/worldcup.json",
    "fixtures_path": os.path.join(DATA_DIR, "fixtures.json"),
    "injuries_path": os.path.join(DATA_DIR, "injuries.json"),
    "squads_path": os.path.join(DATA_DIR, "squads.json"),
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

_MAPPING = {
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

_MAPPING_LOWER = {k.lower(): v for k, v in _MAPPING.items()}

def normalize_team_name(name):
    if not name:
        return ""
    name = name.strip()
    return _MAPPING_LOWER.get(name.lower(), name)

def is_placeholder(name):
    if not name:
        return True
    return bool(re.match(r'^[WL]\d+', name))
# pragma: no mutate end

TEAM_CODE_MAP = {
    "brazil": "BRA", "france": "FRA", "england": "ENG", "germany": "GER", "spain": "ESP",
    "argentina": "ARG", "portugal": "POR", "netherlands": "NED", "belgium": "BEL", "croatia": "CRO",
    "senegal": "SEN", "morocco": "MAR", "japan": "JPN", "united states": "USA", "usa": "USA",
    "mexico": "MEX", "canada": "CAN", "colombia": "COL", "uruguay": "URU", "switzerland": "SUI",
    "serbia": "SRB", "denmark": "DEN", "austria": "AUT", "turkey": "TUR", "south korea": "KOR",
    "poland": "POL", "australia": "AUS", "iran": "IRN", "ecuador": "ECU", "nigeria": "NGR",
    "ghana": "GHA", "cameroon": "CMR", "egypt": "EGY", "algeria": "ALG", "ivory coast": "CIV",
    "saudi arabia": "SAU", "qatar": "QAT", "costa rica": "CRI", "panama": "PAN", "venezuela": "VEN",
    "chile": "CHI", "romania": "ROU", "ukraine": "UKR", "south africa": "RSA", "czech republic": "CZE",
    "paraguay": "PAR", "scotland": "SCO", "sweden": "SWE", "tunisia": "TUN", "dr congo": "COD",
    "bosnia & herzegovina": "BIH", "cape verde": "CPV", "haiti": "HAI", "iraq": "IRQ",
    "norway": "NOR", "jordan": "JOR", "uzbekistan": "UZB", "curacao": "CUW", "curaçao": "CUW",
    "bosnia and herzegovina": "BIH", "côte d'ivoire": "CIV", "cabo verde": "CPV", "türkiye": "TUR",
    "ir iran": "IRN", "congo dr": "COD", "czechia": "CZE", "turkiye": "TUR"
}

def get_team_code(name):
    if not name:
        return None
    name_norm = normalize_team_name(name).lower()
    return TEAM_CODE_MAP.get(name_norm)


def get_match_outcome(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "et" in result:
        scores = result["et"]
    else:
        scores = result.get("ft")
    if not scores or len(scores) < 2:
        return None
    home_score, away_score = scores[0], scores[1]
    if home_score == away_score:
        return "draw"
        
    team_norm = normalize_team_name(team).lower()
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None

def is_confirmed_eliminated(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).lower() if a else ""
            if h_norm == team_name_norm or a_norm == team_name_norm:
                team_completed.append(f)
                
    if not team_completed:
        return False
        
    team_completed.sort(key=lambda x: x.get("kickoff_utc", ""))
    last_match = team_completed[-1]
    stage = last_match.get("stage", "")
    
    if "Matchday" not in stage:
        outcome = get_match_outcome(team_name, last_match)
        if outcome == "loss":
            return True
        return False
    else:
        has_unplayed_group = False
        for f in fixtures:
            if "Matchday" in f.get("stage", "") and f.get("result") is None:
                has_unplayed_group = True
                break
        if has_unplayed_group:
            return False
            
        in_knockout = False
        for f in fixtures:
            if "Matchday" not in f.get("stage", ""):
                h = f.get("home_team")
                a = f.get("away_team")
                h_norm = normalize_team_name(h).lower() if h else ""
                a_norm = normalize_team_name(a).lower() if a else ""
                if h_norm == team_name_norm or a_norm == team_name_norm:
                    in_knockout = True
                    break
        if in_knockout:
            return False
            
        bracket_resolution_started = False
        for f in fixtures:
            if "Matchday" not in f.get("stage", ""):
                h = f.get("home_team")
                a = f.get("away_team")
                if h and not is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def resolve_team_statuses(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(normalize_team_name(a))
            
        kickoff_str = fixture.get("kickoff_utc")
        if not kickoff_str:
            continue
        try:
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("Z", "+00:00"))
        except Exception:
            continue
            
        is_completed = fixture.get("result") is not None
        if kickoff_dt >= now_dt and not is_completed:
            if h and not is_placeholder(h):
                normally_active.add(normalize_team_name(h))
            if a and not is_placeholder(a):
                normally_active.add(normalize_team_name(a))
                
    gap_window = set()
    skipped = set()
    for team in all_teams:
        if team not in normally_active:
            if not is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

