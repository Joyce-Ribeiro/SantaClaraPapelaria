from django.db import models
from cadastro.models.distribuidor import Distribuidor
from cadastro.models.fornecedor import Fornecedor
from cadastro.models.produto import Produto

class Fornecimento(models.Model):
    id_fornecimento = models.AutoField(primary_key=True)
    data = models.DateTimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE, related_name='fornecimentos', null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='fornecimentos')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name='fornecimentos')

    class Meta:
        db_table = '"comercial"."fornecimento"'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"Fornecimento {self.id_fornecimento} - Produto {self.produto.nome} - Distribuidor {self.distribuidor.nome}"