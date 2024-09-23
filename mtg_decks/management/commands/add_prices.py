from django.core.management.base import BaseCommand
from django.conf import settings
from mtg_decks.models import Card, BestPrice
from mtg_utils import goatbots


class Command(BaseCommand):
    help = 'Adds BestPrice to all cards in the Database.'

    def handle(self, *args, **options):
        # Get price data from Goatbots
        self.stdout.write('Downloading price data from Goatbots...')
        URL_PRICES = 'https://www.goatbots.com/download/price-history.zip'
        URL_CARD_DEFINITIONS = 'https://www.goatbots.com/download/card-definitions.zip'

        data_dir = settings.BASE_DIR / 'data'
        goatbots.download_data(URL_PRICES, data_dir)
        goatbots.download_data(URL_CARD_DEFINITIONS, data_dir)

        # Update price info
        self.stdout.write('Updating card prices...')
        cards = Card.objects.all()
        n_created, n_updated = (0, 0)
        for card in cards:
            # Get prices for a given card
            prices = goatbots.get_prices(card.name, data_dir)
            best_price = goatbots.get_best_price(prices)

            # Add or update prices
            price, created = BestPrice.objects.update_or_create(
                card=card,
                defaults={'set_abbreviation': best_price['set'], 'tix': best_price['price']},
            )

            if created:
                n_created += 1
            else:
                n_updated += 1

        self.stdout.write('Done.')
        self.stdout.write(f'Created {n_created} prices and updated {n_updated}.')
