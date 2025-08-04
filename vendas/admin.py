from django.contrib import admin

from .models import Pedid, FormaPagmento, PedidoPagamento


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'total')


# Register your models here.
admin.site.register(Pedid, PedidoAdmin)
admin.site.register(FormaPagmento)
admin.site.register(PedidoPagamento)
