# Generated by Django 5.1.1 on 2024-10-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtg_decks', '0004_remove_tag_decks_deck_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='art_url',
            field=models.URLField(blank=True),
        ),
    ]
