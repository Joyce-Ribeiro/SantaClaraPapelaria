from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from cadastro.models.pedido import Pedido
from cadastro.serializers.pedido_serializer import PedidoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-data_pedido')
    serializer_class = PedidoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['data_pedido']

    @action(detail=False, methods=['get'])
    def pesquisar_por_data(self, request):
        data_str = request.query_params.get('data')
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return Response({'erro': 'Data inválida. Formato correto: YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        pedidos = Pedido.objects.filter(data_pedido__date=data)
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def produtos(self, request, pk=None):
        from comercial.models.itens_pedido import ItensPedido  # se o relacionamento estiver em outra app
        from cadastro.serializers.produto_serializer import ProdutoSerializer  # certifique-se de que esse existe

        itens = ItensPedido.objects.filter(pedido_id=pk).select_related('produto')
        produtos = [item.produto for item in itens]
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
