from django.db import models

class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    cnpj = models.CharField(max_length=18, unique=True, null=False)
    nome = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = '"cadastro"."fornecedor"'
         
    def __str__(self):
        return self.nome