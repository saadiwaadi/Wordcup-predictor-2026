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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict

def normalize_team_name(name):
    if not name:
        return ""
    name = name.strip()
    return _MAPPING_LOWER.get(name.lower(), name)

def is_placeholder(name):
    if not name:
        return True
    return bool(re.match(r'^[WL]\d+', name))
mutants_x_get_match_outcome__mutmut: MutantDict = {}  # type: ignore
# pragma: no mutate end

@_mutmut_mutated(mutants_x_get_match_outcome__mutmut)
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_orig(team, match):
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_1(team, match):
    result = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_2(team, match):
    result = match.get(None)
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_3(team, match):
    result = match.get("XXresultXX")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_4(team, match):
    result = match.get("RESULT")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_5(team, match):
    result = match.get("result")
    if result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_6(team, match):
    result = match.get("result")
    if not result:
        return None
    home = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_7(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get(None)
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_8(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("XXhome_teamXX")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_9(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("HOME_TEAM")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_10(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_11(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get(None)
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_12(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("XXaway_teamXX")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_13(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("AWAY_TEAM")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_14(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "XXpXX" in result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_15(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "P" in result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_16(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" not in result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_17(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_18(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["XXpXX"]
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_19(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["P"]
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_20(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "XXetXX" in result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_21(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "ET" in result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_22(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "et" not in result:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_23(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "et" in result:
        scores = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_24(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "et" in result:
        scores = result["XXetXX"]
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_25(team, match):
    result = match.get("result")
    if not result:
        return None
    home = match.get("home_team")
    away = match.get("away_team")
    if "p" in result:
        scores = result["p"]
    elif "et" in result:
        scores = result["ET"]
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_26(team, match):
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
        scores = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_27(team, match):
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
        scores = result.get(None)
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_28(team, match):
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
        scores = result.get("XXftXX")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_29(team, match):
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
        scores = result.get("FT")
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_30(team, match):
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
    if not scores and len(scores) < 2:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_31(team, match):
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
    if scores or len(scores) < 2:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_32(team, match):
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
    if not scores or len(scores) <= 2:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_33(team, match):
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
    if not scores or len(scores) < 3:
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_34(team, match):
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
    home_score, away_score = None
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_35(team, match):
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
    home_score, away_score = scores[1], scores[1]
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_36(team, match):
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
    home_score, away_score = scores[0], scores[2]
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
# pragma: no mutate end

def x_get_match_outcome__mutmut_37(team, match):
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
    if home_score != away_score:
        return "draw"
        
    team_norm = normalize_team_name(team).lower()
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_38(team, match):
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
        return "XXdrawXX"
        
    team_norm = normalize_team_name(team).lower()
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_39(team, match):
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
        return "DRAW"
        
    team_norm = normalize_team_name(team).lower()
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_40(team, match):
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
        
    team_norm = None
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_41(team, match):
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
        
    team_norm = normalize_team_name(team).upper()
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_42(team, match):
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
        
    team_norm = normalize_team_name(None).lower()
    home_norm = normalize_team_name(home).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_43(team, match):
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
    home_norm = None
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_44(team, match):
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
    home_norm = normalize_team_name(home).upper() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_45(team, match):
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
    home_norm = normalize_team_name(None).lower() if home else ""
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_46(team, match):
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
    home_norm = normalize_team_name(home).lower() if home else "XXXX"
    away_norm = normalize_team_name(away).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_47(team, match):
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
    away_norm = None
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_48(team, match):
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
    away_norm = normalize_team_name(away).upper() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_49(team, match):
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
    away_norm = normalize_team_name(None).lower() if away else ""
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_50(team, match):
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
    away_norm = normalize_team_name(away).lower() if away else "XXXX"
    
    if team_norm == home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_51(team, match):
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
    
    if team_norm != home_norm:
        return "win" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_52(team, match):
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
        return "XXwinXX" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_53(team, match):
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
        return "WIN" if home_score > away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_54(team, match):
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
        return "win" if home_score >= away_score else "loss"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_55(team, match):
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
        return "win" if home_score > away_score else "XXlossXX"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_56(team, match):
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
        return "win" if home_score > away_score else "LOSS"
    elif team_norm == away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_57(team, match):
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
    elif team_norm != away_norm:
        return "win" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_58(team, match):
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
        return "XXwinXX" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_59(team, match):
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
        return "WIN" if away_score > home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_60(team, match):
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
        return "win" if away_score >= home_score else "loss"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_61(team, match):
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
        return "win" if away_score > home_score else "XXlossXX"
    return None
# pragma: no mutate end

def x_get_match_outcome__mutmut_62(team, match):
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
        return "win" if away_score > home_score else "LOSS"
    return None

mutants_x_get_match_outcome__mutmut['_mutmut_orig'] = x_get_match_outcome__mutmut_orig # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_1'] = x_get_match_outcome__mutmut_1 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_2'] = x_get_match_outcome__mutmut_2 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_3'] = x_get_match_outcome__mutmut_3 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_4'] = x_get_match_outcome__mutmut_4 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_5'] = x_get_match_outcome__mutmut_5 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_6'] = x_get_match_outcome__mutmut_6 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_7'] = x_get_match_outcome__mutmut_7 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_8'] = x_get_match_outcome__mutmut_8 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_9'] = x_get_match_outcome__mutmut_9 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_10'] = x_get_match_outcome__mutmut_10 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_11'] = x_get_match_outcome__mutmut_11 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_12'] = x_get_match_outcome__mutmut_12 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_13'] = x_get_match_outcome__mutmut_13 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_14'] = x_get_match_outcome__mutmut_14 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_15'] = x_get_match_outcome__mutmut_15 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_16'] = x_get_match_outcome__mutmut_16 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_17'] = x_get_match_outcome__mutmut_17 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_18'] = x_get_match_outcome__mutmut_18 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_19'] = x_get_match_outcome__mutmut_19 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_20'] = x_get_match_outcome__mutmut_20 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_21'] = x_get_match_outcome__mutmut_21 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_22'] = x_get_match_outcome__mutmut_22 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_23'] = x_get_match_outcome__mutmut_23 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_24'] = x_get_match_outcome__mutmut_24 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_25'] = x_get_match_outcome__mutmut_25 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_26'] = x_get_match_outcome__mutmut_26 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_27'] = x_get_match_outcome__mutmut_27 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_28'] = x_get_match_outcome__mutmut_28 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_29'] = x_get_match_outcome__mutmut_29 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_30'] = x_get_match_outcome__mutmut_30 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_31'] = x_get_match_outcome__mutmut_31 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_32'] = x_get_match_outcome__mutmut_32 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_33'] = x_get_match_outcome__mutmut_33 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_34'] = x_get_match_outcome__mutmut_34 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_35'] = x_get_match_outcome__mutmut_35 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_36'] = x_get_match_outcome__mutmut_36 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_37'] = x_get_match_outcome__mutmut_37 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_38'] = x_get_match_outcome__mutmut_38 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_39'] = x_get_match_outcome__mutmut_39 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_40'] = x_get_match_outcome__mutmut_40 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_41'] = x_get_match_outcome__mutmut_41 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_42'] = x_get_match_outcome__mutmut_42 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_43'] = x_get_match_outcome__mutmut_43 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_44'] = x_get_match_outcome__mutmut_44 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_45'] = x_get_match_outcome__mutmut_45 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_46'] = x_get_match_outcome__mutmut_46 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_47'] = x_get_match_outcome__mutmut_47 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_48'] = x_get_match_outcome__mutmut_48 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_49'] = x_get_match_outcome__mutmut_49 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_50'] = x_get_match_outcome__mutmut_50 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_51'] = x_get_match_outcome__mutmut_51 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_52'] = x_get_match_outcome__mutmut_52 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_53'] = x_get_match_outcome__mutmut_53 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_54'] = x_get_match_outcome__mutmut_54 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_55'] = x_get_match_outcome__mutmut_55 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_56'] = x_get_match_outcome__mutmut_56 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_57'] = x_get_match_outcome__mutmut_57 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_58'] = x_get_match_outcome__mutmut_58 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_59'] = x_get_match_outcome__mutmut_59 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_60'] = x_get_match_outcome__mutmut_60 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_61'] = x_get_match_outcome__mutmut_61 # type: ignore # mutmut generated
mutants_x_get_match_outcome__mutmut['x_get_match_outcome__mutmut_62'] = x_get_match_outcome__mutmut_62 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut: MutantDict = {}  # type: ignore

@_mutmut_mutated(mutants_x_is_confirmed_eliminated__mutmut)
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

def x_is_confirmed_eliminated__mutmut_orig(team_name, fixtures):
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

def x_is_confirmed_eliminated__mutmut_1(team_name, fixtures):
    team_name_norm = None
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

def x_is_confirmed_eliminated__mutmut_2(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).upper()
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

def x_is_confirmed_eliminated__mutmut_3(team_name, fixtures):
    team_name_norm = normalize_team_name(None).lower()
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

def x_is_confirmed_eliminated__mutmut_4(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = None
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

def x_is_confirmed_eliminated__mutmut_5(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get(None) is not None:
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

def x_is_confirmed_eliminated__mutmut_6(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("XXresultXX") is not None:
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

def x_is_confirmed_eliminated__mutmut_7(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("RESULT") is not None:
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

def x_is_confirmed_eliminated__mutmut_8(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_9(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = None
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

def x_is_confirmed_eliminated__mutmut_10(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get(None)
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

def x_is_confirmed_eliminated__mutmut_11(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("XXhome_teamXX")
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

def x_is_confirmed_eliminated__mutmut_12(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("HOME_TEAM")
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

def x_is_confirmed_eliminated__mutmut_13(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = None
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

def x_is_confirmed_eliminated__mutmut_14(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get(None)
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

def x_is_confirmed_eliminated__mutmut_15(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("XXaway_teamXX")
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

def x_is_confirmed_eliminated__mutmut_16(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("AWAY_TEAM")
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

def x_is_confirmed_eliminated__mutmut_17(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = None
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

def x_is_confirmed_eliminated__mutmut_18(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).upper() if h else ""
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

def x_is_confirmed_eliminated__mutmut_19(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(None).lower() if h else ""
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

def x_is_confirmed_eliminated__mutmut_20(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else "XXXX"
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

def x_is_confirmed_eliminated__mutmut_21(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = None
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

def x_is_confirmed_eliminated__mutmut_22(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).upper() if a else ""
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

def x_is_confirmed_eliminated__mutmut_23(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(None).lower() if a else ""
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

def x_is_confirmed_eliminated__mutmut_24(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).lower() if a else "XXXX"
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

def x_is_confirmed_eliminated__mutmut_25(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).lower() if a else ""
            if h_norm == team_name_norm and a_norm == team_name_norm:
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

def x_is_confirmed_eliminated__mutmut_26(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).lower() if a else ""
            if h_norm != team_name_norm or a_norm == team_name_norm:
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

def x_is_confirmed_eliminated__mutmut_27(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).lower() if a else ""
            if h_norm == team_name_norm or a_norm != team_name_norm:
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

def x_is_confirmed_eliminated__mutmut_28(team_name, fixtures):
    team_name_norm = normalize_team_name(team_name).lower()
    team_completed = []
    for f in fixtures:
        if f.get("result") is not None:
            h = f.get("home_team")
            a = f.get("away_team")
            h_norm = normalize_team_name(h).lower() if h else ""
            a_norm = normalize_team_name(a).lower() if a else ""
            if h_norm == team_name_norm or a_norm == team_name_norm:
                team_completed.append(None)
                
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

def x_is_confirmed_eliminated__mutmut_29(team_name, fixtures):
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
                
    if team_completed:
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

def x_is_confirmed_eliminated__mutmut_30(team_name, fixtures):
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
        return True
        
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

def x_is_confirmed_eliminated__mutmut_31(team_name, fixtures):
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
        
    team_completed.sort(key=None)
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

def x_is_confirmed_eliminated__mutmut_32(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: None)
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

def x_is_confirmed_eliminated__mutmut_33(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get(None, ""))
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

def x_is_confirmed_eliminated__mutmut_34(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get("kickoff_utc", None))
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

def x_is_confirmed_eliminated__mutmut_35(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get(""))
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

def x_is_confirmed_eliminated__mutmut_36(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get("kickoff_utc", ))
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

def x_is_confirmed_eliminated__mutmut_37(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get("XXkickoff_utcXX", ""))
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

def x_is_confirmed_eliminated__mutmut_38(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get("KICKOFF_UTC", ""))
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

def x_is_confirmed_eliminated__mutmut_39(team_name, fixtures):
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
        
    team_completed.sort(key=lambda x: x.get("kickoff_utc", "XXXX"))
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

def x_is_confirmed_eliminated__mutmut_40(team_name, fixtures):
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
    last_match = None
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

def x_is_confirmed_eliminated__mutmut_41(team_name, fixtures):
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
    last_match = team_completed[+1]
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

def x_is_confirmed_eliminated__mutmut_42(team_name, fixtures):
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
    last_match = team_completed[-2]
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

def x_is_confirmed_eliminated__mutmut_43(team_name, fixtures):
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
    stage = None
    
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

def x_is_confirmed_eliminated__mutmut_44(team_name, fixtures):
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
    stage = last_match.get(None, "")
    
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

def x_is_confirmed_eliminated__mutmut_45(team_name, fixtures):
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
    stage = last_match.get("stage", None)
    
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

def x_is_confirmed_eliminated__mutmut_46(team_name, fixtures):
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
    stage = last_match.get("")
    
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

def x_is_confirmed_eliminated__mutmut_47(team_name, fixtures):
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
    stage = last_match.get("stage", )
    
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

def x_is_confirmed_eliminated__mutmut_48(team_name, fixtures):
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
    stage = last_match.get("XXstageXX", "")
    
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

def x_is_confirmed_eliminated__mutmut_49(team_name, fixtures):
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
    stage = last_match.get("STAGE", "")
    
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

def x_is_confirmed_eliminated__mutmut_50(team_name, fixtures):
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
    stage = last_match.get("stage", "XXXX")
    
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

def x_is_confirmed_eliminated__mutmut_51(team_name, fixtures):
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
    
    if "XXMatchdayXX" not in stage:
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

def x_is_confirmed_eliminated__mutmut_52(team_name, fixtures):
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
    
    if "matchday" not in stage:
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

def x_is_confirmed_eliminated__mutmut_53(team_name, fixtures):
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
    
    if "MATCHDAY" not in stage:
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

def x_is_confirmed_eliminated__mutmut_54(team_name, fixtures):
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
    
    if "Matchday" in stage:
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

def x_is_confirmed_eliminated__mutmut_55(team_name, fixtures):
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
        outcome = None
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

def x_is_confirmed_eliminated__mutmut_56(team_name, fixtures):
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
        outcome = get_match_outcome(None, last_match)
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

def x_is_confirmed_eliminated__mutmut_57(team_name, fixtures):
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
        outcome = get_match_outcome(team_name, None)
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

def x_is_confirmed_eliminated__mutmut_58(team_name, fixtures):
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
        outcome = get_match_outcome(last_match)
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

def x_is_confirmed_eliminated__mutmut_59(team_name, fixtures):
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
        outcome = get_match_outcome(team_name, )
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

def x_is_confirmed_eliminated__mutmut_60(team_name, fixtures):
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
        if outcome != "loss":
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

def x_is_confirmed_eliminated__mutmut_61(team_name, fixtures):
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
        if outcome == "XXlossXX":
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

def x_is_confirmed_eliminated__mutmut_62(team_name, fixtures):
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
        if outcome == "LOSS":
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

def x_is_confirmed_eliminated__mutmut_63(team_name, fixtures):
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
            return False
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

def x_is_confirmed_eliminated__mutmut_64(team_name, fixtures):
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
        return True
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

def x_is_confirmed_eliminated__mutmut_65(team_name, fixtures):
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
        has_unplayed_group = None
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

def x_is_confirmed_eliminated__mutmut_66(team_name, fixtures):
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
        has_unplayed_group = True
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

def x_is_confirmed_eliminated__mutmut_67(team_name, fixtures):
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
            if "Matchday" in f.get("stage", "") or f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_68(team_name, fixtures):
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
            if "XXMatchdayXX" in f.get("stage", "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_69(team_name, fixtures):
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
            if "matchday" in f.get("stage", "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_70(team_name, fixtures):
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
            if "MATCHDAY" in f.get("stage", "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_71(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_72(team_name, fixtures):
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
            if "Matchday" in f.get(None, "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_73(team_name, fixtures):
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
            if "Matchday" in f.get("stage", None) and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_74(team_name, fixtures):
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
            if "Matchday" in f.get("") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_75(team_name, fixtures):
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
            if "Matchday" in f.get("stage", ) and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_76(team_name, fixtures):
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
            if "Matchday" in f.get("XXstageXX", "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_77(team_name, fixtures):
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
            if "Matchday" in f.get("STAGE", "") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_78(team_name, fixtures):
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
            if "Matchday" in f.get("stage", "XXXX") and f.get("result") is None:
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

def x_is_confirmed_eliminated__mutmut_79(team_name, fixtures):
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
            if "Matchday" in f.get("stage", "") and f.get(None) is None:
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

def x_is_confirmed_eliminated__mutmut_80(team_name, fixtures):
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
            if "Matchday" in f.get("stage", "") and f.get("XXresultXX") is None:
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

def x_is_confirmed_eliminated__mutmut_81(team_name, fixtures):
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
            if "Matchday" in f.get("stage", "") and f.get("RESULT") is None:
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

def x_is_confirmed_eliminated__mutmut_82(team_name, fixtures):
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
            if "Matchday" in f.get("stage", "") and f.get("result") is not None:
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

def x_is_confirmed_eliminated__mutmut_83(team_name, fixtures):
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
                has_unplayed_group = None
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

def x_is_confirmed_eliminated__mutmut_84(team_name, fixtures):
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
                has_unplayed_group = False
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

def x_is_confirmed_eliminated__mutmut_85(team_name, fixtures):
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
                return
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

def x_is_confirmed_eliminated__mutmut_86(team_name, fixtures):
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
            return True
            
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

def x_is_confirmed_eliminated__mutmut_87(team_name, fixtures):
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
            
        in_knockout = None
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

def x_is_confirmed_eliminated__mutmut_88(team_name, fixtures):
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
            
        in_knockout = True
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

def x_is_confirmed_eliminated__mutmut_89(team_name, fixtures):
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
            if "XXMatchdayXX" not in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_90(team_name, fixtures):
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
            if "matchday" not in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_91(team_name, fixtures):
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
            if "MATCHDAY" not in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_92(team_name, fixtures):
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
            if "Matchday" in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_93(team_name, fixtures):
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
            if "Matchday" not in f.get(None, ""):
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

def x_is_confirmed_eliminated__mutmut_94(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", None):
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

def x_is_confirmed_eliminated__mutmut_95(team_name, fixtures):
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
            if "Matchday" not in f.get(""):
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

def x_is_confirmed_eliminated__mutmut_96(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", ):
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

def x_is_confirmed_eliminated__mutmut_97(team_name, fixtures):
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
            if "Matchday" not in f.get("XXstageXX", ""):
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

def x_is_confirmed_eliminated__mutmut_98(team_name, fixtures):
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
            if "Matchday" not in f.get("STAGE", ""):
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

def x_is_confirmed_eliminated__mutmut_99(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", "XXXX"):
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

def x_is_confirmed_eliminated__mutmut_100(team_name, fixtures):
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
                h = None
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

def x_is_confirmed_eliminated__mutmut_101(team_name, fixtures):
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
                h = f.get(None)
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

def x_is_confirmed_eliminated__mutmut_102(team_name, fixtures):
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
                h = f.get("XXhome_teamXX")
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

def x_is_confirmed_eliminated__mutmut_103(team_name, fixtures):
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
                h = f.get("HOME_TEAM")
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

def x_is_confirmed_eliminated__mutmut_104(team_name, fixtures):
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
                a = None
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

def x_is_confirmed_eliminated__mutmut_105(team_name, fixtures):
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
                a = f.get(None)
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

def x_is_confirmed_eliminated__mutmut_106(team_name, fixtures):
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
                a = f.get("XXaway_teamXX")
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

def x_is_confirmed_eliminated__mutmut_107(team_name, fixtures):
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
                a = f.get("AWAY_TEAM")
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

def x_is_confirmed_eliminated__mutmut_108(team_name, fixtures):
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
                h_norm = None
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

def x_is_confirmed_eliminated__mutmut_109(team_name, fixtures):
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
                h_norm = normalize_team_name(h).upper() if h else ""
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

def x_is_confirmed_eliminated__mutmut_110(team_name, fixtures):
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
                h_norm = normalize_team_name(None).lower() if h else ""
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

def x_is_confirmed_eliminated__mutmut_111(team_name, fixtures):
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
                h_norm = normalize_team_name(h).lower() if h else "XXXX"
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

def x_is_confirmed_eliminated__mutmut_112(team_name, fixtures):
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
                a_norm = None
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

def x_is_confirmed_eliminated__mutmut_113(team_name, fixtures):
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
                a_norm = normalize_team_name(a).upper() if a else ""
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

def x_is_confirmed_eliminated__mutmut_114(team_name, fixtures):
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
                a_norm = normalize_team_name(None).lower() if a else ""
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

def x_is_confirmed_eliminated__mutmut_115(team_name, fixtures):
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
                a_norm = normalize_team_name(a).lower() if a else "XXXX"
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

def x_is_confirmed_eliminated__mutmut_116(team_name, fixtures):
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
                if h_norm == team_name_norm and a_norm == team_name_norm:
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

def x_is_confirmed_eliminated__mutmut_117(team_name, fixtures):
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
                if h_norm != team_name_norm or a_norm == team_name_norm:
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

def x_is_confirmed_eliminated__mutmut_118(team_name, fixtures):
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
                if h_norm == team_name_norm or a_norm != team_name_norm:
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

def x_is_confirmed_eliminated__mutmut_119(team_name, fixtures):
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
                    in_knockout = None
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

def x_is_confirmed_eliminated__mutmut_120(team_name, fixtures):
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
                    in_knockout = False
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

def x_is_confirmed_eliminated__mutmut_121(team_name, fixtures):
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
                    return
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

def x_is_confirmed_eliminated__mutmut_122(team_name, fixtures):
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
            return True
            
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

def x_is_confirmed_eliminated__mutmut_123(team_name, fixtures):
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
            
        bracket_resolution_started = None
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

def x_is_confirmed_eliminated__mutmut_124(team_name, fixtures):
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
            
        bracket_resolution_started = True
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

def x_is_confirmed_eliminated__mutmut_125(team_name, fixtures):
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
            if "XXMatchdayXX" not in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_126(team_name, fixtures):
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
            if "matchday" not in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_127(team_name, fixtures):
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
            if "MATCHDAY" not in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_128(team_name, fixtures):
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
            if "Matchday" in f.get("stage", ""):
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

def x_is_confirmed_eliminated__mutmut_129(team_name, fixtures):
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
            if "Matchday" not in f.get(None, ""):
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

def x_is_confirmed_eliminated__mutmut_130(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", None):
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

def x_is_confirmed_eliminated__mutmut_131(team_name, fixtures):
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
            if "Matchday" not in f.get(""):
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

def x_is_confirmed_eliminated__mutmut_132(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", ):
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

def x_is_confirmed_eliminated__mutmut_133(team_name, fixtures):
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
            if "Matchday" not in f.get("XXstageXX", ""):
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

def x_is_confirmed_eliminated__mutmut_134(team_name, fixtures):
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
            if "Matchday" not in f.get("STAGE", ""):
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

def x_is_confirmed_eliminated__mutmut_135(team_name, fixtures):
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
            if "Matchday" not in f.get("stage", "XXXX"):
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

def x_is_confirmed_eliminated__mutmut_136(team_name, fixtures):
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
                h = None
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

def x_is_confirmed_eliminated__mutmut_137(team_name, fixtures):
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
                h = f.get(None)
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

def x_is_confirmed_eliminated__mutmut_138(team_name, fixtures):
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
                h = f.get("XXhome_teamXX")
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

def x_is_confirmed_eliminated__mutmut_139(team_name, fixtures):
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
                h = f.get("HOME_TEAM")
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

def x_is_confirmed_eliminated__mutmut_140(team_name, fixtures):
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
                a = None
                if h and not is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_141(team_name, fixtures):
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
                a = f.get(None)
                if h and not is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_142(team_name, fixtures):
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
                a = f.get("XXaway_teamXX")
                if h and not is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_143(team_name, fixtures):
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
                a = f.get("AWAY_TEAM")
                if h and not is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_144(team_name, fixtures):
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
                if h or not is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_145(team_name, fixtures):
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
                if h and is_placeholder(h):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_146(team_name, fixtures):
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
                if h and not is_placeholder(None):
                    bracket_resolution_started = True
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_147(team_name, fixtures):
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
                    bracket_resolution_started = None
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_148(team_name, fixtures):
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
                    bracket_resolution_started = False
                    break
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_149(team_name, fixtures):
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
                    return
                if a and not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_150(team_name, fixtures):
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
                if a or not is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_151(team_name, fixtures):
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
                if a and is_placeholder(a):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_152(team_name, fixtures):
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
                if a and not is_placeholder(None):
                    bracket_resolution_started = True
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_153(team_name, fixtures):
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
                    bracket_resolution_started = None
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_154(team_name, fixtures):
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
                    bracket_resolution_started = False
                    break
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_155(team_name, fixtures):
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
                    return
        if bracket_resolution_started:
            return True
            
        return False

def x_is_confirmed_eliminated__mutmut_156(team_name, fixtures):
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
            return False
            
        return False

def x_is_confirmed_eliminated__mutmut_157(team_name, fixtures):
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
            
        return True

mutants_x_is_confirmed_eliminated__mutmut['_mutmut_orig'] = x_is_confirmed_eliminated__mutmut_orig # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_1'] = x_is_confirmed_eliminated__mutmut_1 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_2'] = x_is_confirmed_eliminated__mutmut_2 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_3'] = x_is_confirmed_eliminated__mutmut_3 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_4'] = x_is_confirmed_eliminated__mutmut_4 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_5'] = x_is_confirmed_eliminated__mutmut_5 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_6'] = x_is_confirmed_eliminated__mutmut_6 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_7'] = x_is_confirmed_eliminated__mutmut_7 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_8'] = x_is_confirmed_eliminated__mutmut_8 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_9'] = x_is_confirmed_eliminated__mutmut_9 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_10'] = x_is_confirmed_eliminated__mutmut_10 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_11'] = x_is_confirmed_eliminated__mutmut_11 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_12'] = x_is_confirmed_eliminated__mutmut_12 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_13'] = x_is_confirmed_eliminated__mutmut_13 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_14'] = x_is_confirmed_eliminated__mutmut_14 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_15'] = x_is_confirmed_eliminated__mutmut_15 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_16'] = x_is_confirmed_eliminated__mutmut_16 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_17'] = x_is_confirmed_eliminated__mutmut_17 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_18'] = x_is_confirmed_eliminated__mutmut_18 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_19'] = x_is_confirmed_eliminated__mutmut_19 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_20'] = x_is_confirmed_eliminated__mutmut_20 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_21'] = x_is_confirmed_eliminated__mutmut_21 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_22'] = x_is_confirmed_eliminated__mutmut_22 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_23'] = x_is_confirmed_eliminated__mutmut_23 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_24'] = x_is_confirmed_eliminated__mutmut_24 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_25'] = x_is_confirmed_eliminated__mutmut_25 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_26'] = x_is_confirmed_eliminated__mutmut_26 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_27'] = x_is_confirmed_eliminated__mutmut_27 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_28'] = x_is_confirmed_eliminated__mutmut_28 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_29'] = x_is_confirmed_eliminated__mutmut_29 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_30'] = x_is_confirmed_eliminated__mutmut_30 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_31'] = x_is_confirmed_eliminated__mutmut_31 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_32'] = x_is_confirmed_eliminated__mutmut_32 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_33'] = x_is_confirmed_eliminated__mutmut_33 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_34'] = x_is_confirmed_eliminated__mutmut_34 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_35'] = x_is_confirmed_eliminated__mutmut_35 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_36'] = x_is_confirmed_eliminated__mutmut_36 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_37'] = x_is_confirmed_eliminated__mutmut_37 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_38'] = x_is_confirmed_eliminated__mutmut_38 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_39'] = x_is_confirmed_eliminated__mutmut_39 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_40'] = x_is_confirmed_eliminated__mutmut_40 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_41'] = x_is_confirmed_eliminated__mutmut_41 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_42'] = x_is_confirmed_eliminated__mutmut_42 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_43'] = x_is_confirmed_eliminated__mutmut_43 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_44'] = x_is_confirmed_eliminated__mutmut_44 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_45'] = x_is_confirmed_eliminated__mutmut_45 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_46'] = x_is_confirmed_eliminated__mutmut_46 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_47'] = x_is_confirmed_eliminated__mutmut_47 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_48'] = x_is_confirmed_eliminated__mutmut_48 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_49'] = x_is_confirmed_eliminated__mutmut_49 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_50'] = x_is_confirmed_eliminated__mutmut_50 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_51'] = x_is_confirmed_eliminated__mutmut_51 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_52'] = x_is_confirmed_eliminated__mutmut_52 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_53'] = x_is_confirmed_eliminated__mutmut_53 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_54'] = x_is_confirmed_eliminated__mutmut_54 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_55'] = x_is_confirmed_eliminated__mutmut_55 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_56'] = x_is_confirmed_eliminated__mutmut_56 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_57'] = x_is_confirmed_eliminated__mutmut_57 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_58'] = x_is_confirmed_eliminated__mutmut_58 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_59'] = x_is_confirmed_eliminated__mutmut_59 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_60'] = x_is_confirmed_eliminated__mutmut_60 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_61'] = x_is_confirmed_eliminated__mutmut_61 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_62'] = x_is_confirmed_eliminated__mutmut_62 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_63'] = x_is_confirmed_eliminated__mutmut_63 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_64'] = x_is_confirmed_eliminated__mutmut_64 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_65'] = x_is_confirmed_eliminated__mutmut_65 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_66'] = x_is_confirmed_eliminated__mutmut_66 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_67'] = x_is_confirmed_eliminated__mutmut_67 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_68'] = x_is_confirmed_eliminated__mutmut_68 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_69'] = x_is_confirmed_eliminated__mutmut_69 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_70'] = x_is_confirmed_eliminated__mutmut_70 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_71'] = x_is_confirmed_eliminated__mutmut_71 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_72'] = x_is_confirmed_eliminated__mutmut_72 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_73'] = x_is_confirmed_eliminated__mutmut_73 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_74'] = x_is_confirmed_eliminated__mutmut_74 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_75'] = x_is_confirmed_eliminated__mutmut_75 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_76'] = x_is_confirmed_eliminated__mutmut_76 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_77'] = x_is_confirmed_eliminated__mutmut_77 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_78'] = x_is_confirmed_eliminated__mutmut_78 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_79'] = x_is_confirmed_eliminated__mutmut_79 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_80'] = x_is_confirmed_eliminated__mutmut_80 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_81'] = x_is_confirmed_eliminated__mutmut_81 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_82'] = x_is_confirmed_eliminated__mutmut_82 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_83'] = x_is_confirmed_eliminated__mutmut_83 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_84'] = x_is_confirmed_eliminated__mutmut_84 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_85'] = x_is_confirmed_eliminated__mutmut_85 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_86'] = x_is_confirmed_eliminated__mutmut_86 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_87'] = x_is_confirmed_eliminated__mutmut_87 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_88'] = x_is_confirmed_eliminated__mutmut_88 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_89'] = x_is_confirmed_eliminated__mutmut_89 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_90'] = x_is_confirmed_eliminated__mutmut_90 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_91'] = x_is_confirmed_eliminated__mutmut_91 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_92'] = x_is_confirmed_eliminated__mutmut_92 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_93'] = x_is_confirmed_eliminated__mutmut_93 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_94'] = x_is_confirmed_eliminated__mutmut_94 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_95'] = x_is_confirmed_eliminated__mutmut_95 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_96'] = x_is_confirmed_eliminated__mutmut_96 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_97'] = x_is_confirmed_eliminated__mutmut_97 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_98'] = x_is_confirmed_eliminated__mutmut_98 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_99'] = x_is_confirmed_eliminated__mutmut_99 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_100'] = x_is_confirmed_eliminated__mutmut_100 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_101'] = x_is_confirmed_eliminated__mutmut_101 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_102'] = x_is_confirmed_eliminated__mutmut_102 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_103'] = x_is_confirmed_eliminated__mutmut_103 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_104'] = x_is_confirmed_eliminated__mutmut_104 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_105'] = x_is_confirmed_eliminated__mutmut_105 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_106'] = x_is_confirmed_eliminated__mutmut_106 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_107'] = x_is_confirmed_eliminated__mutmut_107 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_108'] = x_is_confirmed_eliminated__mutmut_108 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_109'] = x_is_confirmed_eliminated__mutmut_109 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_110'] = x_is_confirmed_eliminated__mutmut_110 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_111'] = x_is_confirmed_eliminated__mutmut_111 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_112'] = x_is_confirmed_eliminated__mutmut_112 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_113'] = x_is_confirmed_eliminated__mutmut_113 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_114'] = x_is_confirmed_eliminated__mutmut_114 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_115'] = x_is_confirmed_eliminated__mutmut_115 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_116'] = x_is_confirmed_eliminated__mutmut_116 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_117'] = x_is_confirmed_eliminated__mutmut_117 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_118'] = x_is_confirmed_eliminated__mutmut_118 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_119'] = x_is_confirmed_eliminated__mutmut_119 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_120'] = x_is_confirmed_eliminated__mutmut_120 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_121'] = x_is_confirmed_eliminated__mutmut_121 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_122'] = x_is_confirmed_eliminated__mutmut_122 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_123'] = x_is_confirmed_eliminated__mutmut_123 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_124'] = x_is_confirmed_eliminated__mutmut_124 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_125'] = x_is_confirmed_eliminated__mutmut_125 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_126'] = x_is_confirmed_eliminated__mutmut_126 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_127'] = x_is_confirmed_eliminated__mutmut_127 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_128'] = x_is_confirmed_eliminated__mutmut_128 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_129'] = x_is_confirmed_eliminated__mutmut_129 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_130'] = x_is_confirmed_eliminated__mutmut_130 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_131'] = x_is_confirmed_eliminated__mutmut_131 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_132'] = x_is_confirmed_eliminated__mutmut_132 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_133'] = x_is_confirmed_eliminated__mutmut_133 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_134'] = x_is_confirmed_eliminated__mutmut_134 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_135'] = x_is_confirmed_eliminated__mutmut_135 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_136'] = x_is_confirmed_eliminated__mutmut_136 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_137'] = x_is_confirmed_eliminated__mutmut_137 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_138'] = x_is_confirmed_eliminated__mutmut_138 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_139'] = x_is_confirmed_eliminated__mutmut_139 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_140'] = x_is_confirmed_eliminated__mutmut_140 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_141'] = x_is_confirmed_eliminated__mutmut_141 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_142'] = x_is_confirmed_eliminated__mutmut_142 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_143'] = x_is_confirmed_eliminated__mutmut_143 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_144'] = x_is_confirmed_eliminated__mutmut_144 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_145'] = x_is_confirmed_eliminated__mutmut_145 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_146'] = x_is_confirmed_eliminated__mutmut_146 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_147'] = x_is_confirmed_eliminated__mutmut_147 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_148'] = x_is_confirmed_eliminated__mutmut_148 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_149'] = x_is_confirmed_eliminated__mutmut_149 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_150'] = x_is_confirmed_eliminated__mutmut_150 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_151'] = x_is_confirmed_eliminated__mutmut_151 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_152'] = x_is_confirmed_eliminated__mutmut_152 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_153'] = x_is_confirmed_eliminated__mutmut_153 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_154'] = x_is_confirmed_eliminated__mutmut_154 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_155'] = x_is_confirmed_eliminated__mutmut_155 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_156'] = x_is_confirmed_eliminated__mutmut_156 # type: ignore # mutmut generated
mutants_x_is_confirmed_eliminated__mutmut['x_is_confirmed_eliminated__mutmut_157'] = x_is_confirmed_eliminated__mutmut_157 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut: MutantDict = {}  # type: ignore

@_mutmut_mutated(mutants_x_resolve_team_statuses__mutmut)
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

def x_resolve_team_statuses__mutmut_orig(fixtures_data, now_dt):
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

def x_resolve_team_statuses__mutmut_1(fixtures_data, now_dt):
    all_teams = None
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

def x_resolve_team_statuses__mutmut_2(fixtures_data, now_dt):
    all_teams = set()
    normally_active = None
    
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

def x_resolve_team_statuses__mutmut_3(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = None
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

def x_resolve_team_statuses__mutmut_4(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get(None)
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

def x_resolve_team_statuses__mutmut_5(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("XXhome_teamXX")
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

def x_resolve_team_statuses__mutmut_6(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("HOME_TEAM")
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

def x_resolve_team_statuses__mutmut_7(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = None
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

def x_resolve_team_statuses__mutmut_8(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get(None)
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

def x_resolve_team_statuses__mutmut_9(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("XXaway_teamXX")
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

def x_resolve_team_statuses__mutmut_10(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("AWAY_TEAM")
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

def x_resolve_team_statuses__mutmut_11(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h or not is_placeholder(h):
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

def x_resolve_team_statuses__mutmut_12(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and is_placeholder(h):
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

def x_resolve_team_statuses__mutmut_13(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(None):
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

def x_resolve_team_statuses__mutmut_14(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(None)
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

def x_resolve_team_statuses__mutmut_15(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(None))
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

def x_resolve_team_statuses__mutmut_16(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a or not is_placeholder(a):
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

def x_resolve_team_statuses__mutmut_17(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and is_placeholder(a):
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

def x_resolve_team_statuses__mutmut_18(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(None):
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

def x_resolve_team_statuses__mutmut_19(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(None)
            
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

def x_resolve_team_statuses__mutmut_20(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(normalize_team_name(None))
            
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

def x_resolve_team_statuses__mutmut_21(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(normalize_team_name(a))
            
        kickoff_str = None
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

def x_resolve_team_statuses__mutmut_22(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(normalize_team_name(a))
            
        kickoff_str = fixture.get(None)
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

def x_resolve_team_statuses__mutmut_23(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(normalize_team_name(a))
            
        kickoff_str = fixture.get("XXkickoff_utcXX")
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

def x_resolve_team_statuses__mutmut_24(fixtures_data, now_dt):
    all_teams = set()
    normally_active = set()
    
    for fixture in fixtures_data:
        h = fixture.get("home_team")
        a = fixture.get("away_team")
        if h and not is_placeholder(h):
            all_teams.add(normalize_team_name(h))
        if a and not is_placeholder(a):
            all_teams.add(normalize_team_name(a))
            
        kickoff_str = fixture.get("KICKOFF_UTC")
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

def x_resolve_team_statuses__mutmut_25(fixtures_data, now_dt):
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
        if kickoff_str:
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

def x_resolve_team_statuses__mutmut_26(fixtures_data, now_dt):
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
            break
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

def x_resolve_team_statuses__mutmut_27(fixtures_data, now_dt):
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
            kickoff_dt = None
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

def x_resolve_team_statuses__mutmut_28(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(None)
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

def x_resolve_team_statuses__mutmut_29(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace(None, "+00:00"))
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

def x_resolve_team_statuses__mutmut_30(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("Z", None))
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

def x_resolve_team_statuses__mutmut_31(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("+00:00"))
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

def x_resolve_team_statuses__mutmut_32(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("Z", ))
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

def x_resolve_team_statuses__mutmut_33(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("XXZXX", "+00:00"))
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

def x_resolve_team_statuses__mutmut_34(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("z", "+00:00"))
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

def x_resolve_team_statuses__mutmut_35(fixtures_data, now_dt):
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
            kickoff_dt = datetime.fromisoformat(kickoff_str.replace("Z", "XX+00:00XX"))
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

def x_resolve_team_statuses__mutmut_36(fixtures_data, now_dt):
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
            break
            
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

def x_resolve_team_statuses__mutmut_37(fixtures_data, now_dt):
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
            
        is_completed = None
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

def x_resolve_team_statuses__mutmut_38(fixtures_data, now_dt):
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
            
        is_completed = fixture.get(None) is not None
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

def x_resolve_team_statuses__mutmut_39(fixtures_data, now_dt):
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
            
        is_completed = fixture.get("XXresultXX") is not None
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

def x_resolve_team_statuses__mutmut_40(fixtures_data, now_dt):
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
            
        is_completed = fixture.get("RESULT") is not None
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

def x_resolve_team_statuses__mutmut_41(fixtures_data, now_dt):
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
            
        is_completed = fixture.get("result") is None
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

def x_resolve_team_statuses__mutmut_42(fixtures_data, now_dt):
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
        if kickoff_dt >= now_dt or not is_completed:
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

def x_resolve_team_statuses__mutmut_43(fixtures_data, now_dt):
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
        if kickoff_dt > now_dt and not is_completed:
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

def x_resolve_team_statuses__mutmut_44(fixtures_data, now_dt):
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
        if kickoff_dt >= now_dt and is_completed:
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

def x_resolve_team_statuses__mutmut_45(fixtures_data, now_dt):
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
            if h or not is_placeholder(h):
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

def x_resolve_team_statuses__mutmut_46(fixtures_data, now_dt):
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
            if h and is_placeholder(h):
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

def x_resolve_team_statuses__mutmut_47(fixtures_data, now_dt):
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
            if h and not is_placeholder(None):
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

def x_resolve_team_statuses__mutmut_48(fixtures_data, now_dt):
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
                normally_active.add(None)
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

def x_resolve_team_statuses__mutmut_49(fixtures_data, now_dt):
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
                normally_active.add(normalize_team_name(None))
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

def x_resolve_team_statuses__mutmut_50(fixtures_data, now_dt):
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
            if a or not is_placeholder(a):
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

def x_resolve_team_statuses__mutmut_51(fixtures_data, now_dt):
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
            if a and is_placeholder(a):
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

def x_resolve_team_statuses__mutmut_52(fixtures_data, now_dt):
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
            if a and not is_placeholder(None):
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

def x_resolve_team_statuses__mutmut_53(fixtures_data, now_dt):
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
                normally_active.add(None)
                
    gap_window = set()
    skipped = set()
    for team in all_teams:
        if team not in normally_active:
            if not is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_54(fixtures_data, now_dt):
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
                normally_active.add(normalize_team_name(None))
                
    gap_window = set()
    skipped = set()
    for team in all_teams:
        if team not in normally_active:
            if not is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_55(fixtures_data, now_dt):
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
                
    gap_window = None
    skipped = set()
    for team in all_teams:
        if team not in normally_active:
            if not is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_56(fixtures_data, now_dt):
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
    skipped = None
    for team in all_teams:
        if team not in normally_active:
            if not is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_57(fixtures_data, now_dt):
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
        if team in normally_active:
            if not is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_58(fixtures_data, now_dt):
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
            if is_confirmed_eliminated(team, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_59(fixtures_data, now_dt):
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
            if not is_confirmed_eliminated(None, fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_60(fixtures_data, now_dt):
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
            if not is_confirmed_eliminated(team, None):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_61(fixtures_data, now_dt):
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
            if not is_confirmed_eliminated(fixtures_data):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_62(fixtures_data, now_dt):
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
            if not is_confirmed_eliminated(team, ):
                gap_window.add(team)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_63(fixtures_data, now_dt):
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
                gap_window.add(None)
            else:
                skipped.add(team)
                
    return normally_active, gap_window, skipped

def x_resolve_team_statuses__mutmut_64(fixtures_data, now_dt):
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
                skipped.add(None)
                
    return normally_active, gap_window, skipped

mutants_x_resolve_team_statuses__mutmut['_mutmut_orig'] = x_resolve_team_statuses__mutmut_orig # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_1'] = x_resolve_team_statuses__mutmut_1 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_2'] = x_resolve_team_statuses__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_3'] = x_resolve_team_statuses__mutmut_3 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_4'] = x_resolve_team_statuses__mutmut_4 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_5'] = x_resolve_team_statuses__mutmut_5 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_6'] = x_resolve_team_statuses__mutmut_6 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_7'] = x_resolve_team_statuses__mutmut_7 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_8'] = x_resolve_team_statuses__mutmut_8 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_9'] = x_resolve_team_statuses__mutmut_9 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_10'] = x_resolve_team_statuses__mutmut_10 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_11'] = x_resolve_team_statuses__mutmut_11 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_12'] = x_resolve_team_statuses__mutmut_12 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_13'] = x_resolve_team_statuses__mutmut_13 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_14'] = x_resolve_team_statuses__mutmut_14 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_15'] = x_resolve_team_statuses__mutmut_15 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_16'] = x_resolve_team_statuses__mutmut_16 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_17'] = x_resolve_team_statuses__mutmut_17 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_18'] = x_resolve_team_statuses__mutmut_18 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_19'] = x_resolve_team_statuses__mutmut_19 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_20'] = x_resolve_team_statuses__mutmut_20 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_21'] = x_resolve_team_statuses__mutmut_21 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_22'] = x_resolve_team_statuses__mutmut_22 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_23'] = x_resolve_team_statuses__mutmut_23 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_24'] = x_resolve_team_statuses__mutmut_24 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_25'] = x_resolve_team_statuses__mutmut_25 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_26'] = x_resolve_team_statuses__mutmut_26 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_27'] = x_resolve_team_statuses__mutmut_27 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_28'] = x_resolve_team_statuses__mutmut_28 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_29'] = x_resolve_team_statuses__mutmut_29 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_30'] = x_resolve_team_statuses__mutmut_30 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_31'] = x_resolve_team_statuses__mutmut_31 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_32'] = x_resolve_team_statuses__mutmut_32 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_33'] = x_resolve_team_statuses__mutmut_33 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_34'] = x_resolve_team_statuses__mutmut_34 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_35'] = x_resolve_team_statuses__mutmut_35 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_36'] = x_resolve_team_statuses__mutmut_36 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_37'] = x_resolve_team_statuses__mutmut_37 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_38'] = x_resolve_team_statuses__mutmut_38 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_39'] = x_resolve_team_statuses__mutmut_39 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_40'] = x_resolve_team_statuses__mutmut_40 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_41'] = x_resolve_team_statuses__mutmut_41 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_42'] = x_resolve_team_statuses__mutmut_42 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_43'] = x_resolve_team_statuses__mutmut_43 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_44'] = x_resolve_team_statuses__mutmut_44 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_45'] = x_resolve_team_statuses__mutmut_45 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_46'] = x_resolve_team_statuses__mutmut_46 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_47'] = x_resolve_team_statuses__mutmut_47 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_48'] = x_resolve_team_statuses__mutmut_48 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_49'] = x_resolve_team_statuses__mutmut_49 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_50'] = x_resolve_team_statuses__mutmut_50 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_51'] = x_resolve_team_statuses__mutmut_51 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_52'] = x_resolve_team_statuses__mutmut_52 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_53'] = x_resolve_team_statuses__mutmut_53 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_54'] = x_resolve_team_statuses__mutmut_54 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_55'] = x_resolve_team_statuses__mutmut_55 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_56'] = x_resolve_team_statuses__mutmut_56 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_57'] = x_resolve_team_statuses__mutmut_57 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_58'] = x_resolve_team_statuses__mutmut_58 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_59'] = x_resolve_team_statuses__mutmut_59 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_60'] = x_resolve_team_statuses__mutmut_60 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_61'] = x_resolve_team_statuses__mutmut_61 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_62'] = x_resolve_team_statuses__mutmut_62 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_63'] = x_resolve_team_statuses__mutmut_63 # type: ignore # mutmut generated
mutants_x_resolve_team_statuses__mutmut['x_resolve_team_statuses__mutmut_64'] = x_resolve_team_statuses__mutmut_64 # type: ignore # mutmut generated

