# Generated by Django 5.1.1 on 2024-09-27 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mtg_decks', '0002_bestprice_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deck',
            options={'ordering': ['-updated_at', 'name']},
        ),
    ]
