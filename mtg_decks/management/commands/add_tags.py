from django.core.management.base import BaseCommand
from mtg_decks.models import Tag


# Deck tags
TAGS = [
    '2-color', '3-color', '4-color', '5-color', 'affinity', 'aggro', 'ally', 'arcane', 
    'artifacts', 'blink', 'cascade', 'changeling', 'cipher', 'colorless', 'combo', 
    'competitive', 'control', 'convoke', 'counters', 'creatureless', 'creatures', 'crew', 
    'cycling', 'deathtouch', 'defender', 'delve', 'discard', 'dredge', 'emerge', 'enchantments', 
    'equipments', 'ETB', 'evolve', 'exalted', 'exert', 'extort', 'fog', 'gates', 'graveyard', 
    'heroic', 'hexproof', 'infect', 'infinite', 'land destruction', 'landfall', 'lands', 
    'lifegain', 'lock', 'madness', 'metalcraft', 'midrange', 'mill', 'mimic', 'monocolor', 
    'morph', 'ninjutsu', 'persist', 'ping', 'prowess', 'ramp', 'reanimator', 'sacrifice', 
    'soulshift', 'spells', 'synergy', 'voltron', 'tempo', 'threshold', 'tokens', 
    'transformational', 'tribal', 'tron', 'undying', 'value', 'vehicles', 'wall', 
    'white', 'wide',
]


class Command(BaseCommand):
    help = 'Adds deck Tags to the database.'

    def handle(self, *args, **options):
        # Add tags
        n_created = 0
        for tag_name in TAGS:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                n_created += 1

        # Summarize
        self.stdout.write('Adding tags...')
        self.stdout.write(f'Added {n_created} tags out of {len(TAGS)} provided.')
