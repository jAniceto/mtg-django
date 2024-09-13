from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from mtg_decks.models import Deck


def index(request):
    """Homepage. List decks."""
    decks = Deck.objects.all()

    context = {
        'decklist_view': 'by_type',  # Options: '' or 'by_type'
        'decks': decks,
    }
    return render(request, 'mtg_decks/index.html', context)


def download_deck_txt(request, deck_pk):
    """Download a decklist in .txt."""
    deck = get_object_or_404(Deck, pk=deck_pk)
    
    filename = deck.name.replace(' ', '-')
    text_decklist = deck.to_string()

    response = HttpResponse(text_decklist, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
    return response


def copy_decklist(request, deck_pk):
    """Download a decklist in .txt."""
    deck = get_object_or_404(Deck, pk=deck_pk)
    text_decklist = deck.to_string()
    return HttpResponse(text_decklist)
