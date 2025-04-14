# Generated by Django 5.1.7 on 2025-04-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0013_remove_cliente_cliente_especial_cliente_cidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='cupom',
            field=models.CharField(blank=True, choices=[('onepiece', 'One Piece'), ('flamengo', 'Flamengo')], help_text='Cupom promocional: "onepiece" ou "flamengo"', max_length=20, null=True),
        ),
    ]
