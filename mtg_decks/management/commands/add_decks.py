from django.core.management.base import BaseCommand

import json

from mtg_decks.models import Deck, update_or_create_deck


EXAMPLE_DECKS = [
    {
        'mainboard': [
            [4, 'All That Glitters'],
            [3, 'Ancient Den'],
            [3, 'Blood Fountain'],
            [4, 'Myr Enforcer'],
            [4, 'Deadly Dispute'],
            [4, 'Frogmite'],
            [1, 'Goldmire Bridge'],
            [4, 'Ichor Wellspring'],
            [2, 'Metallic Rebuke'],
            [4, 'Mistvault Bridge'],
            [4, 'Chromatic Star'],
            [4, 'Razortide Bridge'],
            [2, "Reckoner's Bargain"],
            [3, 'Saiba Cryptomancer'],
            [4, 'Seat of the Synod'],
            [4, 'Thoughtcast'],
            [4, 'Vault of Whispers'],
            [2, 'Wedding Invitation'],
        ],
        'sideboard': [
            [3, "Chainer's Edict"],
            [2, 'Drown in Sorrow'],
            [3, 'Dust to Dust'],
            [1, 'Essence Harvest'],
            [3, 'Blue Elemental Blast'],
            [2, 'Nihil Spellbomb'],
            [1, 'Metallic Rebuke'],
        ],
        'name': 'Affinity Glitter Esper',
        'color': 'esper',
        'tags': None,
        'author': None,
        'source': None,
        'created_at': '2024/04/26',
    },
    {
        'mainboard': [
            [2, 'Archaeomancer'],
            [3, 'Snap'],
            [4, 'Azorius Chancery'],
            [4, 'Plains'],
            [6, 'Island'],
            [2, 'Evolving Wilds'],
            [2, 'Ephemerate'],
            [3, 'Deep Analysis'],
            [1, 'Ghostly Flicker'],
            [4, 'Halimar Excavator'],
            [2, 'Irregular Cohort'],
            [1, 'Counterspell'],
            [1, 'Mortuary Mire'],
            [3, 'Mulldrifter'],
            [2, 'Ondu Cleric'],
            [4, 'Brainstorm'],
            [2, 'Preordain'],
            [2, 'Prohibit'],
            [3, 'Sea Gate Oracle'],
            [4, 'Ash Barrens'],
            [3, 'Sunscape Familiar'],
            [2, 'The Modern Age'],
        ],
        'sideboard': [
            [2, 'Revoke Existence'],
            [2, 'Dispel'],
            [3, 'Dust to Dust'],
            [2, 'Prismatic Strands'],
            [1, 'Negate'],
            [1, 'Ondu Cleric'],
            [1, 'Echoing Truth'],
            [2, 'Blue Elemental Blast'],
            [1, 'Stonehorn Dignitary'],
        ],
        'name': 'Ally Mill Azorius',
        'color': 'azorius',
        'tags': None,
        'author': None,
        'source': None,
        'created_at': '2024/04/26',
    },
]


class Command(BaseCommand):
    help = 'Adds decks to the Database.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filepath', type=str, help='Path to decks JSON file.')
        parser.add_argument('-m', '--max', type=int, help='Maximum number of decks to load.')
        parser.add_argument('--del', action='store_true', help='Delete all decks not in the in the input data.')

    def handle(self, *args, **options):
        json_file = options['filepath']
        max_decks = options['max']
        delete_other_decks = options['del']

        # 1) Choose source of data (JSON file or dict)
        self.stdout.write('Loading data...')
        if json_file:
            # Load decks file
            with open(json_file, 'r') as f:
                decks = json.load(f)

            if max_decks:
                decks = decks[:max_decks]

        else:
            decks = EXAMPLE_DECKS

        # 2) If --del was passed, delete all decks that are not in the provided data
        if delete_other_decks:
            self.stdout.write('Searching decks for deletion...')
            
            deck_names_in_data = [d['name'] for d in decks]  # list of deck names in the data
            deck_objs = Deck.objects.all()
            
            for deck_obj in deck_objs:
                if deck_obj.name not in deck_names_in_data:
                    self.stdout.write(f'Deleted {deck_obj.name} deck.')
                    deck_obj.delete()

        # 3) Add decks in the provided data to DB
        self.stdout.write('Adding or updating decks...')
        for deck_dict in decks:
            # Add or update deck
            deck, created, errors = update_or_create_deck(deck_dict)

            # Print result
            if created:
                self.stdout.write(f'Created {deck.name}.')
            else:
                self.stdout.write(f'Updated {deck.name}.')
            
            # Print errors
            for card_name in errors:
                self.stdout.write(f' - Error adding {card_name} to {deck.name}.')
