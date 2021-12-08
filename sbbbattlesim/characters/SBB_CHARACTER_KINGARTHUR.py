from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe, StatChangeCause


class PrinceArthurOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.arthur.golden else 2
        royals = self.arthur.owner.valid_characters(
            _lambda=lambda char: char.golden and (Tribe.PRINCE in char.tribes or Tribe.PRINCESS in char.tribes)
        )
        Buff(source=self.arthur, reason=StatChangeCause.PRINCEARTHUR_BUFF, targets=royals,
             attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Prince Arthur'

    _attack = 5
    _health = 5
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner.board.register(PrinceArthurOnStart, priority=80, arthur=self)
