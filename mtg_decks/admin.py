from django.contrib import admin
from mtg_decks.models import Card, Deck, CardMainboard, CardSideboard


admin.site.register(Card)
admin.site.register(Deck)
admin.site.register(CardMainboard)
admin.site.register(CardSideboard)
