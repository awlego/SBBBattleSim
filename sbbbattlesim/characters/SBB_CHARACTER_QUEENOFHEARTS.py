from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class EvilQueenOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.evil_queen.golden else 2
        Buff(source=self.evil_queen, reason=ActionReason.EVILQUEEN_BUFF, targets=[self.evil_queen],
             attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Evil Queen'
    aura = True

    _attack = 1
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.QUEEN}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, oni_king=self, event=EvilQueenOnDeath, evil_queen=self,
                                   _lambda=lambda char: Tribe.EVIL in char.tribes)

    
