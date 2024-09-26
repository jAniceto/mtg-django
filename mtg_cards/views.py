from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from mtg_decks.models import Card


def cards_home(request):
    """Home page"""

    # Handle card search
    query = request.GET.get('q')
    if query:
        try:
            card = Card.objects.all().get(name__iexact=query)
            return redirect('card_detail', pk=card.pk)
        except ObjectDoesNotExist:
            messages.error(request, 'Card not found. Try again.')

    return render(request, 'mtg_cards/home.html')


def card_detail(request, pk):
    """Card detail page"""
    card = get_object_or_404(
        Card.objects.prefetch_related('cardmainboard_set__mainboard', 'cardsideboard_set__sideboard'), 
        pk=pk
    )

    # price_data = {'labels': [], 'data': [], 'edition': []}
    # for price in card.prices.all():
    #     price_data['labels'].append(price.date.strftime("%d/%m/%Y"))
    #     price_data['data'].append(price.tix)
    #     price_data['edition'].append(price.edition)

    context = {
        'card': card,
    }
    return render(request, 'mtg_cards/card_detail.html', context)
