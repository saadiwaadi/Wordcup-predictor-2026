import os
import sys
import json
import time
import requests

# Add parent directory to path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import COMPETITION_CONFIG

def bootstrap_squads():
    # Derive the squads URL from openfootball_url
    url = COMPETITION_CONFIG["openfootball_url"].replace("worldcup.json", "worldcup.squads.json")
    headers = {"User-Agent": COMPETITION_CONFIG["user_agent"]}
    
    print(f"Fetching squad database from: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Error: Server returned status code {r.status_code}", file=sys.stderr)
            sys.exit(1)
        data = r.json()
    except Exception as e:
        print(f"Error fetching squad database: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Check if the squads are returned directly as a list or wrapped in an object
    if isinstance(data, list):
        squads_list = data
    elif isinstance(data, dict):
        squads_list = data.get("squads", [])
    else:
        squads_list = []
        
    if not squads_list:
        print("Error: No squads found in JSON response", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(squads_list)} squads. Starting sequential parsing...")
    squads_by_team = {}
    total_players_written = 0
    
    for idx, team_squad in enumerate(squads_list):
        team_name = team_squad.get("name", "Unknown Team")
        players = []
        
        for p in team_squad.get("players", []):
            club_data = p.get("club")
            club_name = club_data.get("name") if isinstance(club_data, dict) else club_data
            
            players.append({
                "name": p.get("name"),
                "position": p.get("pos"),
                "club": club_name
            })
            
        squads_by_team[team_name] = players
        total_players_written += len(players)
        print(f"[{idx+1}/{len(squads_list)}] Parsed {team_name} - {len(players)} players extracted")
        
        # 2 second sleep between team parse
        time.sleep(2)
        
    # Write to target path
    output_path = COMPETITION_CONFIG["squads_path"]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(squads_by_team, f, separators=(',', ':'), ensure_ascii=False)
        
    print(f"\nBootstrap conclude. Total teams: {len(squads_by_team)}, Total players written: {total_players_written}")

if __name__ == "__main__":
    bootstrap_squads()
