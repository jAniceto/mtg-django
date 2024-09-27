from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count
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


    # Top cards
    cards_by_price = Card.objects.order_by('-best_price__tix')[:20]
    cards_mb_totals = Card.objects.annotate(mainboard_uses_total=Sum('cardmainboard__quantity')).order_by('-mainboard_uses_total')[:10]
    cards_mbs = Card.objects.annotate(mainboard_uses=Count('cardmainboard')).order_by('-mainboard_uses')[:10]
    cards_sb_totals = Card.objects.annotate(sideboard_uses_total=Sum('cardsideboard__quantity')).order_by('-sideboard_uses_total')[:10]
    cards_sbs = Card.objects.annotate(sideboard_uses=Count('cardsideboard')).order_by('-sideboard_uses')[:10]

    context = {
        'cards_by_price': cards_by_price,
        'cards_mb_totals': cards_mb_totals,
        'cards_mbs': cards_mbs,
        'cards_sb_totals': cards_sb_totals,
        'cards_sbs': cards_sbs,
    }
    return render(request, 'mtg_cards/cards_home.html', context)


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
