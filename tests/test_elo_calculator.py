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
