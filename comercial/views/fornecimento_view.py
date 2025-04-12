from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from comercial.models.fornecimento import Fornecimento
from comercial.serializers.fornecimento_serializer import FornecimentoSerializer
from cadastro.services.fornecedor_service import FornecedorService
from cadastro.services.distribuidor_service import DistribuidorService
from santaclara.service.auxiliar_funcao import FuncoesUteis


class FornecimentoViewSet(viewsets.ModelViewSet):
    queryset = Fornecimento.objects.all()
    serializer_class = FornecimentoSerializer

    @action(detail=False, methods=['post'])
    def inserir(self, request):
        """Registra um novo fornecimento."""
        data = request.data.get("data")
        valor = request.data.get("valor")
        distribuidor_id = request.data.get("distribuidor_id", None)
        produto_id = request.data.get("produto_id")
        fornecedor_id = request.data.get("fornecedor_id")

        try:
            data_fornecimento = datetime.strptime(data, "%Y-%m-%d").date()
            if data_fornecimento > datetime.today().date():
                return Response({"erro": "A data não pode ser maior que hoje."},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"erro": "Data inválida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            valor = round(float(valor), 2)
        except ValueError:
            return Response({"erro": "Valor deve ser um número válido com até duas casas decimais."},
                             status=status.HTTP_400_BAD_REQUEST)

        # Verificar a existência do fornecedor
        if not FuncoesUteis.verificar_existencia("fornecedor", "fornecedor_id", fornecedor_id):
            return Response({"erro": "Fornecedor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar a existência do distribuidor (se fornecido)
        if distribuidor_id and not FuncoesUteis.verificar_existencia("distribuidor", "id_distribuidor", distribuidor_id):
            return Response({"erro": "Distribuidor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar a existência do produto
        if not FuncoesUteis.verificar_existencia("produto", "produto_id", produto_id):
            return Response({"erro": "Produto não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Criar o fornecimento
        try:
            fornecimento = Fornecimento.objects.create(
                data=data_fornecimento,
                valor=valor,
                distribuidor_id=distribuidor_id,
                produto_id=produto_id,
                fornecedor_id=fornecedor_id
            )
            return Response({"message": f"Fornecimento {fornecimento.id} registrado com sucesso!"}, 
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def inserir_fornecimento(self, request):
        """Solicita dados para registrar um fornecimento e retorna sucesso ou falha."""
        produto_id = request.data.get("produto_id")
        valor = request.data.get("valor")
        
        # Verificar se o fornecedor existe
        print("\nFornecedores disponíveis:")
        FornecedorService.listar_todos()
        fornecedor_id = request.data.get("fornecedor_id")
        if not FuncoesUteis.verificar_existencia("fornecedor", "id_fornecedor", fornecedor_id):
            return Response({"erro": "Fornecedor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Listar distribuidores (opcional)
        print("\nDistribuidores disponíveis:")
        DistribuidorService.listar_todos()
        id_distribuidor = request.data.get("distribuidor_id", None)
        
        if id_distribuidor and not FuncoesUteis.verificar_existencia("distribuidor", "id_distribuidor", id_distribuidor):
            return Response({"erro": "Distribuidor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar o valor do fornecimento
        try:
            valor = round(float(valor), 2)
        except ValueError:
            return Response({"erro": "O valor deve ser numérico com até duas casas decimais."}, 
                             status=status.HTTP_400_BAD_REQUEST)

        # Criar fornecimento
        try:
            fornecimento = Fornecimento.objects.create(
                data=datetime.today().date(),
                valor=valor,
                distribuidor_id=id_distribuidor,
                produto_id=produto_id,
                fornecedor_id=fornecedor_id
            )
            return Response({"message": f"Fornecimento {fornecimento.id} registrado para o produto {produto_id}."},
                             status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"erro": f"Erro ao registrar fornecimento: {str(e)}"},
                             status=status.HTTP_400_BAD_REQUEST)
