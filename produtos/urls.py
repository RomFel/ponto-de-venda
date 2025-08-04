from django.urls import path

from . import views

urlpatterns = [
    path('lista/', views.lista_produtos, name='lista_produtos'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('deletar/<int:produto_id>/', views.deletar_produto, name='deletar_produto'),
]