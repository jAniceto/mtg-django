from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

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
