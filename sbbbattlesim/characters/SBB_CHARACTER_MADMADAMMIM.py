from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Mad Mim'
    support = True

    def buff(self, target_character):
        target_character.change_stats(attack=6 if self.golden else 3, temp=True, reason=f'{self} support buff')
