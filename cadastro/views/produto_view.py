from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from cadastro.models.produto import Produto
from cadastro.serializers.produto_serializer import ProdutoSerializer
from comercial.services.fornecimento_service import FornecimentoService

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['post'])
    def inserir_com_fornecedor(self, request):
        """
        Cadastra um produto e, opcionalmente, adiciona um fornecedor.
        """
        nome = request.data.get('nome')
        valor_produto = request.data.get('valor_produto')
        estoque = request.data.get('estoque')
        desc_produto = request.data.get('desc_produto', None)

        try:
            valor_produto = round(float(valor_produto), 2)
        except ValueError:
            return Response({"erro": "Valor do produto deve ser numérico com até duas casas decimais."},
                            status=status.HTTP_400_BAD_REQUEST)

        produto = Produto.objects.create(
            nome=nome,
            valor_produto=valor_produto,
            estoque=estoque,
            desc_produto=desc_produto
        )

        # Verifica se o fornecedor será adicionado
        adicionar_fornecedor = request.data.get('adicionar_fornecedor', False)

        if adicionar_fornecedor:
            sucesso = FornecimentoService.inserir_fornecimento(produto.id)
            if not sucesso:
                produto.delete()
                return Response({"erro": "Erro ao criar fornecimento. Produto não será cadastrado."},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"Fornecimento cadastrado para o produto {produto.nome}."},
                            status=status.HTTP_201_CREATED)

        return Response({"message": f"Produto {produto.nome} cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def alterar(self, request, pk=None):
        """
        Altera os dados de um produto.
        """
        produto = Produto.objects.get(pk=pk)
        nome = request.data.get('nome', produto.nome)
        valor_produto = request.data.get('valor_produto', produto.valor_produto)
        estoque = request.data.get('estoque', produto.estoque)
        desc_produto = request.data.get('desc_produto', produto.desc_produto)

        try:
            valor_produto = round(float(valor_produto), 2)
        except ValueError:
            return Response({"erro": "Valor do produto deve ser numérico com até duas casas decimais."},
                            status=status.HTTP_400_BAD_REQUEST)

        produto.nome = nome
        produto.valor_produto = valor_produto
        produto.estoque = estoque
        produto.desc_produto = desc_produto
        produto.save()

        return Response({"message": "Produto alterado com sucesso!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def pesquisar_por_nome(self, request):
        """
        Pesquisa produtos por nome.
        """
        nome = request.query_params.get('nome')
        produtos = Produto.objects.filter(nome__icontains=nome)

        if produtos:
            serializer = ProdutoSerializer(produtos, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Nenhum produto encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        """
        Remove um produto.
        """
        try:
            produto = Produto.objects.get(pk=pk)
            produto.delete()
            return Response({"message": "Produto removido com sucesso!"}, status=status.HTTP_200_OK)
        except Produto.DoesNotExist:
            return Response({"erro": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
