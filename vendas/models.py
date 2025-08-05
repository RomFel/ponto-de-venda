from django.db import models

from clientes.models import Cliente
from produtos.models import Produto

# Create your models here.
class Pedid(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    abertura = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(default='ativo')

    def __str__(self):
        return f'{self.id:0>5}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedid, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    acrescimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.produto and self.quantidade:
            self.total = (self.produto.preco_venda * self.quantidade) + self.acrescimo - self.desconto
        super().save(*args, **kwargs)

        pedido = self.pedido
        itens = ItemPedido.objects.filter(pedido=pedido)
        pedido.total = sum(item.total for item in itens if item.total)
        pedido.save()

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)
        itens = ItemPedido.objects.filter(pedido=pedido)
        pedido.total = sum(item.total for item in itens if item.total)
        pedido.save()


class FormaPagmento(models.Model):
    forma = models.CharField(max_length=10)

    def __str__(self):
        return self.forma


class PedidoPagamento(models.Model):
    pedido = models.ForeignKey(Pedid, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(FormaPagmento, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    recebido = models.DecimalField(max_digits=10, decimal_places=2, default=0)##se a pessoa disser que vai pagar 10 de um total de 20, mas paga com 50
    resto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    troco = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        pagamentos_anteriores = PedidoPagamento.objects.filter(pedido=self.pedido).exclude(pk=self.pk)
        total_pago = sum(pag.valor for pag in pagamentos_anteriores)

        restante = max(self.pedido.total - total_pago, 0)
        valor_informado = self.valor
        self.valor = min(valor_informado, restante)

        if self.recebido == 0:
            self.troco = max(valor_informado - self.valor, 0)
        else:
            self.troco = max(self.recebido - self.valor, 0)

        self.resto = max(self.pedido.total - (total_pago + self.valor), 0)

        super().save(*args, **kwargs)


class AcrescimoDesconto(models.Model):
    pedido = models.ForeignKey(Pedid, on_delete=models.CASCADE)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    acrescimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pedido.total is None:
            self.pedido.total = 0
        self.pedido.total += self.acrescimo - self.desconto
        self.pedido.save()  ##salva o pedido com o novo total
        super().save(*args, **kwargs)
