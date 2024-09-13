from django.shortcuts import render
from mtg_decks.models import Deck


def index(request):
    """Homepage. List decks."""
    decks = Deck.objects.all()

    context = {
        'decklist_view': 'by_type',  # Options: '' or 'by_type'
        'decks': decks,
    }
    return render(request, 'mtg_decks/index.html', context)
