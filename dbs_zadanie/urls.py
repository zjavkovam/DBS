"""dbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('v1/', include('app.urls')),
    path('v2/', include('app.urls')),
    path('v3/', include('app.urls')),
    path('v4/players/<url_id>/game_exp/', views.z6_2),
    path('v4/players/<url_id>/game_objectives/', views.z6_3),
    path('v4/players/<url_id>/abilities/', views.z6_4),
    path('v4/patches/', views.z6_1),
    path('v4/matches/<url_id>/top_purchases/', views.z6_5),
    path('v4/abilities/<url_id>/usage/',views.z6_6),
]
