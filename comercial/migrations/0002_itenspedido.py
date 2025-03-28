# Generated by Django 5.1.7 on 2025-03-24 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0008_cliente'),
        ('comercial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItensPedido',
            fields=[
                ('id_itensPedido', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido', to='cadastro.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido', to='cadastro.produto')),
            ],
            options={
                'db_table': '"comercial"."itens_pedido"',
            },
        ),
    ]
