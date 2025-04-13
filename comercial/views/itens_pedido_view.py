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
from comercial.models.pagamento import Pagamento
from django.utils import timezone


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
        Também registra o pagamento com status 'pendente'.
        Clientes especiais recebem 10% de desconto nos itens.
        """
        idcliente = request.data.get("idcliente", [])
        idprodutos = request.data.get("idproduto", [])
        forma_pagamento = request.data.get("forma_pagamento")

        if not idcliente:
            return Response({"erro": "Cliente não informado."}, status=status.HTTP_400_BAD_REQUEST)

        idcliente = idcliente[0]
        try:
            cliente = Cliente.objects.get(id_cliente=idcliente)
        except Cliente.DoesNotExist:
            return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not forma_pagamento or forma_pagamento not in dict(Pagamento.FORMAS_PAGAMENTO):
            return Response({"erro": "Forma de pagamento inválida ou não informada."}, status=status.HTTP_400_BAD_REQUEST)

        for id_prod in idprodutos:
            if not Produto.objects.filter(id_produto=id_prod).exists():
                return Response({"erro": f"Produto com ID {id_prod} não encontrado."},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            pedido = Pedido.objects.create(data_pedido=timezone.now())
            OrdemServico.objects.create(cliente=cliente, pedido=pedido)

            valor_total = 0

            for id_prod in idprodutos:
                produto = Produto.objects.get(id_produto=id_prod)

                valor_unitario = produto.valor_produto
                if cliente.cliente_especial:
                    valor_unitario *= 0.9  # aplica 10% de desconto

                ItensPedido.objects.create(
                    pedido=pedido,
                    produto=produto,
                    quantidade=1
                )

                valor_total += valor_unitario

            pagamento = Pagamento.objects.create(
                pedido=pedido,
                forma_pagamento=forma_pagamento,
                status_pagamento='pendente'
            )

            return Response({
                "message": "Pedido, itens e pagamento criados com sucesso!",
                "id_pedido": pedido.id_pedido,
                "id_pagamento": pagamento.id_pagamento,
                "status_pagamento": pagamento.status_pagamento,
                "cliente_especial": cliente.cliente_especial,
                "valor_total": round(valor_total, 2)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"erro": f"Erro ao criar pedido: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
