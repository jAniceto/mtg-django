# MTG Django

A Django server and frontend with several.


## Main tech

- Django 5
- Bootstrap 5
- HTMX


## Set up locally

1. Clone or download repo

2. Create database

```
$ python manage.py makemigrations
$ python manage.py migrate
```

3. Add initial data
```
python manage.py add_cards
python manage.py add_decks
python manage.py add_tags
python manage.py add_prices
```

4. Run 
```
$ python manage.py runserver
```
