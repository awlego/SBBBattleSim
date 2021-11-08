from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill


class CharacterType(Character):
    display_name = 'Polywoggle'
    slay = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.PolywoggleSlay)

    class PolywoggleSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            pass  #TODO implement random spawn on survive
