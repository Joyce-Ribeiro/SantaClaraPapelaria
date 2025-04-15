from django.db import models

class Produto(models.Model):
    cod_produto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)
    valor_produto = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    desc_produto = models.TextField(blank=True, null=True)

    class Meta:
        db_table = '"cadastro"."produto"'  # nome da tabela no banco de dados

    def __str__(self):
        return self.nome
