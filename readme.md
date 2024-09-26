# MTG Django

A Django server and frontend with several.


## Main tech

- Django 5
- Bootstrap 5
- HTMX


## Set up locally

1. Clone or download repo

2. Set up virtual environment

```
$ cd mtg-django
$ python -m venv venv
$ venv/Scripts/activate
(venv) $ pip install -r requirements.txt
```

3. Create database

```
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
(venv) $ python manage.py createsuperuser
```

4. Add initial data

```
(venv) $ python manage.py add_cards
(venv) $ python manage.py add_decks
(venv) $ python manage.py add_tags
(venv) $ python manage.py add_prices
```

More details on the management commands below.

5. Run dev server

```
(venv) $ python manage.py runserver
```

## Management commands

### Adding cards

Add cards from a JSON file containing a list of card names.

```
(venv) $ python manage.py add_cards -f data/cards.json
```


### Adding decks

Add decks from a JSON file containing a list of deck objects. This can be the output of `mtg-kit export`. If any cards in the deck are not in the DB they are added automatically.

```
(venv) $ python manage.py add_decks -f data/decks.json
```

If you want to limit the number of decks added (e.g., only 10 decks) use the `--max 10` option. This will add only the first `10` decks.

```
(venv) $ python manage.py add_decks -f data/decks.json --max 10
```

Pass the `--del` option to delete all decks in the database whose name does not match a deck in the JSON file.

```
(venv) $ python manage.py add_decks -f data/decks.json --del
```

### Updating card prices

Add or update the best card price by running:

```
(venv) $ python manage.py add_prices
```
