from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.message),
    path('health/', views.message)
]