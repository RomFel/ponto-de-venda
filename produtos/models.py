from django.db import models

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    # categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    # estoque = models.IntegerField()
    # preco_custo = models.DecimalField(max_digits=6, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome
    
