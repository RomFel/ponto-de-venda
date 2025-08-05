from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from vendas.models import Pedid, PedidoPagamento

# Create your views here.
def vendas_dia(request):
    hoje = timezone.now().date()
    # pedidos
    pedidos = Pedid.objects.filter(abertura__gte=hoje, status='finalizado')
    # total
    total = dinheiro = pix = debito = credito = 0
    for pedido in pedidos:
        total += pedido.total
        # Separa por dinheiro
        dinheiro += PedidoPagamento.objects.filter(
            pedido=pedido, forma_pagamento=1).aggregate(total=Sum('valor'))['total'] or 0
        # Separa por pix
        pix += PedidoPagamento.objects.filter(
            pedido=pedido, forma_pagamento=2).aggregate(total=Sum('valor'))['total'] or 0
        # Separa por débito
        debito += PedidoPagamento.objects.filter(
            pedido=pedido, forma_pagamento=3).aggregate(total=Sum('valor'))['total'] or 0
        # Separa por crédido
        credito += PedidoPagamento.objects.filter(
            pedido=pedido, forma_pagamento=4).aggregate(total=Sum('valor'))['total'] or 0
        

    # número de pedidos
    len_pedidos = len(pedidos)

    context = {'pedidos': pedidos,
               'total': total,
               'len_pedidos': len_pedidos,
               'dinheiro':dinheiro,
               'pix': pix,
               'debito': debito,
               'credito': credito,
    }
    return render(request, 'relatorio.html', context)
