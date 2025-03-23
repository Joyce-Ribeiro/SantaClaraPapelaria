from django.db import models

class Vendedor(models.Model):
    matricula = models.CharField(max_length=8, primary_key=True)  # Matrícula como chave primária
    nome = models.CharField(max_length=300)  # Nome do vendedor
    comissao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Comissão
    senha = models.CharField(max_length=100)  # Senha

    class Meta:
        db_table = '"cadastro"."vendedor"'  # Especificando que a tabela ficará no esquema 'cadastro'

    def __str__(self):
        return self.nome
