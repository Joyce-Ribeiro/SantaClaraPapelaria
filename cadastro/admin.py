from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models.vendedor import Vendedor
from .models.fornecedor import Fornecedor

admin.site.register(Vendedor)
admin.site.register(Fornecedor)
