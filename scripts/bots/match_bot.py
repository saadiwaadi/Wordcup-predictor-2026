import os
import sys
import json
import requests

# Headers for all requests
headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
ID_COMPETITION = 17
ID_SEASON = 285023

def run_match_bot():
    try:
        # Determine paths relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        events_path = os.path.join(base_dir, "public", "data", "scraped", "match_events.json")
        os.makedirs(os.path.dirname(events_path), exist_ok=True)

        # Load existing match events
        match_events = {}
        if os.path.exists(events_path):
            try:
                with open(events_path, "r", encoding="utf-8") as f:
                    match_events = json.load(f)
            except Exception:
                match_events = {}

        # Fetch matches calendar
        url = f"https://api.fifa.com/api/v3/calendar/matches?idCompetition={ID_COMPETITION}&idSeason={ID_SEASON}&count=104&language=en-GB"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"Calendar fetch failed: Status {r.status_code}", file=sys.stderr)
            sys.exit(1)

        data = r.json()
        matches = data.get("Results", [])

        updated_any = False

        for m in matches:
            # Use score presence as finished signal - MatchStatus is unreliable
            home_score = m.get("HomeTeamScore")
            away_score = m.get("AwayTeamScore")
            if home_score is None or away_score is None:
                continue
            # Skip if scores are 0-0 and match date is in the future
            from datetime import datetime, timezone
            match_date = m.get("Date", "")
            try:
                kickoff = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
                if kickoff > datetime.now(timezone.utc):
                    continue
            except Exception:
                continue

            id_match = str(m.get("IdMatch"))
            if not id_match:
                continue

            # Never overwrite an existing IdMatch entry
            if id_match in match_events:
                continue

            id_stage = m.get("IdStage")
            if not id_stage:
                continue

            # Fetch Timeline
            timeline_url = f"https://api.fifa.com/api/v3/timelines/{ID_COMPETITION}/{ID_SEASON}/{id_stage}/{id_match}?language=en-GB"
            tr = requests.get(timeline_url, headers=headers, timeout=15)
            if tr.status_code != 200:
                continue

            timeline_data = tr.json()

            # Resolve team codes & IDs
            home_obj = m.get("Home") or m.get("HomeTeam") or {}
            away_obj = m.get("Away") or m.get("AwayTeam") or {}
            
            home_team_id = home_obj.get("IdTeam")
            away_team_id = away_obj.get("IdTeam")
            
            home_code = home_obj.get("Abbreviation") or "HOME"
            away_code = away_obj.get("Abbreviation") or "AWAY"

            def resolve_team(id_team):
                if id_team == home_team_id:
                    return home_code
                if id_team == away_team_id:
                    return away_code
                return home_code  # Fallback



            # Parse timeline events
            events_list = []
            if isinstance(timeline_data, list):
                events_list = timeline_data
            elif isinstance(timeline_data, dict):
                events_list = (
                    timeline_data.get("Event") or
                    timeline_data.get("Events") or
                    timeline_data.get("Timeline") or
                    timeline_data.get("Results") or
                    []
                )

            goals = []
            yellow_cards = []
            red_cards = []
            subs = []

            def format_minute(min_val):
                if min_val is None:
                    return ""
                min_str = str(min_val).strip()
                if not min_str.endswith("'"):
                    return f"{min_str}'"
                return min_str

            for e in events_list:
                e_type = e.get("Type")
                if e_type is None:
                    continue

                team_id = e.get("IdTeam")
                team_code = resolve_team(team_id)
                player_id = str(e.get("IdPlayer") or e.get("PlayerId") or "")
                minute = format_minute(e.get("MatchMinute") or e.get("Minute"))

                # Type 0 = Goal
                if e_type == 0 or str(e_type) == "0":
                    goals.append({
                        "team": team_code,
                        "player_id": player_id,
                        "minute": minute,
                        "x": e.get("PositionX"),
                        "y": e.get("PositionY")
                    })
                # Type 2 = Yellow card
                elif e_type == 2 or str(e_type) == "2":
                    yellow_cards.append({
                        "team": team_code,
                        "player_id": player_id,
                        "minute": minute
                    })
                # Type 3 = Red card
                elif e_type == 3 or str(e_type) == "3":
                    red_cards.append({
                        "team": team_code,
                        "player_id": player_id,
                        "minute": minute
                    })
                # Type 5 = Substitution
                elif e_type == 5 or str(e_type) == "5":
                    subs.append({
                        "team": team_code,
                        "player_id": player_id,
                        "minute": minute
                    })

            match_events[id_match] = {
                "home": home_code,
                "away": away_code,
                "goals": goals,
                "yellow_cards": yellow_cards,
                "red_cards": red_cards,
                "subs": subs
            }
            updated_any = True
            print(f"Added match events for match {id_match}: {home_code} vs {away_code}")

        if updated_any:
            with open(events_path, "w", encoding="utf-8") as f:
                json.dump(match_events, f, separators=(',', ':'), ensure_ascii=False)
            print("Successfully wrote updated match events.")
        else:
            print("No new match events updated.")

        sys.exit(0)

    except Exception as e:
        print(f"Error in match bot: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_match_bot()
