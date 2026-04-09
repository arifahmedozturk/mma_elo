from ELO.EloCalculator import EloCalculator
from reset_elos import reset_elos

reset_elos()

e = EloCalculator()
e.start_elo_computation()