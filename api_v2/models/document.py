from django.db import models
from django.urls import reverse
from django.apps import apps


from .abstracts import HasName, HasDescription

from api_v2 import models as v2_models

class Document(HasName, HasDescription):

    key = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="Unique key for the Document."
    )

    licenses = models.ManyToManyField(
        "License",
        help_text="Licenses that the content has been released under.")

    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.CASCADE,
        help_text="Publisher which has written the game content document.")

    ruleset = models.ForeignKey(
        "Ruleset",
        on_delete=models.CASCADE,
        help_text="The document's game system that it was published for."
    )

    author = models.TextField(
        help_text='Author or authors.')

    published_at = models.DateTimeField(
        help_text="Date of publication, or null if unknown."
    )

    permalink = models.URLField(
        help_text="Link to the document."
    )

    @property
    def stats(self):
        stats = {}
        for model in apps.get_models():
            # Filter out api_v1.
            if model._meta.app_label != 'api_v2': continue

            SKIPPED_MODEL_NAMES = [
                'Document',
                'Ruleset',
                'License',
                'Publisher']
            if model.__name__ in SKIPPED_MODEL_NAMES: continue

            CHILD_MODEL_NAMES = [
                'Trait',
                'Capability', 
                'Benefit',
                'CreatureAction',
                'CreatureAttack']
            if model.__name__ in CHILD_MODEL_NAMES: continue


            object_count = model.objects.filter(document=self.key).count()
            stats[model.__name__.lower()]=object_count
        return stats


class License(HasName, HasDescription):
    key = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="Unique key for the License."
    )


class Publisher(HasName):
    key = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="Unique key for the publishing organization."
    )


class Ruleset(HasName, HasDescription):
    key = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="Unique key for the ruleset the document was published for."
    )

    content_prefix = models.CharField(
        max_length=10,
        blank=True,
        help_text="Short code prepended to content keys."
    )


class FromDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    key = models.CharField(
        primary_key=True,
        max_length=100,
        help_text="Unique key for the Item.")

    def get_absolute_url(self):
        return reverse(self.__name__, kwargs={"pk": self.pk})

    class Meta:
        abstract = True