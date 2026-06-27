import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Add parent directory to path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import COMPETITION_CONFIG

def scrape_injuries():
    headers = {"User-Agent": COMPETITION_CONFIG["user_agent"]}
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
    for table in tables:
        # Determine team name from parent box table header
        parent_box = table.find_parent("div", class_="box")
        team_name = "Unknown Team"
        if parent_box:
            header = parent_box.find("div", class_="table-header")
            if header:
                team_name = header.get_text(strip=True).split("-")[0].strip()
                
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
        print(f"updated: {len(injuries)} injuries/suspensions")
    else:
        print("no changes detected")

if __name__ == "__main__":
    scrape_injuries()
