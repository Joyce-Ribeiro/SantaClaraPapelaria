from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cadastro.views.vendedor_view import VendedorViewSet  # Importando o ViewSet de Vendedor

# Criando o roteador e registrando as views
router = DefaultRouter()
router.register(r'vendedores', VendedorViewSet)  # Registrando a rota de vendedores

# Incluindo as rotas
urlpatterns = [
    path('api/', include(router.urls)),  # Incluindo as rotas do ViewSet
]
