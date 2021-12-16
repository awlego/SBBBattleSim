import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Cloak of the Assassin'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stats = 3 * (self.mimic + 1)
        self.aura_buff = Aura(reason=ActionReason.CLOAK_OF_THE_ASSASSIN, source=self, health=stats, attack=stats)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
