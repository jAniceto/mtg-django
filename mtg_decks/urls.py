from django.urls import path
from mtg_decks import views


urlpatterns = [
    path('', views.index, name='index'),
    # HTMX views
    path('download-deck-txt/<int:deck_pk>/', views.download_deck_txt, name='download_deck_txt'),
]
