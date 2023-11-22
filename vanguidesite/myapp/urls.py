# myapp/urls.py
from django.urls import path
from .views import process_input#, input_data
from django.shortcuts import render
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-input/', process_input, name='process_input'),
    path('l/<location_data>/', process_input, name='location_data'),
    path('d/<destination_data>/', process_input, name='destination_data'),
    path('<location_data>/<destination_data>/', process_input, name='both_data'),
]