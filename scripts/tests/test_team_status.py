import unittest
import sys
import os
from datetime import datetime, timezone

# Add project root directory to path to allow importing scripts.config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.config import (
    normalize_team_name,
    is_placeholder,
    get_match_outcome,
    is_confirmed_eliminated,
    resolve_team_statuses
)

class TestTeamStatus(unittest.TestCase):

    def test_normalize_team_name_case_insensitive(self):
        # Test original keys case insensitivity
        self.assertEqual(normalize_team_name("korea republic"), "South Korea")
        self.assertEqual(normalize_team_name("KOREA REPUBLIC"), "South Korea")
        self.assertEqual(normalize_team_name("côte d'ivoire"), "Ivory Coast")
        self.assertEqual(normalize_team_name("CÔTE D'IVOIRE"), "Ivory Coast")
        self.assertEqual(normalize_team_name("czechia"), "Czech Republic")
        self.assertEqual(normalize_team_name("CZECHIA"), "Czech Republic")
        # Test non-mapped names
        self.assertEqual(normalize_team_name("Brazil"), "Brazil")
        self.assertEqual(normalize_team_name("brazil"), "brazil")

    def test_is_placeholder(self):
        self.assertTrue(is_placeholder("W99"))
        self.assertTrue(is_placeholder("L102"))
        self.assertFalse(is_placeholder("Brazil"))
        self.assertFalse(is_placeholder("South Korea"))

    def test_get_match_outcome(self):
        # Home team wins in regular time
        match_1 = {
            "home_team": "Canada",
            "away_team": "South Africa",
            "result": {"ft": [2, 0]}
        }
        self.assertEqual(get_match_outcome("Canada", match_1), "win")
        self.assertEqual(get_match_outcome("South Africa", match_1), "loss")

        # Away team wins in penalties
        match_2 = {
            "home_team": "Germany",
            "away_team": "Paraguay",
            "result": {"p": [3, 4], "et": [1, 1], "ft": [1, 1]}
        }
        self.assertEqual(get_match_outcome("Germany", match_2), "loss")
        self.assertEqual(get_match_outcome("Paraguay", match_2), "win")

        # Draw match
        match_draw = {
            "home_team": "Canada",
            "away_team": "South Africa",
            "result": {"ft": [1, 1]}
        }
        self.assertEqual(get_match_outcome("Canada", match_draw), "draw")
        self.assertEqual(get_match_outcome("South Africa", match_draw), "draw")

        # Extra time win without penalties
        match_et = {
            "home_team": "Germany",
            "away_team": "Paraguay",
            "result": {"et": [2, 1], "ft": [1, 1]}
        }
        self.assertEqual(get_match_outcome("Germany", match_et), "win")
        self.assertEqual(get_match_outcome("Paraguay", match_et), "loss")

        # Invalid/empty result cases
        match_no_res = {
            "home_team": "Canada",
            "away_team": "South Africa",
            "result": None
        }
        self.assertIsNone(get_match_outcome("Canada", match_no_res))

        match_invalid_res1 = {
            "home_team": "Canada",
            "away_team": "South Africa",
            "result": {"ft": None}
        }
        self.assertIsNone(get_match_outcome("Canada", match_invalid_res1))

        match_invalid_res2 = {
            "home_team": "Canada",
            "away_team": "South Africa",
            "result": {"ft": [2]}
        }
        self.assertIsNone(get_match_outcome("Canada", match_invalid_res2))

    def test_is_confirmed_eliminated_group_stage_ongoing(self):
        # One group match completed, one group match unplayed
        fixtures = [
            {
                "home_team": "Mexico",
                "away_team": "South Africa",
                "stage": "Matchday 1",
                "kickoff_utc": "2026-06-11T19:00:00Z",
                "result": {"ft": [2, 0]}
            },
            {
                "home_team": "South Korea",
                "away_team": "Czech Republic",
                "stage": "Matchday 1",
                "kickoff_utc": "2026-06-12T02:00:00Z",
                "result": None
            }
        ]
        # Group stage is ongoing because there is an unplayed group match
        self.assertFalse(is_confirmed_eliminated("Mexico", fixtures))

    def test_is_confirmed_eliminated_group_stage_finished_gap_window(self):
        # All group matches completed.
        # Knockout matches are scheduled, but no team names have been resolved in them yet (bracket resolution has not started)
        fixtures = [
            {
                "home_team": "Mexico",
                "away_team": "South Africa",
                "stage": "Matchday 1",
                "kickoff_utc": "2026-06-11T19:00:00Z",
                "result": {"ft": [2, 0]}
            },
            {
                "home_team": "W74",
                "away_team": "W75",
                "stage": "Round of 16",
                "kickoff_utc": "2026-07-04T17:00:00Z",
                "result": None
            }
        ]
        # Mexico has finished group stage, but brackets haven't resolved.
        # They should NOT be confirmed eliminated yet.
        self.assertFalse(is_confirmed_eliminated("Mexico", fixtures))

    def test_is_confirmed_eliminated_group_stage_finished_confirmed_eliminated(self):
        # All group matches completed.
        # Knockout match has been populated with a resolved team name (bracket resolution has started).
        # Since Mexico is not in any knockout match, they are confirmed eliminated.
        fixtures = [
            {
                "home_team": "Mexico",
                "away_team": "South Africa",
                "stage": "Matchday 1",
                "kickoff_utc": "2026-06-11T19:00:00Z",
                "result": {"ft": [2, 0]}
            },
            {
                "home_team": "Canada",
                "away_team": "South Africa",
                "stage": "Round of 32",
                "kickoff_utc": "2026-06-28T19:00:00Z",
                "result": None
            }
        ]
        self.assertTrue(is_confirmed_eliminated("Mexico", fixtures))

    def test_is_confirmed_eliminated_knockout_winner_and_loser(self):
        fixtures = [
            {
                "home_team": "Brazil",
                "away_team": "Japan",
                "stage": "Round of 32",
                "kickoff_utc": "2026-06-29T17:00:00Z",
                "result": {"ft": [2, 1]}
            }
        ]
        # Japan lost a knockout match -> confirmed eliminated
        self.assertTrue(is_confirmed_eliminated("Japan", fixtures))
        # Brazil won a knockout match -> not eliminated
        self.assertFalse(is_confirmed_eliminated("Brazil", fixtures))

    def test_resolve_team_statuses(self):
        fixtures = [
            # Completed group match
            {
                "home_team": "Mexico",
                "away_team": "South Africa",
                "stage": "Matchday 1",
                "kickoff_utc": "2026-06-11T19:00:00Z",
                "result": {"ft": [2, 0]}
            },
            # Upcoming knockout match with resolved names
            {
                "home_team": "Canada",
                "away_team": "Norway",
                "stage": "Round of 32",
                "kickoff_utc": "2026-07-04T17:00:00Z",
                "result": None
            },
            # Placeholder knockout match
            {
                "home_team": "W74",
                "away_team": "W75",
                "stage": "Round of 16",
                "kickoff_utc": "2026-07-06T19:00:00Z",
                "result": None
            }
        ]
        now = datetime(2026, 6, 20, tzinfo=timezone.utc)
        normally_active, gap_window, skipped = resolve_team_statuses(fixtures, now)

        # Canada and Norway have upcoming resolved matches -> normally active
        self.assertIn("Canada", normally_active)
        self.assertIn("Norway", normally_active)

        # Mexico has finished group matches, bracket resolution has started (Canada/Norway are resolved), and Mexico is not in knockout -> skipped
        self.assertIn("Mexico", skipped)

        # South Africa has finished group matches, but wait! Are they in knockout? No.
        # Bracket resolution has started. So they are skipped.
        self.assertIn("South Africa", skipped)

        # Assert no placeholders like W74 or W75 are in any returned sets
        for s in [normally_active, gap_window, skipped]:
            for team in s:
                self.assertIsNotNone(team)
                self.assertFalse(team.startswith("W") and team[1:].isdigit(), f"Placeholder {team} should not be in status sets")
                self.assertFalse(team.startswith("L") and team[1:].isdigit(), f"Placeholder {team} should not be in status sets")

        # Assert sets are mutually exclusive
        self.assertEqual(normally_active & gap_window, set())
        self.assertEqual(normally_active & skipped, set())
        self.assertEqual(gap_window & skipped, set())

if __name__ == "__main__":
    unittest.main()
