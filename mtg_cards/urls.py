from django.urls import path
from mtg_cards import views


urlpatterns = [
    # path('', views.home, name='home'),
    path('detail/<int:pk>/', views.card_detail, name='card_detail'),
]
