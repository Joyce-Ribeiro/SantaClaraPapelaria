from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from comercial.models.pagamento import Pagamento
from cadastro.models.pedido import Pedido
from comercial.models.ordem_servico import OrdemServico
from cadastro.models.vendedor import Vendedor
import uuid

class PagamentoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def atualizar_status(self, request):
        id_pedido = request.data.get('id_pedido')
        novo_status = request.data.get('status')
        id_vendedor = request.data.get('id_vendedor')  # <- novo campo

        if not id_pedido or not novo_status or not id_vendedor:
            return Response({'erro': 'id_pedido, status e id_vendedor são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pagamento = Pagamento.objects.get(pedido_id=uuid.UUID(id_pedido) if isinstance(id_pedido, str) else id_pedido)
            pedido = pagamento.pedido
        except Pagamento.DoesNotExist:
            return Response({'erro': 'Pagamento não encontrado para o pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        if novo_status not in dict(Pagamento.STATUS_PAGAMENTO):
            return Response({'erro': 'Status inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar estoque somente se for confirmar
        if novo_status == 'confirmado':
            produtos_sem_estoque = [
                item.produto.nome
                for item in pedido.itens_pedido.all()
                if item.produto.estoque < item.quantidade
            ]

            if produtos_sem_estoque:
                return Response({
                    'erro': f"Não é possível confirmar o pedido. Os seguintes produtos estão sem estoque: {', '.join(produtos_sem_estoque)}."
                }, status=status.HTTP_400_BAD_REQUEST)

        # Atualizar status
        pagamento.status_pagamento = novo_status
        pagamento.save()

        # Atualizar/associar vendedor na Ordem de Serviço
        try:
            vendedor = Vendedor.objects.get(matricula=id_vendedor)
        except Vendedor.DoesNotExist:
            return Response({'erro': 'Vendedor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar OrdemServico com aquele pedido (e opcionalmente o cliente, se houver)
        ordem = OrdemServico.objects.filter(pedido=pedido).first()
        if ordem:
            ordem.vendedor = vendedor
            ordem.save()
        else:
            OrdemServico.objects.create(
                pedido=pedido,
                cliente=pedido.cliente,
                vendedor=vendedor
            )

        return Response({'mensagem': f'Status atualizado para {novo_status} e vendedor associado à ordem de serviço.'}, status=status.HTTP_200_OK)