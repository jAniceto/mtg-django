from collections import OrderedDict
import math

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone

import requests
import json

from mtg_utils.mtg import color_families, mana_cost_html
from mtg_decks.charts import plot_deck_cmc_curve


class User(AbstractUser):
    """User model."""

    pass


class Card(models.Model):
    """Card model. Containing card information."""

    # Card identification
    name = models.CharField(max_length=150)
    oracle_id = models.CharField(max_length=250, blank=True, null=True)
    layout = models.CharField(max_length=100)

    # Print fields
    set_abbreviation = models.CharField(max_length=10, blank=True, null=True)
    set_name = models.CharField(max_length=100, blank=True, null=True)
    rarity = models.CharField(max_length=10, blank=True, null=True)
    flavor_text = models.TextField(blank=True, null=True)
    img_url = models.URLField(blank=True)
    art_url = models.URLField(blank=True)

    # Links
    scryfall_url = models.URLField(blank=True)
    rulings_url = models.URLField(blank=True)
    prints_search_uri = models.URLField(blank=True)

    # Legalities
    standard_legal = models.BooleanField(default=False)
    historic_legal = models.BooleanField(default=False)
    pioneer_legal = models.BooleanField(default=False)
    modern_legal = models.BooleanField(default=False)
    pauper_legal = models.BooleanField(default=False)
    penny_legal = models.BooleanField(default=False)
    legacy_legal = models.BooleanField(default=False)
    vintage_legal = models.BooleanField(default=False)
    brawl_legal = models.BooleanField(default=False)
    commander_legal = models.BooleanField(default=False)

    # Gameplay fields (main card face)
    cmc = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    type_line = models.CharField(max_length=100, blank=True, null=True)
    color_identity = models.TextField(
        blank=True, null=True
    )  # JSON-serialized (text) version of list
    keywords = models.TextField(blank=True, null=True)  # JSON-serialized (text) version of list
    mana_cost = models.CharField(max_length=50, blank=True, null=True)
    oracle_text = models.TextField(blank=True)
    colors = models.TextField(blank=True, null=True)  # JSON-serialized (text) version of list
    power = models.CharField(max_length=50, blank=True, null=True)
    toughness = models.CharField(max_length=50, blank=True, null=True)

    # Other faces
    faces = models.BooleanField(default=False)
    card_faces = models.TextField(blank=True, null=True)  # JSON-serialized (text) version of list
    # Face 1
    face1_name = models.CharField(max_length=100, blank=True, null=True)
    face1_colors = models.CharField(
        max_length=100, blank=True, null=True
    )  # JSON-serialized (text) version of list
    face1_cmc = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    face1_mana_cost = models.CharField(max_length=50, blank=True, null=True)
    face1_type_line = models.CharField(max_length=100, blank=True, null=True)
    face1_oracle_text = models.TextField(blank=True, null=True)
    face1_power = models.CharField(max_length=50, blank=True, null=True)
    face1_toughness = models.CharField(max_length=50, blank=True, null=True)
    face1_img_url = models.URLField(blank=True, null=True)
    # Face 2
    face2_name = models.CharField(max_length=100, blank=True, null=True)
    face2_colors = models.CharField(max_length=100, blank=True, null=True)
    face2_cmc = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    face2_mana_cost = models.CharField(max_length=50, blank=True, null=True)
    face2_type_line = models.CharField(max_length=100, blank=True, null=True)
    face2_oracle_text = models.TextField(blank=True, null=True)
    face2_power = models.CharField(max_length=50, blank=True, null=True)
    face2_toughness = models.CharField(max_length=50, blank=True, null=True)
    face2_img_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['mana_cost']

    def __str__(self):
        return self.name

    def get_scryfall(self):
        """
        Searches a card by name on the Scryfall API. This function queries the Scryfall 'cards/named' API endpoint with an exact match search for the provided card name.
        Returns a Scryfall card object if a card is found, otherwise returns None

        Raises:
            requests.RequestException: An error from the `requests` library indicating a problem with the network or the
            fetch operation.
        """
        url = 'https://api.scryfall.com/cards/named'
        params = {'exact': self.name}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # The card exists, return card object
                return response.json()
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
        return None

    def add_info(self, scryfall_card_obj):
        """Add info to a the card model. Info as a Scryfall card object."""
        if 'oracle_id' in scryfall_card_obj:
            self.oracle_id = scryfall_card_obj['oracle_id']

        if 'layout' in scryfall_card_obj:
            self.layout = scryfall_card_obj['layout']

        if 'set' in scryfall_card_obj:
            self.set_abbreviation = scryfall_card_obj['set']

        if 'set_name' in scryfall_card_obj:
            self.set_name = scryfall_card_obj['set_name']

        if 'rarity' in scryfall_card_obj:
            self.rarity = scryfall_card_obj['rarity']

        if 'scryfall_uri' in scryfall_card_obj:
            self.scryfall_url = scryfall_card_obj['scryfall_uri']

        if 'rulings_url' in scryfall_card_obj:
            self.rulings_url = scryfall_card_obj['rulings_url']

        if 'prints_search_uri' in scryfall_card_obj:
            self.prints_search_uri = scryfall_card_obj['prints_search_uri']

        if 'legalities' in scryfall_card_obj:
            FORMATS = [
                'pauper',
                'standard',
                'pioneer',
                'modern',
                'legacy',
                'vintage',
                'commander',
                'penny',
                'historic',
                'brawl',
            ]
            legalities = {}
            for fo in FORMATS:
                if scryfall_card_obj['legalities'][fo] == 'legal':
                    legalities[fo] = True
                else:
                    legalities[fo] = False
            self.standard_legal = legalities['standard']
            self.historic_legal = legalities['historic']
            self.pioneer_legal = legalities['pioneer']
            self.modern_legal = legalities['modern']
            self.pauper_legal = legalities['pauper']
            self.penny_legal = legalities['penny']
            self.legacy_legal = legalities['legacy']
            self.vintage_legal = legalities['vintage']
            self.brawl_legal = legalities['brawl']
            self.commander_legal = legalities['commander']

        if 'cmc' in scryfall_card_obj:
            self.cmc = scryfall_card_obj['cmc']

        if 'type_line' in scryfall_card_obj:
            self.type_line = scryfall_card_obj['type_line']

        if 'color_identity' in scryfall_card_obj:
            self.color_identity = json.dumps(scryfall_card_obj['color_identity'])

        if 'keywords' in scryfall_card_obj:
            self.keywords = json.dumps(scryfall_card_obj['keywords'])

        if 'mana_cost' in scryfall_card_obj:
            self.mana_cost = scryfall_card_obj['mana_cost']

        if 'oracle_text' in scryfall_card_obj:
            self.oracle_text = scryfall_card_obj['oracle_text']

        if 'colors' in scryfall_card_obj:
            self.colors = json.dumps(scryfall_card_obj['colors'])

        if 'power' in scryfall_card_obj:
            self.power = scryfall_card_obj['power']

        if 'toughness' in scryfall_card_obj:
            self.toughness = scryfall_card_obj['toughness']

        if 'flavor_text' in scryfall_card_obj:
            self.flavor_text = scryfall_card_obj['flavor_text']

        if 'image_uris' in scryfall_card_obj:
            self.img_url = scryfall_card_obj['image_uris']['normal']
            self.art_url = scryfall_card_obj['image_uris']['art_crop']

        # If the card has multiple faces
        if 'card_faces' in scryfall_card_obj:
            self.faces = True
            self.card_faces = json.dumps(scryfall_card_obj['card_faces'])

            try:
                self.face1_name = scryfall_card_obj['card_faces'][0]['name']
                self.face2_name = scryfall_card_obj['card_faces'][1]['name']
            except Exception:
                pass

            try:
                self.face1_colors = json.dumps(scryfall_card_obj['card_faces'][0]['colors'])
                self.face2_colors = json.dumps(scryfall_card_obj['card_faces'][1]['colors'])
            except Exception:
                pass

            try:
                self.face1_cmc = scryfall_card_obj['card_faces'][0]['cmc']
                self.face2_cmc = scryfall_card_obj['card_faces'][1]['cmc']
            except Exception:
                pass

            try:
                self.face1_mana_cost = scryfall_card_obj['card_faces'][0]['mana_cost']
                self.face2_mana_cost = scryfall_card_obj['card_faces'][1]['mana_cost']
            except Exception:
                pass

            try:
                self.face1_type_line = scryfall_card_obj['card_faces'][0]['type_line']
                self.face2_type_line = scryfall_card_obj['card_faces'][1]['type_line']
            except Exception:
                pass

            try:
                self.face1_oracle_text = scryfall_card_obj['card_faces'][0]['oracle_text']
                self.face2_oracle_text = scryfall_card_obj['card_faces'][1]['oracle_text']
            except Exception:
                pass

            try:
                self.face1_power = scryfall_card_obj['card_faces'][0]['power']
                self.face2_power = scryfall_card_obj['card_faces'][1]['power']
            except Exception:
                pass

            try:
                self.face1_toughness = scryfall_card_obj['card_faces'][0]['toughness']
                self.face2_toughness = scryfall_card_obj['card_faces'][1]['toughness']
            except Exception:
                pass

            try:
                self.face1_img_url = scryfall_card_obj['card_faces'][0]['image_uris']['normal']
                self.face2_img_url = scryfall_card_obj['card_faces'][1]['image_uris']['normal']
            except Exception:
                pass

        # Save card instance
        self.save()

    def get_mana_cost_html(self):
        """Method to return mana cost as HTML symbols"""
        return mana_cost_html(self.mana_cost)

    def is_land(self):
        """Returns True if Card is a Land, otherwise returns False."""
        if 'Land' in self.type_line:
            return True
        return False


