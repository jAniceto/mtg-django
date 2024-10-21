from django.apps import AppConfig


class MtgDecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mtg_decks'

    def ready(self):
        import mtg_decks.signals