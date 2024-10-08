from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.management import call_command
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from mtg_decks.models import Deck, update_or_create_deck
from mtg_decks.forms import DeckFilterForm, DecksJSONUploadForm, CreateTagForm, DeckTagsForm
import json


def index(request):
    """Homepage. List all decks using infinite scroll with HTMX."""
    # Base queryset (all decks)
    decks = Deck.objects.prefetch_related('cardmainboard_set__card__best_price', 'cardsideboard_set__card__best_price').all()

    # Get form data
    form = DeckFilterForm(request.GET)
    if form.is_valid():
        deck_name = form.cleaned_data['name']
        deck_family = form.cleaned_data['family']
        card_name = form.cleaned_data['card']
        card_name_sb = form.cleaned_data['card_sb']
        deck_tag = form.cleaned_data['tag']
        sort_attribute = form.cleaned_data['sort_attribute']
        sort_direction = form.cleaned_data['sort_direction']

        # Filter base queryset
        if deck_name:
            decks = decks.filter(name__icontains=deck_name)
        if deck_family:
            decks = decks.filter(family__iexact=deck_family)
        if card_name:
            decks = decks.filter(mainboard__name__icontains=card_name)
        if card_name_sb:
            decks = decks.filter(sideboard__name__icontains=card_name_sb)
        if deck_tag:
            decks = decks.filter(tags=deck_tag)

        # Sort
        if sort_attribute == 'price':
            if sort_direction == 'Asc':
                decks = sorted(decks, key=lambda t: t.get_price()['total'])
            else:
                decks = sorted(decks, key=lambda t: t.get_price()['total'], reverse=True)
            
        else:
            order_str = ''
            if sort_direction == 'Desc':
                order_str += '-'
            order_str += sort_attribute
            decks = decks.order_by(order_str)

    # Pagination
    page_number = request.GET.get('page', 1)  # defaults to 1 on first load
    paginator = Paginator(decks, settings.DECKS_PER_PAGE)
    decks_page = paginator.get_page(page_number)

    context = {
        'new_badge_limit_days': settings.NEW_BADGE_LIMIT_DAYS,
        'decks': decks_page,
        'form': DeckFilterForm(),
    }
    if request.htmx:
        # Render partial (new page of decks)
        return render(request, 'mtg_decks/partials/decks.html', context)
    # Otherwise, render the full page on the first load
    return render(request, 'mtg_decks/index.html', context)


def deck_index(request):
    """Table containing all decks."""
    decks = Deck.objects.all()
    context = {
        'decks': decks,
    }
    return render(request, 'mtg_decks/deck-index.html', context)


def deck(request, pk, slug):
    """Deck detail page."""
    # Check if deck exists, otherwise return 404 error
    deck = get_object_or_404(Deck, pk=pk)
    context = {
        'new_badge_limit_days': settings.NEW_BADGE_LIMIT_DAYS,
        'deck': deck,
    }
    return render(request, 'mtg_decks/deck-detail.html', context)


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


#######################################################################
# Views for logged in users only (to edit info)
#######################################################################

def create_tag(request, deck_pk):
    """HTMX view. Adds a create tag form and handles tag creation."""
    deck = get_object_or_404(Deck, pk=deck_pk)

    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            deck.tags.add(tag)
            context = {
                'deck': deck,
            }
            return render(request, 'mtg_decks/partials/deck_tags.html', context)

    context = {
        'deck': deck,
        'create_tag_form': CreateTagForm()
    }
    return render(request, 'mtg_decks/partials/create_tag_form.html', context)


def edit_deck_tags(request, deck_pk):
    """HTMX view. Adds a edit tags form and handles tags update."""
    deck = get_object_or_404(Deck, pk=deck_pk)

    if request.method == 'POST':
        form = DeckTagsForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            context = {
                'deck': deck,
            }
            return render(request, 'mtg_decks/partials/deck_tags.html', context)

    context = {
        'deck': deck,
        'deck_tags_form': DeckTagsForm(instance=deck)
    }
    return render(request, 'mtg_decks/partials/edit_tags_form.html', context)


#######################################################################
# Management views
#######################################################################

@login_required
def management(request):
    """Several tools to update the site."""

    deck_json_upload_form = DecksJSONUploadForm()
    
    context = {'deck_json_upload_form': deck_json_upload_form}
    return render(request, 'mtg_decks/management.html', context)


def process_deck_json(request):
    form = DecksJSONUploadForm(request.POST, request.FILES)

    if form.is_valid() and request.htmx:
        file = request.FILES['file']
        try:
            # Parse the JSON file
            decks_data = json.load(file)

            created_decks = []
            updated_decks = []
            err_decks = []
            for deck_dict in decks_data:
                # Add or update deck
                deck, created, errors = update_or_create_deck(deck_dict)
                
                if created:
                    created_decks.append(deck.name)
                elif errors:
                    err_decks.append(deck.name)
                else:
                    updated_decks.append(deck.name)

            context = {
                'created_decks': created_decks,
                'updated_decks': updated_decks,
                'err_decks': err_decks,
            }
            # return HttpResponse('Decks update compleated!')
            return render(request, 'mtg_decks/partials/log_updated_decks.html', context)

        except:
            return HttpResponse('Failed')


def update_card_prices(request):
    call_command('add_prices')
    return HttpResponse('Done!')
