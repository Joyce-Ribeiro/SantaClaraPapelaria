from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from comercial.models.itens_pedido import ItensPedido
from comercial.serializers.itens_pedido_serializer import ItensPedidoSerializer
from cadastro.models.pedido import Pedido
from comercial.models.ordem_servico import OrdemServico
from cadastro.models.cliente import Cliente
from cadastro.models.produto import Produto
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
            return Response({"message": f"Item {item.id_itensPedido} adicionado ao pedido {id_pedido} com sucesso!"},
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
            return Response({"message": f"Item {item.id_itensPedido} adicionado ao Pedido {id_pedido} com sucesso!"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao adicionar item ao pedido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def criar_pedido_com_itens(self, request):
        """
        Cria um novo pedido com os produtos informados e vincula a um cliente.
        Exemplo de payload:
        {
            "idcliente": [1],
            "idproduto": [1, 2, 3]
        }
        """
        idcliente = request.data.get("idcliente", [])
        idprodutos = request.data.get("idproduto", [])

        if not idcliente:
            return Response({"erro": "Cliente não informado."}, status=status.HTTP_400_BAD_REQUEST)

        idcliente = idcliente[0]  # Assume o primeiro cliente da lista
        if not Cliente.objects.filter(id_cliente=idcliente).exists():
            return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        for id_prod in idprodutos:
            if not Produto.objects.filter(id_produto=id_prod).exists():
                return Response({"erro": f"Produto com ID {id_prod} não encontrado."},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            # Cria o Pedido
            pedido = Pedido.objects.create(data_pedido=timezone.now())

            # Cria a Ordem de Serviço vinculando o cliente ao pedido
            OrdemServico.objects.create(cliente_id=idcliente, pedido=pedido)

            # Cria os ItensPedido
            for id_prod in idprodutos:
                ItensPedido.objects.create(
                    pedido=pedido,
                    produto_id=id_prod,
                    quantidade=1  # Padrão
                )

            return Response({
                "message": "Pedido e itens criados com sucesso!",
                "id_pedido": pedido.id_pedido,
                "id_cliente": idcliente,
                "produtos": idprodutos
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"erro": f"Erro ao criar pedido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
