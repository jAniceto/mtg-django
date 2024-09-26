from django.shortcuts import render, get_object_or_404
from mtg_decks.models import Card


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
