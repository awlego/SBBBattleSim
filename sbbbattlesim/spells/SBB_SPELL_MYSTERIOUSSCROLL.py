from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Genies\s Wish'
    _level = 2

    def cast(self, target, *args, **kwargs):
        Buff(targets=[target], attack=10, temp=False, reason=StatChangeCause.HUGEIFY, source=self, *args, **kwargs)
