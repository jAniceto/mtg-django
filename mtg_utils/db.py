from mtg_decks.models import Card
from mtg_utils import scryfall


def get_or_create_card(card_name):
    """Get a card object or create a new one by trying to find data in Scryfall."""
    try:
        # Try to find the card on the database
        card = Card.objects.get(name=card_name)
        return card, 'exists'  # if found, skip to next card

    except Card.DoesNotExist:
        # Try to find the card on Scryfall
        scryfall_card = scryfall.get_card_by_name(card_name)

        if scryfall_card is None:
            print(f'{card_name} was not found.')
            return None, None
        
        # If card was found in Scryfall, add to database
        card = Card(name=card_name)
        card.save()
        card.add_info(scryfall_card)
        return card, 'created'
