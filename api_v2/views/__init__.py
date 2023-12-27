"""The initialization for views for open5e's api v2."""

from .background import BackgroundFilterSet, BackgroundViewSet

from .creature import CreatureFilterSet, CreatureViewSet
from .creature import CreatureTypeViewSet

from .document import DocumentViewSet
from .document import RulesetViewSet
from .document import PublisherViewSet
from .document import LicenseViewSet

from .feat import FeatFilterSet, FeatViewSet

from .race import RaceFilterSet, RaceViewSet

from .item import ItemFilterSet, ItemViewSet
from .item import ItemSetFilterSet, ItemSetViewSet
from .item import ItemCategoryViewSet
from .item import ArmorFilterSet, ArmorViewSet
from .item import WeaponFilterSet, WeaponViewSet

from .damagetype import DamageTypeViewSet

from .language import LanguageFilterSet, LanguageViewSet

from .alignment import AlignmentFilterSet, AlignmentViewSet

from .condition import ConditionViewSet