from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from comercial.models.ordem_servico import OrdemServico
from comercial.serializers.ordem_servico_serializer import OrdemServicoSerializer
from santaclara.service.auxiliar_funcao import FuncoesUteis

class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all()
    serializer_class = OrdemServicoSerializer

    @action(detail=False, methods=['post'])
    def inserir(self, request):
        """Insere uma nova ordem de serviço, garantindo que pelo menos Cliente ou Vendedor exista."""
        id_cliente = request.data.get("id_cliente")
        matricula_vendedor = request.data.get("matricula_vendedor")
        id_pedido = request.data.get("id_pedido")

        if not id_cliente and not matricula_vendedor:
            return Response({"erro": "Deve haver pelo menos um Cliente ou um Vendedor."}, status=status.HTTP_400_BAD_REQUEST)

        if id_cliente and not FuncoesUteis.verificar_existencia("cliente", "id_cliente", id_cliente):
            return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if matricula_vendedor and not FuncoesUteis.verificar_existencia("vendedor", "matricula", matricula_vendedor):
            return Response({"erro": "Vendedor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        if not FuncoesUteis.verificar_existencia("pedido", "id_pedido", id_pedido):
            return Response({"erro": "Pedido não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ordem_servico = OrdemServico.objects.create(
                cliente_id=id_cliente if id_cliente else None,
                vendedor_id=matricula_vendedor if matricula_vendedor else None,
                pedido_id=id_pedido
            )
            return Response({"message": f"Ordem de Serviço {ordem_servico.id} cadastrada com sucesso!"}, 
                             status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao criar ordem de serviço: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def inserir_ordem_servico_vendedor(self, request):
        """Insere uma ordem de serviço vinculada a um vendedor."""
        matricula_vendedor = request.data.get("matricula_vendedor")
        id_pedido = request.data.get("id_pedido")

        if not FuncoesUteis.verificar_existencia("vendedor", "matricula", matricula_vendedor):
            return Response({"erro": "Vendedor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ordem_servico = OrdemServico.objects.create(
                vendedor_id=matricula_vendedor,
                pedido_id=id_pedido
            )
            return Response({"message": f"Ordem de Serviço {ordem_servico.id} cadastrada com sucesso para o vendedor {matricula_vendedor}!"}, 
                             status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao criar ordem de serviço para o vendedor: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def inserir_ordem_servico_cliente(self, request):
        """Insere uma ordem de serviço vinculada a um cliente."""
        id_cliente = request.data.get("id_cliente")
        id_pedido = request.data.get("id_pedido")

        if not FuncoesUteis.verificar_existencia("cliente", "id_cliente", id_cliente):
            return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ordem_servico = OrdemServico.objects.create(
                cliente_id=id_cliente,
                pedido_id=id_pedido
            )
            return Response({"message": f"Ordem de Serviço {ordem_servico.id} cadastrada com sucesso para o cliente {id_cliente}!"}, 
                             status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao criar ordem de serviço para o cliente: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
