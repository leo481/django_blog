from django.urls import path
from . import views

urlpatterns = [
    path('likes_change', views.likes_change, name='likes_change'),
]
