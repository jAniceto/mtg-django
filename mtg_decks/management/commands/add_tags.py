from django.core.management.base import BaseCommand
from mtg_decks.models import Tag


# Deck tags
TAGS = [
    'combo',
    'control',
    'aggro',
    'midrange',
    'colorless',
    'monocolor',
    '2-color',
    '3-color',
    '4-color',
    '5-color',
    'graveyard',
    'mill',
    'tribal',
    'blink',
    'sacrifice',
    'reanimator',
    'spells',
    'creatures',
]


class Command(BaseCommand):
    help = 'Adds deck Tags to the database.'

    def handle(self, *args, **options):
        # Add tags
        n_created = 0
        for tag_name in TAGS:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            n_created += 1
        
        # Summarize
        self.stdout.write('Adding tags...')
        self.stdout.write(f'Added {n_created} tags out of {len(TAGS)} provided.')
