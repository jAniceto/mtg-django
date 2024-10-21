from django.db.models.signals import post_save
from django.dispatch import receiver
from mtg_decks.models import Deck

@receiver(post_save, sender=Deck)
def update_deck_art(sender, instance, created, **kwargs):
    # Choose a deck cover image
    try:
        instance.art_url = instance.get_deck_art()
        instance.save()
    except IndexError as e:
        pass
