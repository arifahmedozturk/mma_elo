from ELO.EloCalculator import EloCalculator
from reset_elos import reset_elos


def compute_accuracy():
    reset_elos()

    calculator = EloCalculator()
    calculator.start_elo_computation()

    correct_predictions = calculator.stats_helper.correct_predictions
    total_predictions = calculator.stats_helper.total_predictions
    ratio = 0 if total_predictions == 0 else correct_predictions / total_predictions

    print("CORRECT PREDICTIONS:", correct_predictions)
    print("TOTAL PREDICTIONS:", total_predictions)
    print("RATIO:", ratio)

    return {
        "correct_predictions": correct_predictions,
        "total_predictions": total_predictions,
        "ratio": ratio,
    }


if __name__ == "__main__":
    compute_accuracy()
