from django.core.management.base import BaseCommand

import json

from mtg_decks.models import get_or_create_card


# Example cards
EXAMPLE_CARDS = [
    'Ancient Den',
    'Rancor',
    'Oh Snap',
    'Preordein',
    'Ponder',
    'Solitude',
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
            # Check if card exists, otherwise create a new card object
            _, result = get_or_create_card(card_name)
            
            if result == 'exists':
                pass
            elif result == 'created':
                n_created += 1
            else:
                n_fails += 1

        # Summarize
        self.stdout.write('--------------------')
        self.stdout.write(f'Total cards: {len(cards)}\nExisting: {len(cards) - n_created - n_fails}\nCreated: {n_created}\nFails: {n_fails}')
