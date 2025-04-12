from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from comercial.models.itens_pedido import ItensPedido
from comercial.serializers.itens_pedido_serializer import ItensPedidoSerializer
from cadastro.services.produto_service import ProdutoService
from santaclara.service.auxiliar_funcao import FuncoesUteis

class ItensPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItensPedido.objects.all()
    serializer_class = ItensPedidoSerializer

    @action(detail=False, methods=['post'])
    def inserir(self, request):
        """Insere um novo item no pedido após verificar a existência do pedido e do produto."""
        id_pedido = request.data.get("id_pedido")
        id_produto = request.data.get("id_produto")
        quantidade = request.data.get("quantidade")

        if not FuncoesUteis.verificar_existencia("pedido", "pedido_id", id_pedido):
            return Response({"erro": "Pedido não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not FuncoesUteis.verificar_existencia("produto", "produto_id", id_produto):
            return Response({"erro": "Produto não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = ItensPedido.objects.create(
                pedido_id=id_pedido,
                produto_id=id_produto,
                quantidade=quantidade
            )
            return Response({"message": f"Item {item.id} adicionado ao pedido {id_pedido} com sucesso!"}, 
                             status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao adicionar item: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def inserir_itens_pedido(self, request):
        """Adiciona um item ao pedido existente."""
        id_pedido = request.data.get("id_pedido")
        id_produto = request.data.get("id_produto")
        quantidade = request.data.get("quantidade")

        if not FuncoesUteis.verificar_existencia("produto", "produto_id", id_produto):
            return Response({"erro": "Produto não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = ItensPedido.objects.create(
                pedido_id=id_pedido,
                produto_id=id_produto,
                quantidade=quantidade
            )
            return Response({"message": f"Item {item.id} adicionado ao Pedido {id_pedido} com sucesso!"}, 
                             status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao adicionar item ao pedido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
