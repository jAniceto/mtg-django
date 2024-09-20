from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Prefetch
from mtg_decks.models import Deck, CardMainboard, CardSideboard
from mtg_decks.forms import DeckFilterForm


def index(request):
    """Homepage. List all decks using infinite scroll with HTMX."""
    # Base queryset (all decks)
    decks = Deck.objects.prefetch_related(
        Prefetch('cardmainboard_set', queryset=CardMainboard.objects.select_related('card')),
        Prefetch('cardsideboard_set', queryset=CardSideboard.objects.select_related('card'))
    ).all()

    # Get form data
    form = DeckFilterForm(request.GET)
    if form.is_valid():
        deck_name = form.cleaned_data['name']
        deck_family = form.cleaned_data['family']
        card_name = form.cleaned_data['card']
        deck_tag = form.cleaned_data['tag']

        # Filter base queryset
        if deck_name:
            decks = decks.filter(name__icontains=deck_name)
        if deck_family:
            decks = decks.filter(family__iexact=deck_family)
        if card_name:
            decks = decks.filter(mainboard__name__icontains=card_name)
        if deck_tag:
            decks = decks.filter(tags=deck_tag)

    # Pagination
    page_number = request.GET.get('page', 1)  # defaults to 1 on first load
    paginator = Paginator(decks, settings.DECKS_PER_PAGE)
    decks_page = paginator.get_page(page_number)

    context = {
        'decklist_view': settings.DECKLIST_DISPLAY,
        'new_badge_limit_days': settings.NEW_BADGE_LIMIT_DAYS,
        'decks': decks_page,
        'form': DeckFilterForm()
    }
    if request.htmx:
        # Render partial (new page of decks)
        return render(request, 'mtg_decks/partials/decks.html', context)
    # Otherwise, render the full page on the first load
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


def deck_index(request):
    """Table containing all decks."""
    decks = Deck.objects.all()
    context = {
        'decks': decks,
    }
    return render(request, 'mtg_decks/deck-index.html', context)
