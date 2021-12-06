import random

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import random_start_combat_spell


class DeckOfManyThingsOnStart(OnStart):
    def handle(self, *args, **kwargs):
        for _ in range(bool(self.deck.mimic) + 1):
            spell = random_start_combat_spell(self.player.level)
            if spell:
                self.player.cast_spell(spell.id)


# todo can only cast spells of current level or below
class TreasureType(Treasure):
    display_name = 'Deck of Many Things'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(DeckOfManyThingsOnStart, deck=self, player=self.player)
