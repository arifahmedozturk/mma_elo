import pytest
from ELO.StatsHelper import StatsHelper


@pytest.fixture
def stats():
    return StatsHelper()


def make_fighter(elo):
    return {'elo': elo}


def make_fight(result):
    return {'result': result}


class TestLogFight:
    def test_correct_prediction_favourite_wins(self, stats):
        stats.log_fight(make_fighter(1600), make_fighter(1400), make_fight('Win'))
        assert stats.correct_predictions == 1
        assert stats.total_predictions == 1

    def test_correct_prediction_underdog_loses(self, stats):
        stats.log_fight(make_fighter(1400), make_fighter(1600), make_fight('Loss'))
        assert stats.correct_predictions == 1

    def test_incorrect_prediction_upset(self, stats):
        stats.log_fight(make_fighter(1600), make_fighter(1400), make_fight('Loss'))
        assert stats.correct_predictions == 0
        assert stats.total_predictions == 1

    def test_equal_elo_win_counts_as_correct(self, stats):
        stats.log_fight(make_fighter(1500), make_fighter(1500), make_fight('Win'))
        assert stats.correct_predictions == 1

    def test_cumulative_accuracy(self, stats):
        stats.log_fight(make_fighter(1600), make_fighter(1400), make_fight('Win'))   # correct
        stats.log_fight(make_fighter(1600), make_fighter(1400), make_fight('Win'))   # correct
        stats.log_fight(make_fighter(1600), make_fighter(1400), make_fight('Loss'))  # wrong
        assert stats.correct_predictions == 2
        assert stats.total_predictions == 3
