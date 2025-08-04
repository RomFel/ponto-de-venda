from django.db import models

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    data_nasc = models.DateField(verbose_name='Nasc.:')
    endereco = models.CharField(max_length=200, verbose_name='Endereço', null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nome