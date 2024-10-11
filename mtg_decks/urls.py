from django.urls import path
from mtg_decks import views


urlpatterns = [
    path('', views.index, name='index'),
    path('deck-index/', views.deck_index, name='deck_index'),
    path('deck/<int:pk>-<str:slug>/', views.deck, name='deck'),
    path('stats/', views.stats, name='stats'),
    path('download-deck-txt/<int:deck_pk>/', views.download_deck_txt, name='download_deck_txt'),
    path('management/', views.management, name='management'),
    # HTMX views
    path('create-tag/<int:deck_pk>/', views.create_tag, name='create_tag'),
    path('edit-deck-tags/<int:deck_pk>/', views.edit_deck_tags, name='edit_deck_tags'),
    path('copy-decklist/<int:deck_pk>/', views.copy_decklist, name='copy_decklist'),
    path('process-deck-json/', views.process_deck_json, name='process_deck_json'),
    path('update-card-prices/', views.update_card_prices, name='update_card_prices'),
]
