from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models.vendedor import Vendedor

admin.site.register(Vendedor)
