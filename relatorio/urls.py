from django.urls import path

from . import views

urlpatterns = [
    path('dia/', views.vendas_dia, name='vendas_dia'),
]