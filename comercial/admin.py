from django.contrib import admin

# Register your models here.
from .models.ordem_servico import OrdemServico
from .models.itens_pedido import ItensPedido
from .models.fornecimento import Fornecimento

admin.site.register(OrdemServico)
admin.site.register(ItensPedido)
admin.site.register(Fornecimento)