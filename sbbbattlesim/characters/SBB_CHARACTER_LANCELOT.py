from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class LancelotSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        modifier = 4 if self.manager.golden else 2
        Buff(reason=ActionReason.SLAY, source=self.manager, targets=[self.manager],
             attack=modifier, health=modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Lancelot'
    quest = True

    _attack = 7
    _health = 7
    _level = 5
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(LancelotSlay)
