from django import forms

from .models import Pedid, ItemPedido, PedidoPagamento, AcrescimoDesconto

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedid
        fields = '__all__'
        exclude = ('total', 'status')


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = '__all__'
        exclude = ('pedido', 'total')


class PedidoPagamentoForm(forms.ModelForm):
    class Meta:
        model = PedidoPagamento
        fields = '__all__'
        exclude = ('pedido', 'troco', 'resto')
                    
        
class AcrescimoDescontoForm(forms.ModelForm):
    class Meta:
        model = AcrescimoDesconto
        fields = '__all__'
        exclude = ('pedido',)
