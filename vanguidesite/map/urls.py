from django.urls import path
from map import views

urlpatterns = [
    path("map/", views.map, name='map'),
]