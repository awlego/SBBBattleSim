import pytest

from sbbbattlesim import Board
from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.utils import Keyword, Tribe, StatChangeCause
from tests import make_character, make_player


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('treasure', treasure_registry.keys())
def test_treasure(treasure, mimic, tiger):
    player = make_player(
        characters=[make_character(position=i, keywords=[kw for kw in Keyword], tribes=[tribe for tribe in Tribe]) for i
                    in range(1, 8)],
        treasures=[treasure]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character()],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
@pytest.mark.parametrize('num', (1, 2))
def test_easter_egg(mimic, tiger, on, num):
    treasures = [
        'SBB_TREASURE_EASTEREGG',
        'SBB_TREASURE_EASTEREGG',
    ]
    player = make_player(
        characters=[
            make_character(golden=True if on else False)
        ],
        treasures=treasures[:num]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    character = player.characters[1]

    mimic_multiplyer = [mimic, tiger].count(True) + 1
    stat_bonus = 3 * mimic_multiplyer

    assert (character.attack, character.health) == ((1+stat_bonus*num, 1+stat_bonus*num) if on else (1, 1))

@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('good', (True, False))
@pytest.mark.parametrize('evil', (True, False))
def test_book_of_heros(mimic, tiger, good, evil):
    starting_attack, starting_health = 1, 2

    player = make_player(
        characters=[
            make_character(health=starting_health, tribes=['good'] if good else [])
        ],
        treasures=[
            'SBB_TREASURE_BOOKOFHEROES',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='ENEMY', attack=0, tribes=['evil'] if evil else [])],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    good_character = player.characters[1]

    mimic_multiplyer = [mimic, tiger].count(True) + 1
    attack_bonus, health_bonus = 1 * mimic_multiplyer, 2 * mimic_multiplyer

    assert good_character
    assert good_character.attack == ((starting_attack + attack_bonus) if good and evil else starting_attack)
    assert good_character.health == ((starting_health + health_bonus) if good and evil else starting_health)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_corrupted_heartwood(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger])

    player = make_player(
        characters=[
            make_character(tribes=['animal'] if on else [])
        ],
        treasures=[
            'SBB_TREASURE_CORRUPTEDHEARTWOOD',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    animal = player.characters[1]

    assert animal
    assert animal.attack == (2 + mimic_multiplyer if on else animal.attack)
    assert animal.tribes == ({Tribe.ANIMAL, Tribe.EVIL} if on else set())


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_crown_of_atlas(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger])

    player = make_player(
        characters=[
            make_character(tribes=['animal'] if on else [])
        ],
        treasures=[
            'SBB_TREASURE_CROWNOFATLAS',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    animal = player.characters[1]

    assert animal
    assert animal.attack == (2 + mimic_multiplyer if on else 1)
    assert animal.health == (2 + mimic_multiplyer if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_dragon_nest(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger])

    player = make_player(
        characters=[
            make_character(tribes=['dragon'] if on else [])
        ],
        treasures=[
            'SBB_TREASURE_DRAGONNEST',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    animal = player.characters[1]

    assert animal
    assert animal.attack == (1 + 5 + (5 * mimic_multiplyer) if on else 1)
    assert animal.health == (1 + 5 + (5 * mimic_multiplyer) if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_fountain_of_youth(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger])

    player = make_player(
        characters=[
            make_character()
        ],
        treasures=[
            'SBB_TREASURE_FOUNTAINOFYOUTH',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.health == 1 + 1 + mimic_multiplyer


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_jacks_jumping_beans(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger])

    player = make_player(
        characters=[
            make_character()
        ],
        treasures=[
            '''SBB_TREASURE_JACK'SJUMPINGBEANS''',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == 1 + 4 + (4 * mimic_multiplyer)
    assert char.health == 1 + 4 + (4 * mimic_multiplyer)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_monster_manual(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(attack=0, tribes=['monster'] if on else [])
        ],
        treasures=[
            'SBB_TREASURE_MONSTERMANUAL',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy')]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.graveyard[0]

    assert char
    assert char.attack == ((2 * mimic_multiplyer) if on else 0)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_noble_steed(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CINDER-ELLA' if on else '')
        ],
        treasures=[
            'SBB_TREASURE_QUESTINGPET',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(attack=0, id='Enemy')]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == (1 + (1 * mimic_multiplyer) if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_ring_of_meteors(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(health=mimic_multiplyer, position=1),
            make_character(health=mimic_multiplyer + 1, position=2)

        ],
        treasures=[
            'SBB_TREASURE_RINGOFMETEORS',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy')]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    assert not player.characters[1]
    assert player.characters[2]


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_needle_nose_dagger(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character()
        ],
        treasures=[
            'SBB_TREASURE_RUSTYDAGGERS',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == 1 + (2 * mimic_multiplyer)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_dancing_sword(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character()
        ],
        treasures=[
            'SBB_TREASURE_SHARPENINGSTONE',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == 1 + (1 * mimic_multiplyer)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_shepherds_sling(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PRINCESSPEEP'),
            make_character(id='SBB_CHARACTER_COPYCAT', position=2)
        ],
        treasures=[
            '''SBB_TREASURE_SHEPHERD'SSLING''',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == 1 + (1 * mimic_multiplyer)
    assert char.health == 1 + (1 * mimic_multiplyer)

    unbuffed = player.characters[2]

    assert unbuffed
    assert unbuffed.attack == 1
    assert unbuffed.health == 1


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_ancient_sarcophagus(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(tribes=['evil'] if on else [], attack=0),
        ],
        treasures=[
            'SBB_TREASURE_ANCIENTSARCOPHAGUS',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=1, position=i) for i in range(1, mimic_multiplyer + 1)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    enemy = board.p2
    assert (not enemy.valid_characters() if on else enemy.valid_characters())


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_bad_moon(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_QUESTINGPRINCESS' if on else '', ),
        ],
        treasures=[
            'SBB_TREASURE_BADMOON',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == (1 + (1 * mimic_multiplyer) if on else 1)
    assert char.health == (1 + (2 * mimic_multiplyer) if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_deepstone_mine(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(tribes=['dwarf'] if on else []),
        ],
        treasures=[
            'SBB_TREASURE_BOUNTIFULMINE',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == (1 + (2 * mimic_multiplyer) if on else 1)
    assert char.health == (1 + (2 * mimic_multiplyer) if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
@pytest.mark.parametrize('unit', ('SBB_CHARACTER_NIGHTSTALKER', 'SBB_CHARACTER_QUESTINGPRINCESS'))
@pytest.mark.parametrize('golden', (True, False))
def test_cloak_of_the_assassin(mimic, tiger, on, unit, golden):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(id=unit if on else '', golden=golden),
        ],
        treasures=[
            'SBB_TREASURE_CLOAKOFTHEASSASSIN',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char

    if on and unit == 'SBB_CHARACTER_QUESTINGPRINCESS' and golden:
        assert char.attack == 1, char.attack
        assert char.health == 1, char.health
    elif unit in ['SBB_CHARACTER_QUESTINGPRINCESS', 'SBB_CHARACTER_NIGHTSTALKER']:
        final_stats = 1 + (3 * mimic_multiplyer) if on else 1
        assert char.attack == final_stats, (char.attack, final_stats)
        assert char.health == final_stats, (char.health, final_stats)
    else:
        raise ValueError('bad unit')


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_eye_of_ares(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_EYEOFARES',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy')]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    for player in [board.p1, board.p2]:
        dead = player.graveyard[0]

        assert dead
        assert dead.attack == 1 + (5 * mimic_multiplyer)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_power_orb(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_POWERSTONE',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == 1 + (1 * mimic_multiplyer)
    assert char.health == 1 + (1 * mimic_multiplyer)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
def test_ring_of_revenge(mimic, tiger):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(position=1),
            make_character(position=5),
        ],
        treasures=[
            'SBB_TREASURE_RINGOFREVENGE',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character()],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[5]

    assert char.attack == 1 + (1 * mimic_multiplyer)
    assert char.health == 1 + (1 * mimic_multiplyer)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_sting(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(position=1 if on else 2),
        ],
        treasures=[
            'SBB_TREASURE_STING',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1 if on else 2]

    assert char.attack == (1 + (10 * mimic_multiplyer) if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_haunted_helm(mimic, tiger, on):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(position=1 if on else 2),
        ],
        treasures=[
            'SBB_TREASURE_STONEHELM',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1 if on else 2]

    assert char.health == (1 + (10 * mimic_multiplyer) if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('tiger', (True, False))
@pytest.mark.parametrize('ranged', (True, False))
@pytest.mark.parametrize('back', (True, False))
def test_tell_tale_quiver(mimic, tiger, ranged, back):
    mimic_multiplyer = sum([mimic, tiger]) + 1

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FOXTAILARCHER' if ranged else '', position=5 if back else 1),
        ],
        treasures=[
            'SBB_TREASURE_TELLTALEQUIVER',
        ]
    )

    if tiger:
        player['hero'] = 'SBB_HERO_THECOLLECTOR'

    if mimic:
        player['treasures'].append('SBB_TREASURE_TREASURECHEST')

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[5 if back else 1]

    assert char.attack == (1 + (3 * mimic_multiplyer) if ranged and back else 1)
    assert char.health == (1 + (3 * mimic_multiplyer) if ranged and back else 1)


@pytest.mark.parametrize('_', range(20))
@pytest.mark.parametrize('mimic', (True, False))
def test_deck_of_many_things(mimic, _):
    #todo test level cast is correct
    player = make_player(
        hero='SBB_HERO_MERLIN',
        level=6,
        characters=[
            make_character(attack=100, health=100),
        ],
        treasures=[
            'SBB_TREASURE_DECKOFMANYTHINGS',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    wizardbuffs = [
        r for r in board.p1.characters[1]._action_history if r.reason == StatChangeCause.MERLIN_BUFF
    ]

    if mimic:
        assert len(wizardbuffs) == 2
    else:
        assert len(wizardbuffs) == 1



@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_other_hand_of_vekna(mimic, on):
    player = make_player(
        characters=[
            make_character(position=1),
            make_character(position=2 if on else 5),
        ],
        treasures=[
            'SBB_TREASURE_JUMPINGJACKS',
            'SBB_TREASURE_TREASURECHEST' if mimic else '',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    enemy = make_player(
        characters=[make_character()],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.valid_characters()[0]

    assert char
    final = 2
    if mimic:
        final = 3
    assert char.attack == (final if on else 1)
    assert char.health == (final if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('real_unit', (True, False))
def test_coin_of_charon(mimic, real_unit):
    player = make_player(
        characters=[
            make_character(),
            make_character(id="SBB_CHARACTER_WIZARD" if real_unit else "", position=5)
        ],
        treasures=[
            '''SBB_TREASURE_MONKEY'SPAW''',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(), make_character(position=2)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    fake_unit = board.p1.characters[1]
    assert fake_unit

    maybe_real_unit = board.p1.characters[5]
    assert maybe_real_unit

    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert fake_unit.dead
    assert maybe_real_unit.dead

    final_stats = (9, 9) if mimic else (5, 5)
    assert (fake_unit.attack, fake_unit.health + fake_unit._damage) == (1, 1)
    assert (maybe_real_unit.attack, maybe_real_unit.health + fake_unit._damage) == (final_stats if real_unit else (1, 1))


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('full_board', (True, False))
def test_reduplicator(mimic, full_board):

    characters = [
        make_character(id="SBB_CHARACTER_BLACKCAT", position=1, health=1),
        make_character(position=4, health=5),
        make_character(position=5, health=5),
        make_character(position=6, health=5),
        make_character(position=7, health=5),
    ]

    if full_board:
        characters.append(make_character(position=2, health=5))
        characters.append(make_character(position=3, health=5))

    player = make_player(
        characters=characters,
        treasures=[
            'SBB_TREASURE_REDUPLICATOR',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        spells=[
            "SBB_SPELL_EARTHQUAKE"
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char1 = player.characters[1]
    char2 = player.characters[2]
    char3 = player.characters[3]

    triggered = player.treasures['SBB_TREASURE_REDUPLICATOR'][0].triggered
    cat_id = 'SBB_CHARACTER_CAT'
    assert char1.id == cat_id
    if mimic and full_board:
        assert char2
        assert char3
        assert char3.id != cat_id
        assert char2.id != cat_id
        assert not triggered
    elif not mimic and full_board:
        assert char3
        assert char3.id != cat_id
        assert char2
        assert char2.id != cat_id
        assert not triggered
    elif mimic and not full_board:
        assert char2
        assert char2.id == cat_id
        assert char3
        assert char3.id == cat_id
        assert triggered
    elif not mimic and not full_board:
        assert char2
        assert char2.id == cat_id
        assert triggered
        assert char3 is None
    else:
        raise ValueError('Nonsense state')



@pytest.mark.parametrize('mimic', (True, False))
def test_moonsong_horn(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_POWERGEM',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char

    final = 2
    if mimic:
        final = 3

    assert char.attack == final
    assert char.health == final


@pytest.mark.parametrize('mimic', (True, False))
def test_six_of_shields(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_RINGOFDISCIPLINE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char

    final = 4
    if mimic:
        final = 7

    assert char.health == final


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_sky_castle(mimic, on):
    player = make_player(
        characters=[
            make_character(tribes=[Tribe.PRINCE] if on else []),
            make_character(tribes=[Tribe.PRINCESS] if on else [], position=2),
        ],
        treasures=[
            'SBB_TREASURE_SKYCASTLE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    for char in [player.characters[1], player.characters[2]]:
        assert char

        final = 5
        if mimic:
            final = 9

        assert char.attack == (final if on else 1)
        assert char.health == (final if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
def test_summoning_portal(mimic):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT'),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=2),
        ],
        treasures=[
            'SBB_TREASURE_SUMMONINGCIRCLE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
        spells=['SBB_SPELL_EARTHQUAKE']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    first_cat = player.characters[1]

    assert first_cat

    final = 3
    if mimic:
        final = 5

    assert first_cat.attack == final
    assert first_cat.health == final

    second_cat = player.characters[2]

    assert second_cat

    final = 2
    if mimic:
        final = 3

    assert second_cat.attack == final
    assert second_cat.health == final


@pytest.mark.parametrize('mimic', (True, False))
def test_ring_of_rage(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_SURGINGSTONE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char

    final = 4
    if mimic:
        final = 7

    assert char.attack == final


def test_tree_of_life():
    player = make_player(
        characters=[
            make_character(health=2),
            make_character(health=2, position=2),
        ],
        treasures=[
            'SBB_TREASURE_CIRCLEOFLIFE',
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=1, health=2)],
        spells=['SBB_SPELL_FALLINGSTARS']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.valid_characters()[0]

    assert char
    assert char.health == 2


@pytest.mark.parametrize('mimic', (True, False))
def test_draculas_saber(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            '''SBB_TREASURE_DRACULA'SSABER''',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char

    if mimic:
        assert char.attack == 5
        assert char.health == 3
    else:
        assert char.attack == 3
        assert char.health == 2


@pytest.mark.parametrize('mimic', (True, False))
def test_exploding_mittens(mimic):
    player = make_player(
        characters=[
            make_character(attack=0),
        ],
        treasures=[
            'SBB_TREASURE_EXPLODINGMITTENS',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    enemy = board.p2

    assert not enemy.valid_characters()


@pytest.mark.parametrize('mimic', (True, False))
def test_helm_of_the_ugly_gosling(mimic):
    player = make_player(
        characters=[
            make_character(position=1),
            make_character(position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HELMOFTHEUGLYGOSLING''',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char

    assert char.attack == 16
    assert char.health == 16

    if mimic:
        char = player.characters[2]

        assert char.attack == 16
        assert char.health == 16


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('trigger', (True, False))
def test_monkeys_paw(trigger, mimic):
    player = make_player(
        characters=[
            make_character(position=i) for i in range(7 - trigger)
        ],
        treasures=[
            'SBB_TREASURE_HEXINGWAND',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1

    for char in player.valid_characters():
        if not trigger:
            assert char.attack == 1 and char.health == 1
        else:
            if mimic:
                assert char.attack == 13 and char.health == 13
            else:
                assert char.attack == 7 and char.health == 7


@pytest.mark.parametrize('mimic', (True, False))
def test_sword_of_fire_and_ice(mimic):
    player = make_player(
        characters=[
            make_character(position=1),
            make_character(position=5)

        ],
        treasures=[
            'SBB_TREASURE_SWORDOFFIREANDICE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    front = player.characters[1]
    assert front
    back = player.characters[5]
    assert back

    buff = 12 if mimic else 6

    assert front.health == 1 + buff
    assert front.attack == 1
    assert back.health == 1
    assert back.attack == 1 + buff


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_ninth_book_of_merlin(mimic, on):
    player = make_player(
        level=5,
        characters=[
            make_character(tribes=['mage']),
            make_character(position=5),
            make_character(id='SBB_CHARACTER_WIZARD', position=6, attack=1, health=5),
        ],
        treasures=[
            'SBB_TREASURE_THENINTHBOOKOFMERLIN',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=1 if on else 0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    mage = player.characters[1]
    not_mage = player.characters[5]

    if on:
        for pos in [6]:
            wizardbuffs = [
                r for r in board.p1.characters[pos]._action_history if r.reason == StatChangeCause.WIZARDS_FAMILIAR
            ]

            assert len(wizardbuffs) == 2 if mimic else 1

    else:
        assert mage
        assert not_mage

        assert mage.last_breath
        assert len([evt for evt in mage.get('OnDeath') if evt.last_breath]) == 1 + mimic

        assert not not_mage.last_breath
        assert len([evt for evt in not_mage.get('OnDeath') if evt.last_breath]) == 0


@pytest.mark.parametrize('mimic', (True, False))
def test_ivory_owl(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_IVORYOWL',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    buff = 2 * (1 + mimic)

    assert char
    assert char.attack == 1 + buff
    assert char.health == 1 + buff


@pytest.mark.parametrize('mimic', (True, False))
def test_spear_of_achilies(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_SPEAROFACHILLES',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    buff = 7 * (1 + mimic)

    assert char
    assert char.attack == 1 + buff
    assert char.health == 1 + buff


@pytest.mark.parametrize('mimic', (True, False))
def test_fairy_queens_wand(mimic):
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=[
            'SBB_TREASURE_FAIRYQUEENSWAND',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(id='Enemy', attack=0)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    buff = 10 if mimic else 5

    assert char
    assert char.attack == 1 + buff
    assert char.health == 1 + buff


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_magic_sword_100(mimic, on):
    player = make_player(
        characters=[
            make_character(position=1 if on else 5),
        ],
        treasures=[
            'SBB_TREASURE_MAGICSWORD+100',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1 if on else 5]

    buff = 200 if mimic else 100

    assert char.attack == (1 + buff if on else 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_mirror_mirror(mimic, on):
    player = make_player(
        characters=[
            make_character(position=1 if on else 5),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character()],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1 if on else 5]

    if on:
        assert char
        assert char.attack == 1
        assert char.health == 1

        if mimic:
            char = player.characters[2]

            assert char
            assert char.attack == 1
            assert char.health == 1
    else:
        assert char is None


@pytest.mark.parametrize('mimic', (True, False))
def test_round_table(mimic):
    player = make_player(
        characters=[
            make_character(attack=0),
        ],
        treasures=[
            'SBB_TREASURE_THEROUNDTABLE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    char = player.characters[1]

    assert char
    assert char.attack == 1


@pytest.mark.parametrize('mimic', (True, False))
def test_round_table_echowood(mimic):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=11, health=1, position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=1, health=1, position=2),
        ],
        treasures=[
            'SBB_TREASURE_THEROUNDTABLE',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    player = board.p1
    e1 = player.characters[1]
    e2 = player.characters[2]

    if mimic:
        assert (e1.attack, e1.health) == (21, 11)
    else:
        assert (e1.attack, e1.health) == (11, 11)

    if mimic:
        assert (e2.attack, e2.health) == (11, 11)
    else:
        assert (e2.attack, e2.health) == (1, 11)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_phoenix_feather(mimic, on):
    player = make_player(
        characters=[
            make_character(attack=5 if on else 1),
            make_character(attack=1 if on else 5, position=5)
        ],
        treasures=[
            'SBB_TREASURE_PHOENIXFEATHER',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character()],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    player = board.p1
    p1char = player.characters[1]

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if on:
        assert player.characters[1]
        assert player.characters[1] is p1char

        if mimic:
            assert player.characters[2]
            assert player.characters[2] is not p1char

        assert player.characters[5] is not None

    else:
        assert player.characters[1] is None
        assert player.characters[5] is not None


@pytest.mark.parametrize('mimic', (True, False))
def test_spear_of_achilles(mimic):
    player = make_player(
        characters=[
            make_character()
        ],
        treasures=[
            'SBB_TREASURE_SPEAROFACHILLES',
            'SBB_TREASURE_TREASURECHEST' if mimic else ''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=0)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    player = board.p1
    p1char = player.characters[1]

    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (player.characters[1].attack, player.characters[1].health) == (15, 15) if mimic else (8, 8)
