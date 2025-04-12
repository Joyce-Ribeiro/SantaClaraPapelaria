from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from comercial.models.pagamento import Pagamento
from comercial.serializers.pagamento_serializer import PagamentoSerializer
from django.db import transaction

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

    def perform_create(self, serializer):
        # Obter o pedido relacionado ao pagamento
        pedido = serializer.validated_data['pedido']

        # Verificar se o estoque de todos os produtos no pedido é suficiente
        for item in pedido.itens_pedido.all():
            if item.produto.estoque < item.quantidade:
                # Caso o estoque seja insuficiente, retornamos um erro
                return Response(
                    {'detail': f'Produto {item.produto.nome} não tem estoque suficiente.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Se todos os produtos tiverem estoque suficiente, criamos o pagamento
        with transaction.atomic():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
