from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Fanny'
    support = True

    def buff(self, target_character):
        if 'dwarf' in target_character.tribes:
            stat_change = 4 if self.golden else 2
            target_character.change_stats(attack=stat_change, health=stat_change, temp=True, reason=f'{self} buff')
