# Generated by Django 5.1.7 on 2025-03-24 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0010_produto'),
        ('comercial', '0005_fornecimento_itenspedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecimento',
            name='distribuidor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecimentos', to='cadastro.distribuidor'),
        ),
    ]
