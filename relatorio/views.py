from django.shortcuts import render
from django.utils import timezone

from vendas.models import Pedid

# Create your views here.
def vendas_dia(request):
    hoje = timezone.now().date()
    pedidos = Pedid.objects.filter(abertura__gte=hoje)
    total = 0
    for pedido in pedidos:
        total = pedido.total

    context = {'pedidos': pedidos, 'total': total}
    return render(request, 'relatorio.html', context)
