from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from datetime import datetime, timedelta

from .models import Pedid, ItemPedido, PedidoPagamento
from .forms import PedidoForm, ItemPedidoForm, PedidoPagamentoForm, AcrescimoDescontoForm

# lembrar pôr essas var em outro lugar
hoje = datetime.now().date()
amanha = hoje + timedelta(days=1)

# Create your views here.
def lista_pedidos(request):
    pedidos_ativo = Pedid.objects.filter(status='ativo').order_by('-abertura')
    pedidos_final = Pedid.objects.filter(status='finalizado').order_by('-abertura')
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm()

    context = {'pedidos_ativos': pedidos_ativo, 'pedidos_final': pedidos_final, 'form': form}
    return render(request, 'pedidos.html', context)


def editar_pedido(request, pedido_id):
    pedido = Pedid.objects.get(id=pedido_id)
    pagamentos = PedidoPagamento.objects.filter(pedido_id=pedido_id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            form.save()
        return redirect('editar_pedido', pedido_id=pedido_id)
    else:
        form = ItemPedidoForm()
    itens = ItemPedido.objects.filter(pedido=pedido)
    context = {'pedido': pedido, 'itens': itens, 'form': form, 'pagamentos': pagamentos}
    return render(request, 'ver_pedido.html', context)    


def deletar_item(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    pedido_id = item.pedido.id
    item.delete()
    return redirect('editar_pedido', pedido_id= pedido_id)


def pagamento(request, pedido_id):
    pedido = Pedid.objects.get(id=pedido_id)
    pagamentos = PedidoPagamento.objects.filter(pedido_id=pedido_id)

    pag_total = pagamentos.aggregate(Sum('valor'))['valor__sum'] or 0
    resto = float(pedido.total) - float(pag_total)

    # Instancia os formulários no início
    form_pagamento = PedidoPagamentoForm()
    form_ajuste = AcrescimoDescontoForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'pagamento':
            form_pagamento = PedidoPagamentoForm(request.POST)
            if form_pagamento.is_valid():
                pag = form_pagamento.save(commit=False)
                pag.pedido = pedido
                pag.save()
                return redirect('pagamento', pedido_id=pedido_id)
            else:
                print(form_pagamento.errors)

        elif form_type == 'ajuste':
            form_ajuste = AcrescimoDescontoForm(request.POST)
            if form_ajuste.is_valid():
                pag = form_ajuste.save(commit=False)
                pag.pedido = pedido
                pag.save()
                return redirect('pagamento', pedido_id=pedido_id)
            else:
                print(form_ajuste.errors)

    # Atualiza status do pedido se pago
    if resto <= 0 and pedido.status != 'finalizado' and resto <= pedido.total:
        pedido.status = 'finalizado'
        pedido.save()

    context = {
        'pedido': pedido,
        'form_ajuste': form_ajuste,
        'form_pagamento': form_pagamento,
        'resto': resto,
        'pagamentos': pagamentos
    }

    return render(request, 'pagamento.html', context)