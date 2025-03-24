from django.db import models
from cadastro.models.pedido import Pedido
from cadastro.models.produto import Produto

class ItensPedido(models.Model):
    id_itensPedido = models.AutoField(primary_key=True)
    quantidade = models.IntegerField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens_pedido')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='itens_pedido')

    class Meta:
        db_table = '"comercial"."itens_pedido"'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"Item {self.id_itensPedido} - Pedido {self.pedido.id_pedido} - Produto {self.produto.nome}"
