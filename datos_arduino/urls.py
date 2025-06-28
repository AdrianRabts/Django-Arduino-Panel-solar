from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_datos, name='lista_datos'),
]
