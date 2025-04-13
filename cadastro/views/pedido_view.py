from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from cadastro.models.pedido import Pedido
from cadastro.serializers.pedido_serializer import PedidoSerializer
from cadastro.models.vendedor import Vendedor
from comercial.models.pagamento import Pagamento


from django.db.models import Case, When, Value, IntegerField
from comercial.models.ordem_servico import OrdemServico 

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

    @action(detail=False, methods=['get'], url_path='resumo-pedidos')
    def resumo_pedidos(self, request):
        from comercial.models.ordem_servico import OrdemServico
        from comercial.models.pagamento import Pagamento
        from django.db.models import Case, When, Value, IntegerField

        ordering = Case(
            When(pedido__pagamento__status_pagamento='pendente', then=Value(0)),
            When(pedido__pagamento__status_pagamento='recusado', then=Value(1)),
            When(pedido__pagamento__status_pagamento='confirmado', then=Value(2)),
            default=Value(3),
            output_field=IntegerField()
        )

        ordens = OrdemServico.objects.select_related('cliente', 'vendedor', 'pedido__pagamento') \
            .prefetch_related('pedido__itens_pedido__produto') \
            .annotate(ordem_status=ordering) \
            .order_by('ordem_status')

        resultado = []
        for ordem in ordens:
            cliente = ordem.cliente
            vendedor = ordem.vendedor
            pedido = ordem.pedido
            pagamento = getattr(pedido, 'pagamento', None)

            produtos_info = [
                {
                    "nome_produto": item.produto.nome,
                    "quantidade": item.quantidade
                }
                for item in pedido.itens_pedido.all()
            ]

            resultado.append({
                "id_pedido": pedido.id,
                "nome_cliente": cliente.nome if cliente else None,
                "nome_vendedor": vendedor.nome if vendedor else None,
                "produtos": produtos_info,
                "status_pagamento": pagamento.status_pagamento if pagamento else "sem pagamento"
            })

        return Response(resultado, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['post'], url_path='atualizar-vendedor-pagamento')
    def atualizar_vendedor_pagamento(self, request):
        # Obtendo os parâmetros do corpo da requisição
        id_pedido = request.data.get('id_pedido')
        matricula = request.data.get('matricula')
        novo_status = request.data.get('status_pagamento')

        # Verificando se os parâmetros necessários foram fornecidos
        if not id_pedido or not matricula or not novo_status:
            return Response({'erro': 'Campos obrigatórios: id_pedido, matricula, status_pagamento.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Obtendo o Pedido e o Vendedor, ou retornando erro caso não existam
        pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
        vendedor = get_object_or_404(Vendedor, matricula=matricula)

        # Obtendo a Ordem de Serviço associada ao pedido
        ordem_servico = get_object_or_404(OrdemServico, pedido=pedido)

        # Associando o vendedor à ordem de serviço
        ordem_servico.vendedor = vendedor
        ordem_servico.save()

        # Atualizando o status de pagamento
        try:
            pagamento = pedido.pagamento
            pagamento.status_pagamento = novo_status
            pagamento.save()
        except Pagamento.DoesNotExist:
            return Response({'erro': 'Pagamento não encontrado para esse pedido.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Retorno de sucesso
        return Response({
            'mensagem': 'Vendedor associado e status do pagamento atualizado com sucesso.',
            'pedido': pedido.id_pedido,
            'vendedor': vendedor.nome,
            'novo_status': novo_status
        }, status=status.HTTP_200_OK)