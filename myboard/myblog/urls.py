from django.urls import path
from myblog.views import views

urlpatterns = [
    path('', views.index, name='index'),
]
