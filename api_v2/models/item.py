"""The model for an item."""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from api.models import GameContent
from .weapon import Weapon
from .armor import Armor
from .abstracts import Object, HasName, HasDescription
from .document import FromDocument

class ItemCategory(HasName, FromDocument):
    """A class describing categories of items."""
    pass

class Item(Object, HasDescription, FromDocument):
    """
    This is the model for an Item, which is an object that can be used.

    This extends the object model, but adds cost, and is_magical.
    """

    cost = models.DecimalField(
        null=True,  # Allow an unspecified cost.
        default=None,
        max_digits=10,
        decimal_places=2,  # Only track down to 2 decimal places.
        validators=[MinValueValidator(0)],
        help_text='Number representing the cost of the object.')

    weapon = models.ForeignKey(
        Weapon,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True)

    armor = models.ForeignKey(
        Armor,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True)

    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        null=False
    )

    requires_attunement = models.BooleanField(
        null=False,
        default=False,  # An item is not magical unless specified.
        help_text='If the item requires attunement.')


    RARITY_CHOICES = [
        (1, 'common'),
        (2, 'uncommon'),
        (3, 'rare'),
        (4, 'very rare'),
        (5, 'legendary'),
        (6, 'artifact')
    ]

    rarity = models.IntegerField(
        null=True,  # Allow an unspecified size.
        blank=True,
        choices=RARITY_CHOICES,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)],
        help_text='Integer representing the rarity of the object.')

    @property 
    def is_magic_item(self):
        return self.rarity is not None


class ItemSet(HasName, HasDescription, FromDocument):
    """A set of items to be referenced."""

    items = models.ManyToManyField(Item, related_name="itemsets",help_text="The set of items.")
