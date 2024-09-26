from django.urls import path
from mtg_cards import views


urlpatterns = [
    path('', views.cards_home, name='cards_home'),
    path('detail/<int:pk>/', views.card_detail, name='card_detail'),
]
