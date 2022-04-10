from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Free Roll'''
    _level = 2
    cost = 0

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
