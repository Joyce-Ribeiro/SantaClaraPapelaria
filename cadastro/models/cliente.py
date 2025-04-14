from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, unique=True)
    senha = models.CharField(max_length=255)
    email = models.CharField(max_length=30, null=True, blank=True)
    cidade = models.CharField(max_length=30, null=True, blank=True)
    
    class Meta:
        db_table = '"cadastro"."cliente"'  

    def __str__(self):
        return self.nome
