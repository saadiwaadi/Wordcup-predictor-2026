import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Add parent directory to path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import COMPETITION_CONFIG, normalize_team_name, resolve_team_statuses

def scrape_injuries():
    headers = {"User-Agent": COMPETITION_CONFIG["user_agent"]}
    
    # Load fixtures to determine active teams
    fixtures_path = COMPETITION_CONFIG["fixtures_path"]
    active_teams = set()
    fixtures_loaded = False
    if os.path.exists(fixtures_path):
        try:
            with open(fixtures_path, "r", encoding="utf-8") as f:
                fixtures_data = json.load(f)
                fixtures_loaded = True
        except Exception as e:
            print(f"Warning: failed to load fixtures.json: {e}", file=sys.stderr)
            
    if fixtures_loaded:
        from datetime import timezone
        now = datetime.now(timezone.utc)
        normally_active, gap_window, skipped = resolve_team_statuses(fixtures_data, now)
        active_teams_set = normally_active.union(gap_window)
        active_teams = {t.lower() for t in active_teams_set}

        gap_names = sorted(list(gap_window))
        if gap_names:
            print(f"Active (gap window — placeholder unresolved): {', '.join(gap_names)}")

    # Transfermarkt absences page for World Cup
    url = "https://www.transfermarkt.com/weltmeisterschaft2026/ausfalle/pokalwettbewerb/WM26"
    
    print(f"Fetching Transfermarkt absences: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Error: Transfermarkt returned status code {r.status_code}", file=sys.stderr)
            sys.exit(0)
        html_content = r.text
    except Exception as e:
        print(f"Exception during request to Transfermarkt: {e}", file=sys.stderr)
        sys.exit(0)
        
    soup = BeautifulSoup(html_content, "html.parser")
    injuries = []
    
    # Locate all tables showing player lists
    tables = soup.find_all("table", class_="items")
    all_teams_found = set()
    active_teams_found = set()
    for table in tables:
        # Determine team name from parent box table header
        parent_box = table.find_parent("div", class_="box")
        team_name = "Unknown Team"
        if parent_box:
            header = parent_box.find("div", class_="table-header")
            if header:
                team_name = header.get_text(strip=True).split("-")[0].strip()
        
        all_teams_found.add(team_name)
        if active_teams:
            norm_team = normalize_team_name(team_name).lower()
            if norm_team not in active_teams:
                continue
        active_teams_found.add(team_name)
                
        rows = table.find_all("tr", class_=["odd", "even"])
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name_el = cols[0].find("a")
                player_name = name_el.get_text(strip=True) if name_el else "Unknown Player"
                
                # Absence reason/status text
                injury_reason = cols[2].get_text(strip=True) if len(cols) > 2 else "Injured"
                
                status = "injured"
                reason_lower = injury_reason.lower()
                if "suspension" in reason_lower or "suspended" in reason_lower:
                    status = "suspended"
                elif "doubtful" in reason_lower:
                    status = "doubtful"
                elif "fit" in reason_lower:
                    status = "fit"
                    
                injuries.append({
                    "player_name": player_name,
                    "team": team_name,
                    "status": status,
                    "updated_at": datetime.utcnow().isoformat() + "Z"
                })
                
    output_path = COMPETITION_CONFIG["injuries_path"]
    existing_injuries = []
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_injuries = json.load(f)
        except Exception:
            pass
            
    # Normalize for comparison by ignoring updated_at
    def normalize_data(lst):
        return [{k: v for k, v in item.items() if k != "updated_at"} for item in lst]
        
    if normalize_data(existing_injuries) != normalize_data(injuries):
        # Update updated_at for writing
        timestamp_str = datetime.utcnow().isoformat() + "Z"
        for item in injuries:
            item["updated_at"] = timestamp_str
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(injuries, f, indent=2, ensure_ascii=False)
        skipped_teams = sorted(list(all_teams_found - active_teams_found))
        print(f"Injury Bot Summary: Pulled injuries for {len(active_teams_found)} teams. Skipped {len(skipped_teams)} teams: {', '.join(skipped_teams)}")
        print(f"updated: {len(injuries)} injuries/suspensions")
    else:
        skipped_teams = sorted(list(all_teams_found - active_teams_found))
        print(f"Injury Bot Summary: Pulled injuries for {len(active_teams_found)} teams. Skipped {len(skipped_teams)} teams: {', '.join(skipped_teams)}")
        print("no changes detected")

if __name__ == "__main__":
    scrape_injuries()
