from django.shortcuts import render, get_object_or_404
from mtg_decks.models import Card


def card_detail(request, pk):
    """Card detail page"""
    card = get_object_or_404(Card, pk=pk)

    # price_data = {'labels': [], 'data': [], 'edition': []}
    # for price in card.prices.all():
    #     price_data['labels'].append(price.date.strftime("%d/%m/%Y"))
    #     price_data['data'].append(price.tix)
    #     price_data['edition'].append(price.edition)

    # # Get user collections containing this card
    # if request.user.is_authenticated:
    #     user_collections_with_card = Collection.objects.all().filter(user=request.user, cards__name=card.name)
    #     user_card_mainboard_associations = CardDeckMainboardAssociation.objects.all().filter(deck__user=request.user, card=card)
    #     user_card_sideboard_associations = CardDeckSideboardAssociation.objects.all().filter(deck__user=request.user, card=card)
    #     collections = Collection.objects.all().filter(user=request.user)
    # else:
    #     user_collections_with_card = None
    #     user_card_mainboard_associations = None
    #     user_card_sideboard_associations = None
    #     collections = None

    context = {
        'card': card,
        # 'price_data': json.dumps(price_data),
        # 'user_collections_with_card': user_collections_with_card,
        # 'user_card_mainboard_associations': user_card_mainboard_associations,
        # 'user_card_sideboard_associations': user_card_sideboard_associations,
        # 'collections': collections,
    }
    return render(request, 'mtg_cards/card_detail.html', context)
