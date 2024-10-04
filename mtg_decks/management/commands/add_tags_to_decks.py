from django.core.management.base import BaseCommand
from mtg_decks.models import Deck, Tag


class Command(BaseCommand):
    help = 'A series of rules to automatically add tags to existing decks.'

    def handle(self, *args, **options):
        # Check if there are tags and decks in the database
        decks = Deck.objects.all()
        if not decks:
            self.stdout.write('There are no Deck objects in the database. Exiting...')
            return

        tags = Tag.objects.all()
        if not tags:
            self.stdout.write('There are no Tag objects in the database. Exiting...')
            return
        
        # Add tags based on deck names
        self.stdout.write('Adding tags based on deck names...')
        for deck in decks:
            for tag in tags:
                if tag.name in deck.name.lower():
                    deck.tags.add(tag)
                    self.stdout.write(f'Added <{tag.name}> to <{deck.name}>.')

        # Add tags based on deck family
        self.stdout.write('Adding tags based on deck family...')
        for deck in decks:
            if deck.family:
                if deck.family.lower() in ['red', 'white', 'blue', 'black', 'green']:
                    tag = Tag.objects.get(name='monocolor')
                    deck.tags.add(tag)
                
                elif deck.family.lower() in ['selesnya', 'orzhov', 'boros', 'azorius', 'dimir', 'rakdos', 'golgari', 'izzet', 'simic', 'gruul']:
                    tag = Tag.objects.get(name='2-color')
                    deck.tags.add(tag)

                elif deck.family.lower() in ['naya', 'esper', 'grixis', 'jund', 'bant', 'abzan', 'temur', 'jeskai', 'mardu', 'sultai']:
                    tag = Tag.objects.get(name='3-color')
                    deck.tags.add(tag)
                
                elif deck.family.lower() in ['glint', 'dune', 'ink', 'whitch', 'yore']:
                    tag = Tag.objects.get(name='4-color')
                    deck.tags.add(tag)

                elif deck.family.lower() == 'domain':
                    tag = Tag.objects.get(name='5-color')
                    deck.tags.add(tag)

                elif deck.family.lower() == 'colorless':
                    tag = Tag.objects.get(name='colorless')
                    deck.tags.add(tag)

                else:
                    continue
                self.stdout.write(f'Added <{tag.name}> to <{deck.name}>.')
        
        # Rules base on cards
        self.stdout.write('Adding tags based on card...')
        card_rules = {
            "Tortured Existence": ['graveyard',],
            "Satyr Wayfinder": ['graveyard',],
            "Urza's Power Plant": ['tron', 'ramp',],
            "Moment's Peace": ['fog', 'control',],
            "Tangle": ['fog', 'control',],
            "Jace's Erasure": ['mill',],
            "Axebane Guardian": ['defender', 'ramp',],
            "Freed from the Real": ['combo',],
            "Ephemerate": ['blink',],
            "Myr Enforcer": ['artifacts', 'affinity',],
            "Carrion Feeder": ['sacrifice',],
            "Raven's Crime": ['discard', 'control',],
            "Basilisk Gate": ['gates', 'midrange',],
            "Ninja of the Deep Hours": ['ninjutsu', 'value',],
            "Impact Tremors": ['ping', 'creatures',],
            "Rally the Peasants": ['wide', 'creatures', 'aggro',],
            "Guardians' Pledge": ['wide', 'creatures', 'aggro',],
            "Stinkweed Imp": ['dredge', 'graveyard',],
        }
        for card_name, tag_names in card_rules.items():
            decks = Deck.objects.filter(mainboard__name=card_name)
            for deck in decks:
                for tag_name in tag_names:
                    tag = Tag.objects.get(name=tag_name)
                    deck.tags.add(tag)
                    self.stdout.write(f'Added <{tag.name}> to <{deck.name}>.')
