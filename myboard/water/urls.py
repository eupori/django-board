from django.urls import path, re_path
from .views import *

app_name = 'water'
urlpatterns = [
    path('', WaterView.as_view(), name='index'),
	path('drink', WaterView.as_view(), name='water_append'),
	path('drink/delete', WaterDeleteView.as_view(), name='water_remove'),
]
