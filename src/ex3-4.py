# !/usr/bin/env python3
# coding: utf-8
from src.minority_game import MinorityGameWithStrategyTable
game = MinorityGameWithStrategyTable(201, 50000, 3, 2,64)
game.run_game()
print(game.winner_for_diff_group())