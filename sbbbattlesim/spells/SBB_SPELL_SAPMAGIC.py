from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = 'Flourish'
    _level = 3

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=7, temp=False, reason=StatChangeCause.STONE_SKIN, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.TREANT in char.tribes