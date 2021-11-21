import logging
import random
from collections import OrderedDict

from sbbbattlesim import utils
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.utils import resolve_damage
from sbbbattlesim.events import EventManager, OnStart
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry, NonTargetedSpell, TargetedSpell
from sbbbattlesim.treasures import registry as treasure_registry

logger = logging.getLogger(__name__)


class Player(EventManager):
    def __init__(self, characters, id, board, treasures, hero, hand, spells, level=0, raw=False, *args, **kwargs):
        super().__init__()
        # Board is board
        self.board = board

        self.id = id
        self.opponent = None
        self.level = level
        self._last_attacker = None
        self._attack_chain = 0
        self.characters = OrderedDict({i: None for i in range(1, 8)})

        self.stateful_effects = {}

        for char_data in characters:
            char = character_registry[char_data['id']](owner=self, **char_data)
            logger.debug(f'{self.id} registering character {char}')
            self.characters[char.position] = char

        self._attack_slot = 1
        self.hand = [character_registry[char_data['id']](owner=self, **char_data) for char_data in hand]
        self.graveyard = []

        self.treasures = {}
        mimic = sum(['SBB_TREASURE_TREASURECHEST' in treasures, hero == 'SBB_HERO_THECOLLECTOR'])
        for tres in treasures:
            treasure = treasure_registry[tres]
            logger.debug(f'{self.id} Registering Treasure {tres} {treasure}')
            self.treasures[treasure.id] = treasure(self, mimic)

        self.hero = hero_registry[hero](player=self, *args, **kwargs)
        logger.debug(f'{self.id} registering hero {self.hero}')

        for spl in spells:
            class CastSpellOnStart(OnStart):
                def handle(self, *args, **kwargs):
                    self.manager.cast_spell(spl, on_start=True)

            self.register(CastSpellOnStart)

        # This is designed to remove temp buffs that were passed in
        if raw:
            self.resolve_board()
            for char in self.characters.values():
                if char:
                    char._base_health -= char._temp_health
                    char._base_attack -= char._temp_attack

    def pretty_print(self):
        return f'{self.id} {", ".join([char.pretty_print() if char else "_" for char in self.characters.values()])}'

    #TODO Make a pretty print for player

    @property
    def front(self):
        return dict(list(self.characters.items())[:4])

    @property
    def back(self):
        return dict(list(self.characters.items())[4:])

    @property
    def attack_slot(self):
        # Handle case where tokens are spawning in the same position
        # With the max chain of 5 as implemented to stop trophy hunter + croc + grim soul shenanigans
        if (self.characters.get(self._attack_slot) is self._last_attacker) or (self._attack_chain >= 5) or (self._last_attacker is None):
            # Prevents the same character from attacking repeatedly
            if self._last_attacker is not None:
                self._attack_slot += 1
            self._attack_chain = 0
        else:
            self._attack_chain += 1

        # If we are advancing the attack slot do it here
        found_attacker = False
        for _ in range(8):
            character = self.characters.get(self._attack_slot)
            if character is not None:
                if character.attack > 0:
                    found_attacker = True
                    break
            self._attack_slot += 1

            if self._attack_slot >= 8:
                self._attack_slot = 1

        # If we have not found an attacker just return None
        if found_attacker:
            self._last_attacker = self.characters.get(self._attack_slot)
        else:
            return None

        return self._attack_slot

    def resolve_board(self):

        self.resolve_damage()

        # Remove all bonuses
        # these need to be prior so that there is not
        # wonky ordering issues with clearing buffs
        # and units that give secondary units buffs that buff
        # arbitrary units
        self.clear_temp()

        for pos, char in self.characters.items():
            if char is None:
                continue
            char.clear_temp()

        # CHARACTER BUFFS
        # Iterate over buff targets and auras then apply them to all necessary targets
        # Support & Aura Targeting
        # This does talk about buffs, but it is for buffs that can only be changed by board state
        for char in self.valid_characters():
            if char.support:
                for target_position in utils.get_support_targets(position=char.position, horn='SBB_TREASURE_BANNEROFCOMMAND' in self.treasures):
                    target = self.characters.get(target_position)
                    if target:
                        char.buff(target)
                        char('OnSupport', buffed=target, support=char)

            elif char.aura:
                for target in self.valid_characters():
                    char.buff(target)

        # TREASURE BUFFS
        for treasure in self.treasures.values():
            if treasure.aura:
                for target in self.valid_characters():
                    treasure.buff(target)

        # HERO BUFFS:
        if self.hero.aura:
            for target in self.valid_characters():
                self.hero.buff(target)

        self('OnResolveBoard')


    def resolve_damage(self, *args, **kwargs):
        action_taken = False

        # TODO Remove all characters before death triggers

        # Resolve Character Deaths
        dead_characters = []

        logger.debug(f'RESOLVING DAMAGE FOR {self}')

        for pos, char in self.characters.items():
            if char is None:
                continue

            if char.dead:
                dead_characters.append(char)
                action_taken = True

                self.graveyard.append(char)
                self.characters[pos] = None

                logger.info(f'{char} died')

        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath', *args,  **kwargs)

        return action_taken

    def summon(self, pos, *characters):
        summoned_characters = []
        spawn_order = utils.get_spawn_positions(pos)
        for char in characters:
            # TODO This could be better
            pos = next((pos for pos in spawn_order if self.characters.get(pos) is None), None)
            if pos is None:
                break

            char.position = pos
            self.characters[pos] = char
            summoned_characters.append(self.characters[pos])
            logger.info(f'Spawning {char} in {pos} position')

        # Now that we have summoned units, make sure they have the buffs they should
        self.resolve_board()

        # The player handles on-summon effects
        self('OnSummon', summoned_characters=summoned_characters)

        return summoned_characters

    def valid_characters(self, _lambda=lambda char: True):
        """
        Return a list of valid characters based on an optional lambda that is passed in as an additoinal filter
        onto the base lambda that guarantees that the character exists and is not dead
        """
        # NOTE: this assumes that a dead thing can NEVER be targeted
        base_lambda = lambda char: char is not None and not char.dead

        return [char for char in self.characters.values() if base_lambda(char) and _lambda(char)]

    def cast_spell(self, spell_id, on_start=False):
        spell = spell_registry[spell_id]
        if spell is None:
            return

        logger.debug(f'{self.id} casting {spell}')

        target = None
        if spell.targeted:
            valid_targets = self.valid_characters(_lambda=spell.filter)
            if valid_targets:
                target = random.choice(valid_targets)

        if isinstance(spell, TargetedSpell) and target is None:
            return

        spell.cast(player=self, target=target)

        resolve_damage(attacker=self, defender=self.opponent)
        resolve_damage(attacker=self.opponent, defender=self)

        self('OnSpellCast', caster=self, spell=spell, target=target)
