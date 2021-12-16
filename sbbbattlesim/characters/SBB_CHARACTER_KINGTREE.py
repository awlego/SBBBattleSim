from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe


class AshwoodElmOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        base_attack_change = self.ashwood.health
        modifier = 2 if self.ashwood.golden else 1
        attack_change = base_attack_change * modifier

        Buff(reason=ActionReason.ASHWOOD_ELM_BUFF, source=self.ashwood,
             targets=self.ashwood.player.valid_characters(_lambda=lambda char: Tribe.TREANT in char.tribes),
             attack=attack_change, temp=False, stack=stack).resolve()

class CharacterType(Character):
    display_name = 'Ashwood Elm'

    _attack = 0
    _health = 20
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player.board.register(AshwoodElmOnStart, priority=70, ashwood=self)
