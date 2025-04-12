from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cadastro.views.cliente_view import ClienteViewSet
from cadastro.views.distribuidor_view import DistribuidorViewSet
from cadastro.views.fornecedor_view import FornecedorViewSet
from cadastro.views.pedido_view import PedidoViewSet
from cadastro.views.produto_view import ProdutoViewSet
from cadastro.views.vendedor_view import VendedorViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'distribuidores', DistribuidorViewSet, basename='distribuidores')
router.register(r'fornecedores', FornecedorViewSet, basename='fornecedores')
router.register(r'pedidos', PedidoViewSet, basename='pedidos')
router.register(r'produtos', ProdutoViewSet, basename='produtos')
router.register(r'vendedores', VendedorViewSet, basename='vendedores')

urlpatterns = [
    path('', include(router.urls)),
]
