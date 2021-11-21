import logging

from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


logger = logging.getLogger(__name__)


class TreasureType(Treasure):
    display_name = 'Cloak of the Assassin'
    aura = True

    def buff(self, target_character):
        logger.debug(f'IS THIS A SLAY??? {target_character}  {target_character.slay}')
        if target_character.slay:
            for _ in range(self.mimic + 1):
                target_character.change_stats(health=3, attack=3, reason=StatChangeCause.CLOAK_OF_THE_ASSASSIN, source=self, temp=True)
