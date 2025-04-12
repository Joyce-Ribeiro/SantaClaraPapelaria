from django.db import models
from cadastro.models.pedido import Pedido

class Pagamento(models.Model):
    FORMAS_PAGAMENTO = [
        ('cartao', 'Cartão'),
        ('boleto', 'Boleto'),
        ('pix', 'Pix'),
        ('berries', 'Berries'),
    ]

    STATUS_PAGAMENTO = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('recusado', 'Recusado'),
    ]

    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pagamento')  # Um pagamento por pedido
    forma_pagamento = models.CharField(max_length=20, choices=FORMAS_PAGAMENTO)
    status_pagamento = models.CharField(max_length=20, choices=STATUS_PAGAMENTO)

    class Meta:
        db_table = '"comercial"."pagamento"'  # Nome da tabela no banco

    def __str__(self):
        return f"Pagamento {self.id_pagamento} - {self.forma_pagamento} - {self.status_pagamento}"
