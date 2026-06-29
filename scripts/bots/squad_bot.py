import os
import sys
import json
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

ID_COMPETITION = 17
ID_SEASON = 285023

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

def run_squad_bot():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        
        fixtures_path = os.path.join(
            base_dir, "public", "data", "scraped", "fixtures.json")
        squads_path = os.path.join(
            base_dir, "public", "data", "scraped", "squads.json")
        os.makedirs(os.path.dirname(squads_path), exist_ok=True)

        if not os.path.exists(fixtures_path):
            print(f"Warning: fixtures.json not found at {fixtures_path}. Skipping squad update.", file=sys.stderr)
            sys.exit(0)

        try:
            with open(fixtures_path, "r", encoding="utf-8") as f:
                fixtures_data = json.load(f)
        except Exception as e:
            print(f"Warning: failed to load fixtures.json: {e}", file=sys.stderr)
            sys.exit(0)

        unique_teams = set()
        for fixture in fixtures_data:
            h = fixture.get("home_team")
            a = fixture.get("away_team")
            if h:
                unique_teams.add(h)
            if a:
                unique_teams.add(a)

        squads = {}
        if os.path.exists(squads_path):
            try:
                with open(squads_path, "r", encoding="utf-8") as f:
                    squads = json.load(f)
            except Exception:
                squads = {}

        # Fetch matches calendar to get team names and team IDs
        matches_url = (
            f"https://api.fifa.com/api/v3/calendar/matches"
            f"?idCompetition={ID_COMPETITION}"
            f"&idSeason={ID_SEASON}"
            f"&count=104&language=en-GB"
        )
        print(f"Fetching matches from: {matches_url}")
        r = requests.get(matches_url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Error: matches endpoint returned {r.status_code}",
                  file=sys.stderr)
            sys.exit(1)

        results = r.json().get("Results", [])
        fifa_teams = {}
        for m in results:
            for key in ["Home", "Away"]:
                team_obj = m.get(key)
                if not team_obj:
                    continue
                team_id = team_obj.get("IdTeam")
                if not team_id:
                    continue

                if team_id not in fifa_teams:
                    team_name = None
                    names = set()
                    for n in team_obj.get("TeamName", []):
                        desc = n.get("Description")
                        if desc:
                            names.add(desc.strip().lower())
                            if n.get("Locale") == "en-GB" or not team_name:
                                team_name = desc.strip()
                    
                    short_club = team_obj.get("ShortClubName")
                    if short_club:
                        names.add(short_club.strip().lower())
                        if not team_name:
                            team_name = short_club.strip()
                            
                    abbreviation = team_obj.get("Abbreviation")
                    if abbreviation:
                        names.add(abbreviation.strip().lower())
                        if not team_name:
                            team_name = abbreviation.strip()
                    
                    # Add normalized version of names to names set
                    norm_names = set()
                    for name_val in names:
                        norm_names.add(normalize_team_name(name_val).lower())
                    names.update(norm_names)

                    fifa_teams[team_id] = {
                        "team_id": team_id,
                        "team_name": team_name,
                        "abbreviation": abbreviation or "",
                        "names": names
                    }

        teams_to_fetch = []
        for fixture_name in unique_teams:
            fixture_name_lower = fixture_name.strip().lower()
            fixture_name_norm_lower = normalize_team_name(fixture_name).lower()
            
            matched_team = None
            for team_id, team_info in fifa_teams.items():
                if (fixture_name_lower in team_info["names"] or 
                    fixture_name_norm_lower in team_info["names"]):
                    matched_team = team_info
                    break
            
            if matched_team:
                if matched_team not in teams_to_fetch:
                    teams_to_fetch.append(matched_team)
            else:
                print(f"Warning: Could not find FIFA team ID for fixture team '{fixture_name}'", file=sys.stderr)

        print(f"Found {len(teams_to_fetch)} teams from fixtures. Fetching squads...")
        updated = 0

        for team in teams_to_fetch:
            team_id = team["team_id"]
            team_name = team["team_name"]
            abbreviation = team["abbreviation"]

            squad_url = (
                f"https://api.fifa.com/api/v3/teams/{team_id}/squads"
                f"?idCompetition={ID_COMPETITION}"
                f"&idSeason={ID_SEASON}"
                f"&language=en-GB"
            )

            try:
                sr = requests.get(squad_url, headers=headers, timeout=15)
                if sr.status_code != 200:
                    print(f"  Warning: squad fetch failed for "
                          f"{team_name} ({sr.status_code})")
                    continue

                squad_data = sr.json().get("Results", [])
                players = []

                for p in squad_data:
                    name_list = p.get("Name", [])
                    player_name = None
                    for n in name_list:
                        if n.get("Locale") == "en-GB" or not player_name:
                            player_name = n.get("Description")

                    shirt_number = p.get("ShirtNumber")
                    position_id = p.get("PositionLocalized", [{}])
                    position = None
                    for pos in position_id:
                        if pos.get("Locale") == "en-GB" or not position:
                            position = pos.get("Description")

                    dob = p.get("BirthDate", "")

                    players.append({
                        "name": player_name,
                        "number": shirt_number,
                        "position": position,
                        "date_of_birth": dob[:10] if dob else None,
                        "player_id": p.get("IdPlayer")
                    })

                players.sort(key=lambda x: x.get("number") or 99)

                squads[abbreviation] = {
                    "team_id": team_id,
                    "team_name": team_name,
                    "abbreviation": abbreviation,
                    "players": players
                }
                updated += 1
                print(f"  {team_name}: {len(players)} players")

            except Exception as e:
                print(f"  Warning: error fetching squad for "
                      f"{team_name}: {e}")
                continue

        with open(squads_path, "w", encoding="utf-8") as f:
            json.dump(squads, f, indent=2, ensure_ascii=False)

        print(f"Squads updated: {updated} teams written to {squads_path}")

    except Exception as e:
        print(f"Fatal error in squad bot: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_squad_bot()