from django.db import models

class Distribuidor(models.Model):
    id_distribuidor = models.AutoField(primary_key=True)
    cnpj = models.CharField(max_length=18, unique=True)
    nome = models.CharField(max_length=255)

    class Meta:
        db_table = '"cadastro"."distribuidor"'  # nome da tabela no banco de dados

    def __str__(self):
        return self.nome