class Deck(models.Model):
    """Deck model. Containing deck information."""

    name = models.CharField(max_length=50)
    slug = models.SlugField()
    FORMAT_CHOICES = (
        ('Standard', 'Standard'),
        ('Historic', 'Historic'),
        ('Pioneer', 'Pioneer'),
        ('Modern', 'Modern'),
        ('Pauper', 'Pauper'),
        ('Penny', 'Penny'),
        ('Legacy', 'Legacy'),
        ('Vintage', 'Vintage'),
        ('Brawl', 'Brawl'),
        ('Commander', 'Commander'),
    )
    format_name = models.CharField(max_length=50, choices=FORMAT_CHOICES, default='Pauper')
    FAMILY_CHOICES = (
        (k.capitalize(), k.capitalize())
        for k, v in color_families().items()  # e.g., ('Boros', 'Boros'),
    )
    family = models.CharField(max_length=50, choices=FAMILY_CHOICES, blank=True, null=True)
    mainboard = models.ManyToManyField(
        Card, through='CardMainboard', related_name='mainboards', blank=True
    )
    sideboard = models.ManyToManyField(
        Card, through='CardSideboard', related_name='sideboards', blank=True
    )
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=150, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    # user = models.ForeignKey(User, related_name='decks', on_delete=models.CASCADE, null=True)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'name']

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        """Override save method to automatically create a slug for every new object"""
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Deck, self).save(*args, **kwargs)

    def add_info(self, deck_dict):
        """Add deck info to deck object. Deck info is a dict of the following format:
        deck_dict = {
            "mainboard": [
                [4, "All That Glitters"],
                [4, "Ancient Den"],
                ...
            ],
            "sideboard": [
                [1, "Revoke Existence"],
                [3, "Dust to Dust"],
                ...
            ],
            "name": "Affinity Azorius",
            "color": "azorius",
            "tags": None,
            "author": None,
            "source": None,
            "created_at": "2024/04/26"
        }
        """
        # Add or update info
        # self.format_name = 'Pauper'
        try:
            self.family = deck_dict['color'].capitalize()
        except AttributeError:
            pass
        # self.description = None
        self.source = deck_dict['author']
        self.source_url = deck_dict['source']
        self.save()

        # Clear decklists if needed
        self.mainboard.clear()
        self.sideboard.clear()

        # Add mainboard
        errors = []  # list of card names that caused and error
        for card in deck_dict['mainboard']:
            card_qty = card[0]
            card_name = card[1].strip()

            # Get Card or create a new Card object
            card, created = Card.objects.get_or_create(name=card_name)

            if created:
                # Get card info from Scryfall
                scryfall_card = card.get_scryfall()

                # Add card info to DB
                if scryfall_card:
                    card.add_info(scryfall_card)
                else:
                    errors.append(card_name)
                    print('Error with', card_name)
                    continue

            # Add card object to mainboard
            CardMainboard.objects.create(mainboard=self, card=card, quantity=card_qty)

        # Add sideboard
        for card in deck_dict['sideboard']:
            card_qty = card[0]
            card_name = card[1].strip()

            # Get Card or create a new Card object
            card, created = Card.objects.get_or_create(name=card_name)

            if created:
                # Get card info from Scryfall
                scryfall_card = card.get_scryfall()

                # Add card info to DB
                if scryfall_card:
                    card.add_info(scryfall_card)
                else:
                    errors.append(card_name)
                    print('Error with', card_name)
                    continue

            # Add card object to sideboard
            CardSideboard.objects.create(sideboard=self, card=card, quantity=card_qty)
        return self, errors
    
    def get_categorized_mainboard(self):
        """Returns a dict of the mainboard card categorized by card type (creature, artifact, etc)."""
        mainboard = self.cardmainboard_set.all()
        categorized_mainboard = OrderedDict([
            ('creature', []),
            ('instant', []),
            ('sorcery', []),
            ('artifact', []),
            ('enchantment', []),
            ('land', []),
            ('other', []),
        ])
        for cardmb in mainboard:
            if 'Creature' in cardmb.card.type_line:
                categorized_mainboard['creature'].append(cardmb)
            elif 'Instant' in cardmb.card.type_line:
                categorized_mainboard['instant'].append(cardmb)
            elif 'Sorcery' in cardmb.card.type_line:
                categorized_mainboard['sorcery'].append(cardmb)
            elif 'Artifact' in cardmb.card.type_line:
                categorized_mainboard['artifact'].append(cardmb)
            elif 'Enchantment' in cardmb.card.type_line:
                categorized_mainboard['enchantment'].append(cardmb)
            elif 'Land' in cardmb.card.type_line:
                categorized_mainboard['land'].append(cardmb)
            else:
                categorized_mainboard['other'].append(cardmb)
        return categorized_mainboard
    
    def max_cards_col(self):
        """Estimates how many unique cards should appear in each of the two decklist columns
        so that columns are of similar height. 
        max_cards = floor( [(mainboard cards) + (sideboard cards) + (margin)] / 2 )
        """
        margin = 3  # safety margin to give
        n_cards_main = len(self.cardmainboard_set.all())
        n_cards_side = len(self.cardsideboard_set.all())
        return math.floor( (n_cards_main + n_cards_side + margin) / 2 )

    def get_colors(self):
        """Get a list of color codes for the deck, according to its color family."""
        color_dict = color_families()
        try:
            return color_dict[self.family.lower()]
        except AttributeError:
            return None

    def get_days_since_created(self):
        """Get number of days since the deck was created."""
        time_diff = timezone.now() - self.created_at
        return time_diff.days

    def get_days_since_updated(self):
        """Get number of days since the deck was last updated."""
        time_diff = timezone.now() - self.updated_at
        return time_diff.days

    def cmc_chart(self):
        """Create the CMC bar chart for a deck."""
        fig = plot_deck_cmc_curve(self)
        return fig.to_html(full_html=True, config={'staticPlot': True, 'displayModeBar': False})


class CardMainboard(models.Model):
    """Relationship between Cards and Mainboards. Through models for the ManyToMany Card-DeckMainboard relationship."""

    mainboard = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.mainboard.name} - {self.quantity} {self.card.name}'

    class Meta:
        ordering = ['card__cmc', '-card__mana_cost']


class CardSideboard(models.Model):
    """Relationship between Cards and Sideboards. Through models for the ManyToMany Card-DeckSideboard relationship."""

    sideboard = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sideboard.name} - {self.quantity} {self.card.name}'

    class Meta:
        ordering = ['card__cmc', '-card__mana_cost']
