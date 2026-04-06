import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def helper():
    with patch('psycopg2.connect'):
        from ELO.EloHelper import EloHelper
        h = EloHelper()
        h.FighterDB = MagicMock()
        return h


class TestGetResultScore:
    def test_win_decision(self, helper):
        fighter_score, opponent_score = helper.get_result_score("Win", "Decision (unanimous)")
        assert fighter_score == 1
        assert opponent_score == 0

    def test_loss_decision(self, helper):
        fighter_score, opponent_score = helper.get_result_score("Loss", "Decision (unanimous)")
        assert fighter_score == 0
        assert opponent_score == 1

    def test_win_split_decision(self, helper):
        fighter_score, opponent_score = helper.get_result_score("Win", "Decision (split)")
        assert fighter_score == 0.67
        assert opponent_score == 0.33

    def test_loss_split_decision(self, helper):
        fighter_score, opponent_score = helper.get_result_score("Loss", "Decision (split)")
        assert fighter_score == 0.33
        assert opponent_score == 0.67

    def test_draw(self, helper):
        assert helper.get_result_score("Draw", "") == (0.5, 0.5)

    def test_no_contest(self, helper):
        assert helper.get_result_score("NC", "") == (0.5, 0.5)

    def test_win_ko(self, helper):
        fighter_score, opponent_score = helper.get_result_score("Win", "KO/TKO")
        assert fighter_score == 1
        assert opponent_score == 0


class TestGetResultPenalty:
    def test_ko_loss_applies_penalty(self, helper):
        fighter_penalty, opponent_penalty = helper.get_result_penalty("Loss", "KO/TKO")
        assert fighter_penalty == -25
        assert opponent_penalty == 0

    def test_ko_win_no_penalty_for_winner(self, helper):
        fighter_penalty, opponent_penalty = helper.get_result_penalty("Win", "KO/TKO")
        assert fighter_penalty == 0
        assert opponent_penalty == -25

    def test_decision_no_penalty(self, helper):
        assert helper.get_result_penalty("Win", "Decision (unanimous)") == (0, 0)
        assert helper.get_result_penalty("Loss", "Decision (unanimous)") == (0, 0)

    def test_submission_no_penalty(self, helper):
        assert helper.get_result_penalty("Loss", "Submission") == (0, 0)


class TestGetAgePenalty:
    def test_none_dob_returns_zero(self, helper):
        penalty, new_date = helper.get_age_penalty_and_new_date(None, "2020-01-01")
        assert penalty == 0
        assert new_date is None

    def test_no_years_crossed(self, helper):
        # fight is before the penalty date — no penalty
        penalty, new_date = helper.get_age_penalty_and_new_date("2021-01-01", "2020-06-01")
        assert penalty == 0
        assert new_date == "2021-01-01"

    def test_one_year_crossed(self, helper):
        penalty, new_date = helper.get_age_penalty_and_new_date("2020-01-01", "2020-06-01")
        assert penalty == -50
        assert new_date == "2021-01-01"

    def test_multiple_years_crossed(self, helper):
        # fight_date crosses penalty_date thresholds at 2019-01-01, 2020-01-01, 2021-01-01 → 3 × 50
        penalty, new_date = helper.get_age_penalty_and_new_date("2019-01-01", "2021-06-01")
        assert penalty == -150
        assert new_date == "2022-01-01"


class TestGetEloChanges:
    def _make_fighter(self, elo, last_age_penalty=None):
        return {'name': 'Fighter A', 'elo': elo, 'last_age_penalty': last_age_penalty}

    def _make_opponent(self, elo, last_age_penalty=None):
        return {'name': 'Fighter B', 'elo': elo, 'last_age_penalty': last_age_penalty}

    def _make_fight(self, result, method="Decision (unanimous)", date="2020-01-01"):
        return {'result': result, 'method': method, 'date': date}

    def test_equal_elo_win_gains_points(self, helper):
        fighter = self._make_fighter(1500)
        opponent = self._make_opponent(1500)
        fighter_delta, opponent_delta = helper.get_elo_changes(fighter, opponent, self._make_fight("Win"))
        assert fighter_delta > 0
        assert opponent_delta < 0
        assert fighter_delta == -opponent_delta

    def test_equal_elo_loss_loses_points(self, helper):
        fighter = self._make_fighter(1500)
        opponent = self._make_opponent(1500)
        fighter_delta, opponent_delta = helper.get_elo_changes(fighter, opponent, self._make_fight("Loss"))
        assert fighter_delta < 0
        assert opponent_delta > 0

    def test_ko_loss_extra_penalty(self, helper):
        fighter = self._make_fighter(1500)
        opponent = self._make_opponent(1500)
        decision_delta, _ = helper.get_elo_changes(fighter, opponent, self._make_fight("Loss", "Decision (unanimous)"))
        ko_delta, _ = helper.get_elo_changes(fighter, opponent, self._make_fight("Loss", "KO/TKO"))
        assert ko_delta < decision_delta

    def test_upset_win_gains_more_points(self, helper):
        underdog = self._make_fighter(1300)
        favourite = self._make_opponent(1700)
        underdog_delta, _ = helper.get_elo_changes(underdog, favourite, self._make_fight("Win"))

        expected_delta, _ = helper.get_elo_changes(
            self._make_fighter(1500), self._make_opponent(1500), self._make_fight("Win")
        )
        assert underdog_delta > expected_delta

    def test_expected_win_gains_fewer_points(self, helper):
        favourite = self._make_fighter(1700)
        underdog = self._make_opponent(1300)
        favourite_delta, _ = helper.get_elo_changes(favourite, underdog, self._make_fight("Win"))

        even_delta, _ = helper.get_elo_changes(
            self._make_fighter(1500), self._make_opponent(1500), self._make_fight("Win")
        )
        assert favourite_delta < even_delta
