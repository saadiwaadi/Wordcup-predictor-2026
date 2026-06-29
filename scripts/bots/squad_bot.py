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

def run_squad_bot():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        squads_path = os.path.join(
            base_dir, "public", "data", "scraped", "squads.json")
        os.makedirs(os.path.dirname(squads_path), exist_ok=True)

        squads = {}
        if os.path.exists(squads_path):
            try:
                with open(squads_path, "r", encoding="utf-8") as f:
                    squads = json.load(f)
            except Exception:
                squads = {}

        # Fetch all teams in the competition
        teams_url = (
            f"https://api.fifa.com/api/v3/teams"
            f"?idCompetition={ID_COMPETITION}"
            f"&idSeason={ID_SEASON}"
            f"&count=48&language=en-GB"
        )
        print(f"Fetching teams from: {teams_url}")
        r = requests.get(teams_url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Error: teams endpoint returned {r.status_code}",
                  file=sys.stderr)
            sys.exit(1)

        teams_data = r.json().get("Results", [])
        if not teams_data:
            print("Error: no teams found", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(teams_data)} teams. Fetching squads...")
        updated = 0

        for team in teams_data:
            team_id = team.get("IdTeam")
            team_name = None
            for n in team.get("Name", []):
                if n.get("Locale") == "en-GB" or not team_name:
                    team_name = n.get("Description")

            abbreviation = team.get("Abbreviation", "")

            if not team_id:
                continue

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
    