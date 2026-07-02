import os
import sys
import json
import requests
from datetime import datetime, timedelta, timezone

# Headers for all requests
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
ID_COMPETITION = 17
ID_SEASON = 285023

def run_lineup_bot():
    try:
        # Determine paths relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        lineups_path = os.path.join(base_dir, "public", "data", "scraped", "lineups.json")
        os.makedirs(os.path.dirname(lineups_path), exist_ok=True)

        # Load existing lineups
        lineups = {}
        if os.path.exists(lineups_path):
            try:
                with open(lineups_path, "r", encoding="utf-8") as f:
                    lineups = json.load(f)
            except Exception:
                lineups = {}

        # Fetch matches calendar
        url = f"https://api.fifa.com/api/v3/calendar/matches?idCompetition={ID_COMPETITION}&idSeason={ID_SEASON}&count=104&language=en-GB"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Calendar fetch failed: Status {r.status_code}", file=sys.stderr)
            sys.exit(1)

        data = r.json()
        matches = data.get("Results", [])

        now = datetime.now(timezone.utc)
        six_hours_later = now + timedelta(hours=6)

        updated_any = False

        for m in matches:
            match_status = m.get("MatchStatus")
            # Usually MatchStatus 1 is upcoming, check if not completed (0 or 3)
            # Let's check: str(match_status) == "1" or m.get("MatchStatus") == 1
            if str(match_status) != "1":
                continue

            date_str = m.get("Date")
            if not date_str:
                continue

            try:
                match_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except Exception:
                continue

            # Check if within the next 6 hours (and not in the past)
            if now <= match_date <= six_hours_later:
                id_stage = m.get("IdStage")
                id_match = m.get("IdMatch")
                if not id_stage or not id_match:
                    continue

                # Fetch live match details (lineups)
                live_url = f"https://api.fifa.com/api/v3/live/football/{ID_COMPETITION}/{ID_SEASON}/{id_stage}/{id_match}?language=en-GB"
                lr = requests.get(live_url, headers=headers, timeout=15)
                if lr.status_code != 200:
                    continue

                live_data = lr.json()

                # Parse squads
                home_team_data = live_data.get("HomeTeam") or live_data.get("HomeTeamSquad") or {}
                away_team_data = live_data.get("AwayTeam") or live_data.get("AwayTeamSquad") or {}
                
                home_players = home_team_data.get("Players") or home_team_data.get("Squad") or []
                away_players = away_team_data.get("Players") or away_team_data.get("Squad") or []

                if not home_players and not away_players:
                    continue

                # Resolve team abbreviations
                home_obj = m.get("Home") or m.get("HomeTeam") or {}
                away_obj = m.get("Away") or m.get("AwayTeam") or {}
                home_code = home_obj.get("Abbreviation") or "HOME"
                away_code = away_obj.get("Abbreviation") or "AWAY"

                home_starters = []
                home_subs = []
                away_starters = []
                away_subs = []

                def parse_player(p):
                    # Player Name
                    p_names = p.get("PlayerName", [])
                    name = p_names[0].get("Description") if p_names else p.get("ShortName", [{}])[0].get("Description", "Unknown Player")
                    
                    return {
                        "id": str(p.get("IdPlayer") or p.get("PlayerId") or ""),
                        "name": name,
                        "position": p.get("Position"),
                        "shirt": p.get("ShirtNumber") or p.get("Shirt"),
                        "captain": bool(p.get("Captain") or p.get("IsCaptain") or False),
                        "x": p.get("LineupX"),
                        "y": p.get("LineupY")
                    }

                for p in home_players:
                    status = p.get("Status")
                    parsed = parse_player(p)
                    if str(status) == "1" or status == 1:
                        home_starters.append(parsed)
                    else:
                        home_subs.append(parsed)

                for p in away_players:
                    status = p.get("Status")
                    parsed = parse_player(p)
                    if str(status) == "1" or status == 1:
                        away_starters.append(parsed)
                    else:
                        away_subs.append(parsed)

                # Only write if starters array is non-empty
                if home_starters or away_starters:
                    lineups[str(id_match)] = {
                        "home": home_code,
                        "away": away_code,
                        "date": date_str,
                        "home_starters": home_starters,
                        "away_starters": away_starters,
                        "home_subs": home_subs,
                        "away_subs": away_subs
                    }
                    updated_any = True
                    print(f"Updated lineup for match {id_match}: {home_code} vs {away_code}")

        if updated_any:
            with open(lineups_path, "w", encoding="utf-8") as f:
                json.dump(lineups, f, separators=(',', ':'), ensure_ascii=False)
            print("Successfully wrote updated lineups.")
        else:
            print("No new lineups updated.")

        sys.exit(0)

    except Exception as e:
        print(f"Error in lineup bot: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_lineup_bot()
