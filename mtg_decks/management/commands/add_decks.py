from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import json

from mtg_decks.models import Deck, CardMainboard, CardSideboard


class Command(BaseCommand):
    help = "Adds decks to the Database."

    # def add_arguments(self, parser):
    #     parser.add_argument('json_file', type=str, help='Path to the json file containing decks.')

    def handle(self, *args, **options):
        # json_file = options['json_file']

        # # Load decks file
        # with open(json_file, 'r') as f:
        #     data = json.load(f)

        data = [
            {
                "mainboard": [
                    [3, "Preordain"],
                    [4, "Ancient Den"],
                ],
                "sideboard": [
                    [1, "Rancor"],
                    [3, "Dust to Dust"],
                ],
                "name": "Test Deck One",
                "color": "azorius",
                "tags": None,
                "author": None,
                "source": None,
                "created_at": "2024/04/26"
            },
            {
                "mainboard": [
                    [4, "Brainstorm"],
                    [2, "Ancient Den"],
                ],
                "sideboard": [
                    [1, "Forest"],
                    [3, "Dust to Dust"],
                ],
                "name": "Test Deck Two",
                "color": "rakdos",
                "tags": None,
                "author": 'Example author',
                "source": 'www.example.com',
                "created_at": "2024/04/26"
            }
        ]
        
        # Add decks
        for deck_dict in data:
            # Get or create Deck
            deck, created = Deck.objects.get_or_create(name=deck_dict['name'])

            # Add or update info
            deck.add_info(deck_dict)
        
            # Print result
            if created:
                action_str = 'CREATED'
            else:
                action_str = 'UPDATED'
            self.stdout.write(f"{action_str} -- {deck.name}")
