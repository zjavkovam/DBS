from django.urls import path
from . import views



urlpatterns = [
    path('hello/', views.message),
    path('health/', views.message),
    path('patches/', views.prvy_endpoint),
    path('players/<id>/game_exp/', views.druhy_endpoint),
    path('players/<id>/game_objectives/', views.treti_endpoint),
    path('players/<id>/abilities/', views.stvrty_endpoint),
    path('matches/<id>/top_purchases/', views.z5_prvy_endpoint)
]