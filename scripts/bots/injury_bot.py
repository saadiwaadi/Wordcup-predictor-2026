import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Add parent directory to path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import COMPETITION_CONFIG, normalize_team_name, resolve_team_statuses, get_team_code

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
    url = "https://www.transfermarkt.com/weltmeisterschaft-2026/ausfalle/pokalwettbewerb/WM26"
    
    print(f"Fetching Transfermarkt absences: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            if r.status_code in [403, 405] or "captcha" in r.text.lower() or "human verification" in r.text.lower():
                print(f"FATAL ERROR: WAF/CAPTCHA Block detected on Transfermarkt. Status code: {r.status_code}", file=sys.stderr)
                print("Response contains Cloudflare/AWS WAF challenge. Scraping cannot proceed.", file=sys.stderr)
            else:
                print(f"FATAL ERROR: Transfermarkt returned status code {r.status_code}", file=sys.stderr)
            sys.exit(1)
        html_content = r.text
    except Exception as e:
        print(f"FATAL ERROR: Exception during request to Transfermarkt: {e}", file=sys.stderr)
        sys.exit(1)
        
    soup = BeautifulSoup(html_content, "html.parser")
    injuries_dict = {}
    timestamp_str = datetime.utcnow().isoformat() + "Z"
    
    # Locate all tables showing player lists
    tables = soup.find_all("table", class_="items")
    if not tables:
        print("FATAL ERROR: No injury/absence tables found on the Transfermarkt page. Structure may have changed or page was blocked.", file=sys.stderr)
        sys.exit(1)
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
        
        code = get_team_code(team_name)
        if not code:
            continue
            
        if code not in injuries_dict:
            injuries_dict[code] = {
                "team_id": code,
                "team_name": team_name,
                "injured_players": [],
                "updated_at": timestamp_str
            }
                
        rows = table.find_all("tr", class_=["odd", "even"])
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name_el = cols[0].find("a")
                player_name = name_el.get_text(strip=True) if name_el else "Unknown Player"
                
                injuries_dict[code]["injured_players"].append(player_name)

    # Initialize all active teams not found on the page with empty injured_players list
    for t_name in active_teams_set:
        code = get_team_code(t_name)
        if code and code not in injuries_dict:
            injuries_dict[code] = {
                "team_id": code,
                "team_name": t_name,
                "injured_players": [],
                "updated_at": timestamp_str
            }
                
    output_path = COMPETITION_CONFIG["injuries_path"]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(injuries_dict, f, indent=2, ensure_ascii=False)
        
    skipped_teams = sorted(list(all_teams_found - active_teams_found))
    print(f"Injury Bot Summary: Pulled injuries for {len(active_teams_found)} teams. Skipped {len(skipped_teams)} teams: {', '.join(skipped_teams)}")
    total_injuries = sum(len(info["injured_players"]) for info in injuries_dict.values())
    print(f"updated: {total_injuries} injuries/suspensions across {len(injuries_dict)} teams")


if __name__ == "__main__":
    scrape_injuries()
