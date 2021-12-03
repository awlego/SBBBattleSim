import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe, StatChangeCause
from sbbbattlesim.spells import registry as spell_registry
from tests import make_character, make_player

@pytest.mark.parametrize('spell', spell_registry.keys())
def test_spell(spell):
    player = make_player(
        characters=[make_character(id='GENERIC', attack=1, position=1, keywords=[kw.value for kw in Keyword], tribes=[tribe.value for tribe in Tribe])],
        spells=[spell]
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)


def test_falling_stars():
    player = make_player(
        characters=[make_character()],
        spells=['''SBB_SPELL_FALLINGSTARS''',]
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p1.graveyard[0]
    assert char.stat_history[0].reason == StatChangeCause.FALLING_STARS


def test_lightning_bolt():
    player = make_player(
        spells=['''SBB_SPELL_LIGHTNINGBOLT''', ]
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=5, attack=1, health=10)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char.stat_history[0].reason == StatChangeCause.LIGHTNING_BOLT


def test_fire_ball():
    player = make_player(
        spells=['''SBB_SPELL_FIREBALL''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=2, health=4),
            make_character(position=5, health=4),
            make_character(position=6, health=5)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char.position == 2
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL

    char = board.p2.graveyard[1]
    assert char.position == 5
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL

    char = board.p2.characters[6]
    assert char.stat_history[0].reason == StatChangeCause.FIREBALL


def test_shrivel():
    player = make_player(
        spells=['''SBB_SPELL_ENFEEBLEMENT''', ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=4, health=13),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.characters[1]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.SHRIVEL
    assert char.attack == 0 and char.health == 1


def test_earthquake():
    player = make_player(
        spells=['''SBB_SPELL_EARTHQUAKE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=1, health=2),
            make_character(position=2, health=3),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.EARTHQUAKE

    char = board.p2.characters[2]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.EARTHQUAKE
    assert char.health == 1


def test_poison_apple():
    player = make_player(
        spells=['''SBB_SPELL_POISONAPPLE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(health=99),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.characters[1]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.POISON_APPLE
    assert char.health == 1

def test_disintegrate():
    player = make_player(
        spells=['''SBB_SPELL_DISINTEGRATE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(health=30),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.graveyard[0]
    assert char
    assert char.stat_history[0].reason == StatChangeCause.SMITE


def test_pigomorph():
    player = make_player(
        spells=['''SBB_SPELL_PIGOMORPH''', ]
    )
    enemy = make_player(
        characters=[
            make_character(),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    char = board.p2.characters[1]
    assert char
    assert char.id == 'SBB_CHARACTER_PIG'


def test_cats_call():
    player = make_player(
        characters=[make_character()],
        spells=['''SBB_SPELL_BEASTWITHIN''', ]
    )
    enemy = make_player(
        characters=[
            make_character(position=2),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    for i in range(1, 5):
        char = board.p1.characters[i]
        assert char
        assert char.id == 'Cat'


def test_toil_and_trouble():
    player = make_player(
        characters=[
            make_character(attack=0),
            make_character(position=2, attack=0),
        ],
        spells=['''SBB_SPELL_MENAGERIE''', ]
    )
    enemy = make_player(
        characters=[
            make_character(),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)

    for i in range(1, 3):
        char = board.p1.characters[i]
        assert char
        assert char.stat_history[0].reason == StatChangeCause.TOIL_AND_TROUBLE
