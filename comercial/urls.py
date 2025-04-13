from django.urls import path, include
from rest_framework.routers import DefaultRouter
from comercial.views.pagamento_view import PagamentoViewSet
from comercial.views.fornecimento_view import FornecimentoViewSet
from comercial.views.itens_pedido_view import ItensPedidoViewSet
from comercial.views.ordem_servico_view import OrdemServicoViewSet
from comercial.views.relatorio_view import RelatorioViewSet

router = DefaultRouter()
router.register(r'pagamentos', PagamentoViewSet, basename='pagamentos')
router.register(r'fornecimentos', FornecimentoViewSet, basename='fornecimentos')
router.register(r'itens-pedido', ItensPedidoViewSet, basename='itens-pedido')
router.register(r'ordem-servico', OrdemServicoViewSet, basename='ordem-servico')
router.register(r'relatorio', RelatorioViewSet, basename='relatorio')

urlpatterns = [
    path('', include(router.urls)),
]
