from django.core.management.base import BaseCommand
from mtg_decks.models import Deck


class Command(BaseCommand):
    help = 'Add or update the Deck art_url field for every Deck in the DB.'

    def handle(self, *args, **options):
        decks = Deck.objects.all()
        for deck in decks:
            deck.art_url = deck.get_deck_art()
            if deck.art_url is None:
                self.stdout.write(f'Failed for {deck.name}')
            deck.save()

        # Summarize
        self.stdout.write('Updating deck art...')
        self.stdout.write('Done.')
