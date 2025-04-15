from django.db import models
from cadastro.models.cliente import Cliente
from cadastro.models.pedido import Pedido
from cadastro.models.vendedor import Vendedor  # Supondo que há um modelo Vendedor

class OrdemServico(models.Model):
    id_ordem = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ordens_servico", null=True, blank=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="ordens_servico", null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="ordens_servico")
    
    class Meta:
        db_table = '"comercial"."ordem_servico"'
        constraints = [
            models.UniqueConstraint(fields=['pedido'], name='unique_pedido_ordem_servico')  # Adiciona a restrição de unicidade
        ]

    def __str__(self):
        return f"Ordem {self.id_ordem} - {self.cliente or self.vendedor} - Pedido {self.pedido.id_pedido}"
