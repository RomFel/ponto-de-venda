from django.urls import path

from . import views

urlpatterns = [
    path('lista', views.lista_clientes, name='lista_clientes'),
]