import logging

import pytest
from typing import Dict, List

from sbbbattlesim import Board
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import ActionReason
from sbbbattlesim.player import Player
# from sbbbattlesim.simulate import _process, simulate_brawl
from sbbbattlesim.stats import calculate_stats, BoardStats


from tests import make_character, make_player

logger = logging.getLogger(__name__)


player = make_player(
    raw=True,
    characters=[
        make_character(id='SBB_CHARACTER_TROJANDONKEY', position=1, attack=1, health=2)
    ],
    level=3
)
enemy = make_player(
    raw=True,
    characters=[
        make_character(id='SBB_CHARACTER_TROJANDONKEY', position=1, attack=1, health=2)
    ],
    treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
    level=3
)
board = Board({'PLAYER': player, 'ENEMY': enemy})
# winner, loser = board.fight()

# player = board.p1

# print(Player.pretty_print(winner))
# print(Player.pretty_print(loser))


def simulate_brawl(board: Board, k: int) -> List[BoardStats]:
    logger.debug(f'Simulation Process Starting (k={k})')
    results = []
    for _ in range(k):
        board.fight(limit=100)
        results.append(calculate_stats(board))

    return results


results = simulate_brawl(board, k=10)
print(results)

# pretty_print(player)