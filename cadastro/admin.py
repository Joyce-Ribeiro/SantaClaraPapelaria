from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models.vendedor import Vendedor
from .models.fornecedor import Fornecedor
from .models.produto import Produto
from .models.distribuidor import Distribuidor
from .models.pedido import Pedido
from .models.cliente import Cliente

admin.site.register(Vendedor)
admin.site.register(Fornecedor)
admin.site.register(Produto)
admin.site.register(Distribuidor)
admin.site.register(Pedido)
admin.site.register(Cliente)