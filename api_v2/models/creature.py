"""The model for a creature."""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .abilities import Abilities
from .abstracts import HasDescription, HasName
from .abstracts import damage_die_count_field, damage_die_type_field
from .abstracts import damage_bonus_field, key_field
from .object import Object
from .document import FromDocument
from .speed import HasSpeed
from .enums import CREATURE_ATTACK_TYPES, CREATURE_USES_TYPES



class CreatureType(HasName, HasDescription, FromDocument):
    """The Type of creature, such as Aberration."""


class Creature(Object, Abilities, FromDocument, HasSpeed):
    """
    This is the model for a Creature, per the 5e ruleset.

    This extends the object and abilities models.
    """

    type = models.ForeignKey(
        CreatureType,
        on_delete=models.CASCADE,
        help_text="Type of creature, such as Aberration."
    )

    category = models.CharField(
        max_length=100,
        help_text='What category this creature belongs to.'
    )

    alignment = models.CharField(
        max_length=100,
        help_text='The creature\'s allowed alignments.'
    )
    
    def as_text(self):
        text = self.name + '\n'
        
        for action in self.creatureaction_set.all():
            text+='\n' + action.as_text()

        return text
        
    def search_result_extra_fields(self):
        return {
            "armor_class":self.armor_class,
            "hit_points":self.hit_points,
            "ability_scores":self.get_ability_scores(),
              }

    @property
    def creatureset(self):
        return self.creaturesets.all()


class CreatureAction(HasName, HasDescription):
    """Describes an action available to a creature."""
    key = key_field()

    parent = models.ForeignKey(
        Creature,
        on_delete=models.CASCADE,
        help_text='The creature to which this action belongs.'
    )

    uses_type = models.CharField(
        null=True,
        max_length=20,
        choices=CREATURE_USES_TYPES,
        help_text='How use of the action is limited, if at all.'
    )

    uses_param = models.SmallIntegerField(
        null=True,
        help_text='The parameter X for if the action is limited.'
    )

    def as_text(self):
        text = self.name + '\n' + self.desc

        return text


class CreatureActionAttack(HasName):
    """Describes an attack action used by a creature."""
    
    key = key_field()

    parent = models.ForeignKey(
        CreatureAction,
        on_delete=models.CASCADE,
        help_text='The creature action to which this attack belongs.'
    )

    attack_type = models.CharField(
        max_length=20,
        choices=CREATURE_ATTACK_TYPES,
        help_text='Whether this is a Weapon or Spell attack.'
    )

    to_hit_mod = models.SmallIntegerField(
        validators=[MinValueValidator(-5), MaxValueValidator(20)],
        help_text='Attack roll modifier.'
    )

    reach_ft = models.SmallIntegerField(
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Reach for melee attacks, in feet.'
    )

    range_ft = models.SmallIntegerField(
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Normal range for ranged attacks, in feet.'
    )

    long_range_ft = models.SmallIntegerField(
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Long range for ranged attacks, in feet.'
    )

    target_creature_only = models.BooleanField(
        help_text='If an attack can target creatures only and not objects.'
    )

    # Base damage fields
    damage_die_count = damage_die_count_field()
    damage_die_type = damage_die_type_field()
    damage_bonus = damage_bonus_field()

    damage_type = models.ForeignKey(
        "DamageType",
        null=True,
        related_name="+", # No backwards relation.
        on_delete=models.CASCADE,
        help_text='What kind of damage this attack deals')

    # Additional damage fields
    extra_damage_die_count = damage_die_count_field()
    extra_damage_die_type = damage_die_type_field()
    extra_damage_bonus = damage_bonus_field()

    extra_damage_type = models.ForeignKey(
        "DamageType",
        null=True,
        on_delete=models.CASCADE,
        related_name="+", # No backwards relation.
        help_text='What kind of extra damage this attack deals')


class CreatureSet(HasName, FromDocument):
    """Set that the creature belongs to."""

    creatures = models.ManyToManyField(Creature, related_name="creaturesets",
                                       help_text="The set of creatures.")
