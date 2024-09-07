from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
import requests
import json
from mtg_utils.mtg import color_families, mana_cost_html


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
    prints_search_uri  = models.URLField(blank=True)

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
    color_identity = models.TextField(blank=True, null=True)  # JSON-serialized (text) version of list
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
    face1_colors = models.CharField(max_length=100, blank=True, null=True)  # JSON-serialized (text) version of list
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
    
    def get_card_scryfall(self):
        """
        Searches a card by name on the Scryfall API. This function queries the Scryfall 'cards/named' API endpoint with an exact match search for the provided card name.
        Returns a Scryfall card object if a card is found, otherwise returns None

        Raises:
            requests.RequestException: An error from the `requests` library indicating a problem with the network or the
            fetch operation.
        """
        url = "https://api.scryfall.com/cards/named"
        params = {'exact': self.name}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # The card exists, return card object
                return response.json()
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
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
            FORMATS = ['pauper', 'standard', 'pioneer', 'modern', 'legacy', 'vintage', 'commander', 'penny', 'historic', 'brawl']
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

    # def mana_symbols(self):
    #     """Method to return mana cost as HTML symbols"""
    #     return mana_cost_html(self.mana_cost)


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
        ('Commander', 'Commander')
    )
    format_name = models.CharField(max_length=50, choices=FORMAT_CHOICES, default='Pauper')
    FAMILY_CHOICES = (
        (k.capitalize(), k.capitalize()) for k, v in color_families().items()  # e.g., ('Boros', 'Boros'),
    )
    family = models.CharField(max_length=50, choices=FAMILY_CHOICES, blank=True, null=True)
    mainboard = models.ManyToManyField(Card, through="CardMainboard", related_name='mainboards', blank=True)
    sideboard = models.ManyToManyField(Card, through="CardSideboard", related_name='sideboards', blank=True)
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=150, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    # user = models.ForeignKey(User, related_name='decks', on_delete=models.CASCADE, null=True)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Override save method to automatically create a slug for every new object"""
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Deck, self).save(*args, **kwargs)


class CardMainboard(models.Model):
    """Relationship between Cards and Mainboards. Through models for the ManyToMany Card-DeckMainboard relationship."""
    mainboard = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CardSideboard(models.Model):
    """Relationship between Cards and Sideboards. Through models for the ManyToMany Card-DeckSideboard relationship."""
    sideboard = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
