from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.heros import Hero


class SadDraculaOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
       Buff(reason=ActionReason.SAD_DRACULA_SLAY, source=self.sad_dracula, targets=[self.manager],
            attack=3, stack=stack).resolve()


class HeroType(Hero):
    display_name = 'Sad Dracula'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(event=SadDraculaOnAttackAndKill, sad_dracula=self, _lambda=lambda char: char.position == 1)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
