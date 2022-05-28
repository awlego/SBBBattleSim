import logging
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List

import numpy as np
from tests import PLAYER, make_character

from sbbbattlesim import fight
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.player import Player
from sbbbattlesim.stats import CombatStats

logger = logging.getLogger(__name__)

SIM_DATA = (
    {
        'PLAYER_ID': PLAYER | {
            'characters': [make_character(id='SBB_CHARACTER_FOXTAILARCHER', position=1),],
            # 'treasures': ['''SBB_TREASURE_HERMES'BOOTS''']
        },
        'ENEMY_ID': PLAYER | {
            'characters': [make_character(id='SBB_CHARACTER_FOXTAILARCHER', position=1),]
        }
    },

)

def simulate_brawl(data: dict, k: int) -> List[CombatStats]:
    logger.debug(f'Simulation Process Starting (k={k})')
    return [fight(*(Player(id=i, **d) for i, d in deepcopy(data).items()), limit=-1) for _ in range(k)]


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

    print("Win:", win_string, "Tie:", tie_string, "Loss:", loss_string, "Dmg:", win_dmg_string, loss_dmg_string)


combat_stats = simulate_brawl(SIM_DATA[0], k=1000)
get_stats(combat_stats)
