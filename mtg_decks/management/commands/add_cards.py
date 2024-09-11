from django.core.management.base import BaseCommand

import json

from mtg_decks.models import Card


# Example cards
EXAMPLE_CARDS = [
    'Ancient Den',
    'Rancor',
    'Forest',
    'Preordain',
    'Ponder',
    'Brainstorm',
]


class Command(BaseCommand):
    help = "Adds cards to the Database."

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filepath', type=str, help='Path to cards JSON file.')

    def handle(self, *args, **options):
        json_file = options['filepath']
        
        if json_file:
            # Load decks file
            with open(json_file, 'r') as f:
                cards = json.load(f)
        else:
            cards = EXAMPLE_CARDS
        
        # Add cards
        n_created = 0
        for card_name in cards:
            # Get or create Card
            card, created = Card.objects.get_or_create(name=card_name)

            if created:
                action_str = 'CREATED'
                n_created += 1

                # Get card info from Scryfall
                scryfall_card = card.get_scryfall()

                # Add card info to DB
                if scryfall_card:
                    card.add_info(scryfall_card)

            else:
                action_str = 'EXISTED'
            
            self.stdout.write(f"{action_str} -- {card.name}")
        
        self.stdout.write(f"Created {n_created} out of {len(cards)} cards.")
