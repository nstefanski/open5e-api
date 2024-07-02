"""Serializers and helper methods for the Creature model."""

from math import floor

from rest_framework import serializers

from api_v2 import models

from .abstracts import GameContentSerializer
from .size import SizeSerializer



def calc_damage_amount(die_count, die_type, bonus):
    die_values = {
        'D4': 2.5,
        'D6': 3.5,
        'D8': 4.5,
        'D10': 5.5,
        'D12': 6.5,
        'D20': 10.5,
    }
    return floor(die_count * die_values[die_type] + bonus)

def make_damage_obj(die_count, die_type, bonus, damage_type):
    if die_count:
        return {
            'amount': calc_damage_amount(
                die_count,
                die_type,
                bonus
            ),
            'die_count': die_count,
            'die_type': die_type,
            'bonus': bonus,
            'type': damage_type,
        }
    return {
        'amount': 1,
        'type': damage_type,
    }

def make_attack_obj(attack):

    obj = {
        'name': attack.name,
        'attack_type': attack.attack_type,
        'to_hit_mod': attack.to_hit_mod,
    }

    if attack.reach_ft:
        obj['reach_ft'] = attack.reach_ft
    if attack.range_ft:
        obj['range_ft'] = attack.range_ft
    if attack.long_range_ft:
        obj['long_range_ft'] = attack.long_range_ft

    obj['target_creature_only'] = attack.target_creature_only

    if attack.damage_type:
        obj['damage'] = make_damage_obj(
            attack.damage_die_count,
            attack.damage_die_type,
            attack.damage_bonus,
            attack.damage_type.key
        )

    if attack.extra_damage_type:
        obj['extra_damage'] = make_damage_obj(
            attack.extra_damage_die_count,
            attack.extra_damage_die_type,
            attack.extra_damage_bonus,
            attack.extra_damage_type.key
        )

    return obj

def make_action_obj(action):

    obj = { 'name': action.name, 'desc': action.desc }

    match action.uses_type:
        case 'PER_DAY':
            obj['uses_per_day'] = action.uses_param
        case 'RECHARGE_ON_ROLL':
            obj['recharge_on_roll'] = action.uses_param
        case 'RECHARGE_AFTER_REST':
            obj['recharge_after_rest'] = True

    attacks = action.creatureactionattack_set.all()

    if len(attacks) > 0:
        obj['attacks'] = [make_attack_obj(attack) for attack in attacks]

    return obj


class CreatureSerializer(GameContentSerializer):
    '''The serializer for the Creature object.'''

    key = serializers.ReadOnlyField()
    ability_scores = serializers.SerializerMethodField()
    modifiers = serializers.SerializerMethodField()
    saving_throws = serializers.SerializerMethodField()
    all_saving_throws = serializers.SerializerMethodField()
    skill_bonuses = serializers.SerializerMethodField()
    all_skill_bonuses = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()
    size = SizeSerializer(read_only=True, context={'request': {}})
    speed = serializers.SerializerMethodField()
    all_speed = serializers.SerializerMethodField()

    class Meta:
        model = models.Creature
        fields = [
            'url',
            'document',
            'key',
            'name',
            'size',
            'speed',
            'all_speed',
            'category',
            'type',
            'alignment',
            'weight',
            'armor_class',
            'hit_points',
            'ability_scores',
            'modifiers',
            'saving_throws',
            'all_saving_throws',
            'skill_bonuses',
            'all_skill_bonuses',
            'passive_perception',
            'actions',
            'creaturesets'
        ]

    def get_ability_scores(self, creature):
        return creature.get_ability_scores()

    def get_modifiers(self, creature):
        return creature.get_modifiers()

    def get_saving_throws(self, creature):
        entries = creature.get_saving_throws().items()
        return { key: value for key, value in entries if value is not None }

    def get_all_saving_throws(self, creature):
        defaults = creature.get_modifiers()
        entries = creature.get_saving_throws().items()
        return { key: (defaults[key] if value is None else value) for key, value in entries }

    def get_skill_bonuses(self, creature):
        entries = creature.get_skill_bonuses().items()
        return { key: value for key, value in entries if value is not None }

    def get_all_skill_bonuses(self, creature):
        defaults = {
            'acrobatics': creature.modifier_dexterity,
            'animal_handling': creature.modifier_wisdom,
            'arcana': creature.modifier_intelligence,
            'athletics': creature.modifier_strength,
            'deception': creature.modifier_charisma,
            'history': creature.modifier_intelligence,
            'insight': creature.modifier_wisdom,
            'intimidation': creature.modifier_charisma,
            'investigation': creature.modifier_intelligence,
            'medicine': creature.modifier_wisdom,
            'nature': creature.modifier_intelligence,
            'perception': creature.modifier_wisdom,
            'performance': creature.modifier_charisma,
            'persuasion': creature.modifier_charisma,
            'religion': creature.modifier_intelligence,
            'sleight_of_hand': creature.modifier_dexterity,
            'stealth': creature.modifier_dexterity,
            'survival': creature.modifier_wisdom,
        }
        entries = creature.get_skill_bonuses().items()
        return { key: (defaults[key] if value is None else value) for key, value in entries }

    def get_speed(self, creature):
        entries = creature.get_speed().items()
        return { key: value for key, value in entries if value is not None }


    def get_all_speed(self, creature):
        return creature.get_all_speed()

    def get_actions(self, creature):
        result = []
        for action in creature.creatureaction_set.all():
            action_obj = make_action_obj(action)
            result.append(action_obj)
        return result


class CreatureTypeSerializer(GameContentSerializer):
    '''Serializer for the Creature Type object'''
    key = serializers.ReadOnlyField()

    class Meta:
        model = models.CreatureType
        fields = '__all__'


class CreatureSetSerializer(GameContentSerializer):
    '''Serializer for the Creature Set object'''
    key = serializers.ReadOnlyField()
    creatures = CreatureSerializer(many=True, read_only=True, context={'request':{}})

    class Meta:
        model = models.CreatureSet
        fields = '__all__'
