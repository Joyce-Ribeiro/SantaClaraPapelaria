from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from comercial.models.pagamento import Pagamento
from cadastro.models.pedido import Pedido
import uuid

class PagamentoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def atualizar_status(self, request):
        id_pedido = request.data.get('id_pedido')
        novo_status = request.data.get('status')

        if not id_pedido or not novo_status:
            return Response({'erro': 'id_pedido e status são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pagamento = Pagamento.objects.get(pedido__id=uuid.UUID(id_pedido) if isinstance(id_pedido, str) else id_pedido)
            pedido = pagamento.pedido  # Obtém o pedido associado ao pagamento
        except Pagamento.DoesNotExist:
            return Response({'erro': 'Pagamento não encontrado para o pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        if novo_status not in dict(Pagamento.STATUS_PAGAMENTO):
            return Response({'erro': 'Status inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se o estoque está disponível para todos os produtos do pedido
        if novo_status == 'confirmado':  # Só verifica quando for para "confirmado"
            produtos_sem_estoque = []
            for item in pedido.itens_pedido.all():
                if item.produto.estoque < item.quantidade:  # Verifica se o estoque é suficiente
                    produtos_sem_estoque.append(item.produto.nome)

            if produtos_sem_estoque:
                return Response({
                    'erro': f"Não é possível confirmar o pedido. Os seguintes produtos estão sem estoque: {', '.join(produtos_sem_estoque)}."
                }, status=status.HTTP_400_BAD_REQUEST)

        # Atualizar status do pagamento
        pagamento.status_pagamento = novo_status
        pagamento.save()

        return Response({'mensagem': f'Status do pagamento atualizado para {novo_status}.'}, status=status.HTTP_200_OK)