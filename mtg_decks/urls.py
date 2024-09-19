from django.urls import path
from mtg_decks import views


urlpatterns = [
    path('', views.index, name='index'),
    path('deck-index', views.deck_index, name='deck_index'),
    path('download-deck-txt/<int:deck_pk>/', views.download_deck_txt, name='download_deck_txt'),
    # HTMX views
    path('filtered-decks/', views.deck_list_filtering, name='deck_list_filtering'),
    path('copy-decklist/<int:deck_pk>/', views.copy_decklist, name='copy_decklist'),
]
