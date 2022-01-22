import logging

import pytest
from collections import defaultdict
from typing import Dict, List
import numpy as np
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
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=1, attack=10, health=10),
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=2, attack=10, health=10),
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=3, attack=10, health=10),
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=4, attack=10, health=10),
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=5, attack=10, health=10),
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=6, attack=10, health=10),
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=7, attack=10, health=10)
    ],
    level=6
)
enemy = make_player(
    raw=True,
    characters=[
        make_character(id='SBB_CHARACTER_DOOMBREATH', position=1, attack=10, health=10)
    ],
    # treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
    level=6
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


results = simulate_brawl(board, k=1000)
# print(results)

def get_stats(results):
    aggregated_results = defaultdict(list)
    for result in results:
        aggregated_results[result.win_id].append(result.damage)

    playerid = 9
    keys = set(aggregated_results.keys()) - {playerid, None}
    win_damages = aggregated_results.get(playerid, [])
    tie_damages = aggregated_results.get(None, [])
    loss_damages = [] if not keys else aggregated_results[keys.pop()]

    win_percent = round(len(win_damages) / len(results) * 100, 2)
    tie_percent = round(len(tie_damages) / len(results) * 100, 2)
    loss_percent = round(len(loss_damages) / len(results) * 100, 2)

    win_string = str(win_percent) + "%"
    tie_string = str(tie_percent) + "%"
    loss_string = str(loss_percent) + "%"
    win_dmg_string = str(round(np.mean(win_damages), 1) if win_percent > 0 else 0)
    loss_dmg_string = str(round(np.mean(loss_damages), 1) if loss_percent > 0 else 0)

    print(win_string, tie_string, loss_string, win_dmg_string, loss_dmg_string)

get_stats(results)
