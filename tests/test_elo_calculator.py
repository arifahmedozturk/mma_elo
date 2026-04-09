import pytest
from unittest.mock import patch


@pytest.fixture
def calculator():
    with patch('psycopg2.connect'):
        from ELO.EloCalculator import EloCalculator
        return EloCalculator()


def make_fight(fighter, opponent):
    return {'fighter': fighter, 'opponent': opponent, 'result': 'Win',
            'method': 'Decision', 'date': '2020-01-01', 'event': 'UFC 1'}


class TestRemoveDuplicateMatches:
    def test_removes_reverse_duplicate(self, calculator):
        fights = [
            make_fight("Jon Jones", "Stipe Miocic"),
            make_fight("Stipe Miocic", "Jon Jones"),  # reverse duplicate
        ]
        result = calculator.remove_duplicate_matches(fights)
        assert len(result) == 1

    def test_keeps_distinct_fights(self, calculator):
        fights = [
            make_fight("Jon Jones", "Stipe Miocic"),
            make_fight("Khabib Nurmagomedov", "Conor McGregor"),
        ]
        result = calculator.remove_duplicate_matches(fights)
        assert len(result) == 2

    def test_keeps_first_occurrence(self, calculator):
        fights = [
            make_fight("Jon Jones", "Stipe Miocic"),
            make_fight("Stipe Miocic", "Jon Jones"),
        ]
        result = calculator.remove_duplicate_matches(fights)
        assert result[0]['fighter'] == "Jon Jones"

    def test_empty_input(self, calculator):
        assert calculator.remove_duplicate_matches([]) == []

    def test_single_fight_unchanged(self, calculator):
        fights = [make_fight("Jon Jones", "Stipe Miocic")]
        assert calculator.remove_duplicate_matches(fights) == fights


class TestComputeAccuracy:
    def test_correct_when_higher_elo_fighter_wins(self, calculator):
        fighter = {'elo': 1600}
        opponent = {'elo': 1400}
        fight = {'result': 'Win'}

        result = calculator.compute_accuracy(fighter, opponent, fight)

        assert result is True
        assert calculator.stats_helper.correct_predictions == 1
        assert calculator.stats_helper.total_predictions == 1

    def test_incorrect_when_higher_elo_fighter_loses(self, calculator):
        fighter = {'elo': 1600}
        opponent = {'elo': 1400}
        fight = {'result': 'Loss'}

        result = calculator.compute_accuracy(fighter, opponent, fight)

        assert result is False
        assert calculator.stats_helper.correct_predictions == 0
        assert calculator.stats_helper.total_predictions == 1

    def test_ignores_non_win_loss_results(self, calculator):
        fighter = {'elo': 1600}
        opponent = {'elo': 1400}
        fight = {'result': 'Draw'}

        result = calculator.compute_accuracy(fighter, opponent, fight)

        assert result is None
        assert calculator.stats_helper.correct_predictions == 0
        assert calculator.stats_helper.total_predictions == 0
