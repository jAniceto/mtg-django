from django.core.management.base import BaseCommand

import json

from mtg_decks.models import Card
from mtg_utils import scryfall


# Example cards
EXAMPLE_CARDS = [
    'Ancient Den',
    'Rancor',
    'Oh Crap',
    'Preordein',
    'Ponder',
    'Force of Negation',
]


class Command(BaseCommand):
    help = 'Adds cards to the Database.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filepath', type=str, help='Path to cards JSON file.')

    def handle(self, *args, **options):
        json_file = options['filepath']

        if json_file:
            # Load decks file
            self.stdout.write('Loading JSON file...')
            with open(json_file, 'r') as f:
                cards = json.load(f)
        else:
            cards = EXAMPLE_CARDS

        # Add cards
        self.stdout.write('Processing...')
        n_created = 0 
        n_fails = 0
        for card_name in cards:
            try:
                # Try to find the card on the database
                card = Card.objects.get(name=card_name)
                continue  # if found, skip to next card
            
            except Card.DoesNotExist:
                # Try to find the card on Scryfall
                scryfall_card = scryfall.get_card_by_name(card_name)

                if scryfall_card is None:
                    self.stdout.write(f'{card_name} was not found.')
                    n_fails += 1
                    continue  # skip to next card
                
                # If card was found in Scryfall, add to database
                card = Card(name=card_name)
                card.save()
                n_created += 1
                card.add_info(scryfall_card)

        # Summarize
        self.stdout.write('--------------------')
        self.stdout.write(f'Total cards: {len(cards)}\nExisting: {len(cards) - n_created - n_fails}\nCreated: {n_created}\nFails: {n_fails}')
