from django.db import models

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    data_pedido = models.DateTimeField()

    class Meta:
        db_table = '"cadastro"."pedido"'  # nome da tabela no banco de dados

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.data_pedido}"
