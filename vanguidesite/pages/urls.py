from django.urls import path
from pages import views

urlpatterns = [
    path("home/", views.home, name='home'),
]