from ast import arg
import logging
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List
from itertools import permutations
from tqdm import tqdm
import multiprocessing
import concurrent.futures


import argparse
import math

import json

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

def _process(data: dict, t: int = 1, k: int = 1, timeout: int = 30) -> list:
    raw = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=t) as executor:
        futures = [executor.submit(simulate_brawl, data, k) for _ in range(t)]
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            raw.extend(future.result())

    return raw

def get_stats(results):
    aggregated_results = defaultdict(list)
    for result in results:
        aggregated_results[result.win_id].append(result.damage)

    playerid = "1E93D5EFEEEB1BB5"
    keys = set(aggregated_results.keys()) - {playerid, None}
    win_damages = aggregated_results.get(playerid, [])
    tie_damages = aggregated_results.get(None, [])
    loss_damages = [] if not keys else aggregated_results[keys.pop()]

    win_percent = round(len(win_damages) / len(results) * 100, 2)
    tie_percent = round(len(tie_damages) / len(results) * 100, 2)
    loss_percent = round(len(loss_damages) / len(results) * 100, 2)

    return win_percent, tie_percent, loss_percent


def import_last_combat(json_path):
    with open(json_path) as f:
        return json.load(f)


def replace_arrangement(combat_data, playerid, arrangement):
    for i, char in enumerate(combat_data[playerid]['characters']):
        char['position'] = arrangement[i]
    return combat_data

def print_arrangement(combat_data, playerid):
    for char in combat_data[playerid]['characters']:
        print(char['id'], char['position'])

# testing the simulator
# combat_stats = simulate_brawl(SIM_DATA[0], k=1000)
# get_stats(combat_stats)


def test_simulator(combat_data, playerid, args):
    # testing with last_json data
    # print(combat_data[playerid]['characters'])
    combat_stats = simulate_brawl(combat_data, k=args.k)
    win_percent, tie_percent, loss_percent = get_stats(combat_stats)

    win_string = str(win_percent) + "%"
    tie_string = str(tie_percent) + "%"
    loss_string = str(loss_percent) + "%"
    # win_dmg_string = str(round(np.mean(win_damages), 1) if win_percent > 0 else 0)
    # loss_dmg_string = str(round(np.mean(loss_damages), 1) if loss_percent > 0 else 0)
    print("Win:", win_string, "Tie:", tie_string, "Loss:", loss_string)


def find_best_arrangement(args, playerid, combat_data):
    permutation = permutations(list(range(1, 8)), 7)
    results = {}
    i = 0
    best_win_percent = 0
    best_arrangement = None
# note could maybe use a heap to store the best arrangements
    for arrangement in tqdm(permutation, total=math.factorial(7)):
        i += 1
    # print(arrangement)
    # print(json.dumps(combat_data))
        combat_data = replace_arrangement(combat_data, playerid, arrangement)
    # print(json.dumps(combat_data))
    # break
        combat_stats = simulate_brawl(combat_data, k=args.k)
        win_percent, tie_percent, loss_percent = get_stats(combat_stats)
        if win_percent > best_win_percent:
            tqdm.write(f'New Best Arrangement: {arrangement}, {win_percent}%')
            best_win_percent = win_percent
            best_arrangement = arrangement
        results[arrangement] = [win_percent, tie_percent, loss_percent]
    # print_arrangement(combat_data, playerid)
    # if i > 2:
    #     break
    print(i)
    print(results)
    print(best_arrangement)
    print(best_win_percent)

parser = argparse.ArgumentParser()
parser.add_argument('-json', type=str, default='last_combat.json') # C:\Users\awlego\AppData\Roaming\SBBTracker\last_combat.json
parser.add_argument('-k', type=int, default=1000)
parser.add_argument('-log', type=str, default='ERROR')

args = parser.parse_args()

# oh interesting... the last_combat.json file hardcodes the power/toughness... so I move them around, buffs are not recalculated. Stuff like support, or Pup or Jack's Giant are not accounted for.
# 41% win 0.x tie 59% loss -- sbb tracker results when I ran this combat in game
playerid = "1E93D5EFEEEB1BB5"
combat_data = import_last_combat(args.json)



test_simulator(combat_data, playerid, args)
# find_best_arrangement(args, playerid, combat_data)

