from django.contrib import admin
from mtg_decks.models import Card, Deck, CardMainboard, CardSideboard, Tag


admin.site.register(Card)
admin.site.register(Tag)


# Define the Tag inline admin
class TagInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = Tag.decks.through
    extra = 0  # number of extra blank forms to display


# Define the CardMainboard and CardSideboard inline admin
class CardMainboardInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = CardMainboard
    extra = 0  # number of extra blank forms to display


class CardSideboardInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = CardSideboard
    extra = 0  # number of extra blank forms to display


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    inlines = [TagInline, CardMainboardInline, CardSideboardInline]
