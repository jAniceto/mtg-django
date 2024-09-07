from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import json

from mtg_decks.models import Card


class Command(BaseCommand):
    help = "Adds cards to the Database."

    def handle(self, *args, **options):
        cards = [
            'Ancient Den',
            'Rancor',
            'Forest',
            'Preordain',
            'Ponder',
            'Brainstorm',
        ]
        
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
                card.add_info(scryfall_card)

            else:
                action_str = 'EXISTED'
            
            self.stdout.write(f"{action_str} -- {card.name}")
        
        self.stdout.write(f"Created {n_created} out of {len(cards)} cards.")
