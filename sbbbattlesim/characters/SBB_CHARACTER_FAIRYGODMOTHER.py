import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class FairyGodmotherOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.fairy_godmother.golden else 2
        targets = self.manager.player.valid_characters(_lambda=lambda char: Tribe.GOOD in char.tribes)
        Buff(reason=ActionReason.FAIRY_GODMOTHER_BUFF, source=self.manager, targets=targets,
             health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Fairy Godmother'
    aura = True

    _attack = 4
    _health = 4
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.FAIRY}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, echo_wood=self, event=FairyGodmotherOnDeath, fairy_godmother=self,
                                   _lambda=lambda char: Tribe.GOOD in char.tribes)

    
