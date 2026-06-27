import os

# Base directory setup relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "scraped")

COMPETITION_CONFIG = {
    "competition_name": "FIFA World Cup 2026",
    "year": 2026,
    "openfootball_url": "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2026/worldcup.json",
    "fixtures_path": os.path.join(DATA_DIR, "fixtures.json"),
    "injuries_path": os.path.join(DATA_DIR, "injuries.json"),
    "squads_path": os.path.join(DATA_DIR, "squads.json"),
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
