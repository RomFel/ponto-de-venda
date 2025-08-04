from django.urls import path

from .views import lista_pedidos, editar_pedido, deletar_item, pagamento

urlpatterns = [
    path('pedidos/', view=lista_pedidos, name='lista_pedidos'),
    path('pedido/<int:pedido_id>/', view=editar_pedido, name='editar_pedido'),
    path('deletar/<int:item_id>', view=deletar_item, name='deletar_item'),
    path('pagamento/<int:pedido_id>', view=pagamento, name='pagamento')
]