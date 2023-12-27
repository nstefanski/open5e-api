from django.contrib import admin

from api_v2.models import *


# Register your models here.

class FromDocumentModelAdmin(admin.ModelAdmin):
    list_display = ['key', '__str__']


class ItemModelAdmin(admin.ModelAdmin):
    list_display = ['key', 'name']


class TraitInline(admin.TabularInline):
    model = Trait


class RaceAdmin(admin.ModelAdmin):
    inlines = [
        TraitInline,
    ]


class CapabilityInline(admin.TabularInline):
    model = Capability
    exclude = ('name',)


class FeatAdmin(admin.ModelAdmin):
    inlines = [
        CapabilityInline,
    ]
    list_display = ['key', 'name']


class TraitInline(admin.TabularInline):
    model = Trait


class RaceAdmin(admin.ModelAdmin):
    inlines = [
        TraitInline,
    ]


class BenefitInline(admin.TabularInline):
    model = Benefit


class BackgroundAdmin(admin.ModelAdmin):
    model = Background
    inlines = [
        BenefitInline
    ]

class DamageTypeAdmin(admin.ModelAdmin):
    model = DamageType


class LanguageAdmin(admin.ModelAdmin):
    model = Language


admin.site.register(Weapon, admin_class=FromDocumentModelAdmin)
admin.site.register(Armor, admin_class=FromDocumentModelAdmin)

admin.site.register(ItemCategory)
admin.site.register(Item, admin_class=ItemModelAdmin)
admin.site.register(ItemSet, admin_class=FromDocumentModelAdmin)

admin.site.register(Race, admin_class=RaceAdmin)

admin.site.register(Feat, admin_class=FeatAdmin)

admin.site.register(Creature)
admin.site.register(CreatureType)
admin.site.register(CreatureSet)

admin.site.register(Background, admin_class=BackgroundAdmin)

admin.site.register(Document)
admin.site.register(License)
admin.site.register(Publisher)
admin.site.register(Ruleset)

admin.site.register(DamageType)

admin.site.register(Language)

admin.site.register(Alignment)

admin.site.register(Condition)