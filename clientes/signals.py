from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Cliente


@receiver(pre_save, sender=Cliente)
def cliente_pre_save(sender, instance, **kwargs):
    print(f'{instance.nome} adicionado com sucesso')