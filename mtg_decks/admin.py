from django.contrib import admin
from mtg_decks.models import Card, Deck, CardMainboard, CardSideboard


admin.site.register(Card)


# Define the CardMainboard and CardSideboard inline admin
class CardMainboardInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = CardMainboard
    extra = 0  # number of extra blank forms to display


class CardSideboardInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = CardSideboard
    extra = 0  # number of extra blank forms to display


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    inlines = [CardMainboardInline, CardSideboardInline]
