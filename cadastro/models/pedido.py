from django.db import models

class Pedido(models.Model):
    CUPOM_CHOICES = [
        ('onepiece', 'One Piece'),
        ('flamengo', 'Flamengo'),
    ]

    id_pedido = models.AutoField(primary_key=True)
    data_pedido = models.DateTimeField()
    cupom = models.CharField(
        max_length=20,
        choices=CUPOM_CHOICES,
        null=True,
        blank=True,
        help_text='Cupom promocional: "onepiece" ou "flamengo"'
    )

    class Meta:
        db_table = '"cadastro"."pedido"'

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.data_pedido}"
