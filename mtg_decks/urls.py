from django.urls import path
from mtg_decks import views


urlpatterns = [
    path('', views.index, name='index'),
]
