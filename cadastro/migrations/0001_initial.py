# Generated by Django 5.1.7 on 2025-03-23 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('matricula', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=300)),
                ('comissao', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('senha', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'cadastro.vendedor',
            },
        ),
    ]
