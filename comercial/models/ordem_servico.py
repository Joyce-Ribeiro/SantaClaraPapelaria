from django.db import models
from cadastro.models.cliente import Cliente
from cadastro.models.pedido import Pedido

class OrdemServico(models.Model):
    id_ordem = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ordens_servico")
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="ordens_servico")
    matricula_vendedor = models.CharField(max_length=30)

    class Meta:
        db_table = '"comercial"."ordem_servico"'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"Ordem {self.id_ordem} - Cliente {self.cliente.nome} - Pedido {self.pedido.id_pedido}"