from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from django.db import connection
from rest_framework.response import Response
from cadastro.models.produto import Produto
from cadastro.serializers.produto_serializer import ProdutoSerializer
from comercial.models.fornecimento import Fornecimento
from cadastro.models.fornecedor import Fornecedor
from cadastro.models.distribuidor import Distribuidor
from django.utils import timezone
from decimal import Decimal
from django.shortcuts import get_object_or_404

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']


    @action(detail=False, methods=['post'], url_path='inserir-com-fornecedor')
    def inserir_com_fornecedor(self, request):
        """
        Cadastra um produto e cria um fornecimento associado.
        Fornecedor e Distribuidor são buscados por nome.
        """
        nome = request.data.get('nome')
        valor_produto = request.data.get('valor_produto')
        estoque = request.data.get('estoque')
        desc_produto = request.data.get('desc_produto', '')
        nome_fornecedor = request.data.get('nome_fornecedor')
        nome_distribuidor = request.data.get('nome_distribuidor', None)

        # Validações iniciais
        if not nome or not valor_produto or not estoque or not nome_fornecedor:
            return Response({"erro": "Campos obrigatórios: nome, valor_produto, estoque, nome_fornecedor."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            valor_produto = round(Decimal(valor_produto), 2)
        except:
            return Response({"erro": "Valor do produto deve ser numérico com até duas casas decimais."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            estoque = int(estoque)
        except:
            return Response({"erro": "Estoque deve ser um número inteiro."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fornecedor = Fornecedor.objects.get(nome__iexact=nome_fornecedor)
        except Fornecedor.DoesNotExist:
            return Response({"erro": f"Fornecedor '{nome_fornecedor}' não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        distribuidor = None
        if nome_distribuidor:
            try:
                distribuidor = Distribuidor.objects.get(nome__iexact=nome_distribuidor)
            except Distribuidor.DoesNotExist:
                return Response({"erro": f"Distribuidor '{nome_distribuidor}' não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Criação do produto
        produto = Produto.objects.create(
            nome=nome,
            valor_produto=valor_produto,
            estoque=estoque,
            desc_produto=desc_produto
        )

        try:
            Fornecimento.objects.create(
                data=timezone.now(),
                valor=valor_produto,
                distribuidor=distribuidor,
                produto=produto,
                fornecedor=fornecedor
            )
            return Response({
                "message": f"Produto '{produto.nome}' e fornecimento cadastrados com sucesso."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            produto.delete()
            return Response({"erro": f"Erro ao criar fornecimento: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def alterar(self, request, pk=None):
        """
        Altera parcialmente os dados de um produto.
        """
        try:
            produto = Produto.objects.get(pk=pk)
        except Produto.DoesNotExist:
            return Response({"erro": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        nome = request.data.get('nome', produto.nome)
        valor_produto = request.data.get('valor_produto', produto.valor_produto)
        estoque = request.data.get('estoque', produto.estoque)
        desc_produto = request.data.get('desc_produto', produto.desc_produto)

        try:
            valor_produto = round(float(valor_produto), 2)
        except (ValueError, TypeError):
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
    
    @action(detail=False, methods=['post'], url_path='registrar-entrada-estoque')
    def registrar_entrada_estoque(self, request):
        """
        Registra entrada de estoque via procedure.
        Agora espera:
        - nome_produto
        - nome_fornecedor
        - nome_distribuidor
        - quantidade
        """

        nome_produto = request.data.get('nome_produto')
        nome_fornecedor = request.data.get('nome_fornecedor')
        nome_distribuidor = request.data.get('nome_distribuidor')
        quantidade = request.data.get('quantidade')

        if not (nome_produto and nome_fornecedor and nome_distribuidor and quantidade):
            return Response({"erro": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            produto = Produto.objects.get(nome__iexact=nome_produto)
            fornecedor = Fornecedor.objects.get(nome__iexact=nome_fornecedor)
            distribuidor = Distribuidor.objects.get(nome__iexact=nome_distribuidor)
            quantidade = int(quantidade)
        except Produto.DoesNotExist:
            return Response({"erro": f"Produto '{nome_produto}' não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Fornecedor.DoesNotExist:
            return Response({"erro": f"Fornecedor '{nome_fornecedor}' não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Distribuidor.DoesNotExist:
            return Response({"erro": f"Distribuidor '{nome_distribuidor}' não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"erro": "Quantidade deve ser um número inteiro."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL comercial.registrar_entrada_estoque(%s, %s, %s, %s)", [
                    produto.cod_produto, quantidade, fornecedor.id_fornecedor, distribuidor.id_distribuidor
                ])
            return Response({"mensagem": "Entrada de estoque registrada com sucesso!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"erro": f"Erro ao registrar entrada de estoque: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['get'], url_path='filtrar')
    def filtrar(self, request):
        nome = request.query_params.get('nome')
        preco_min = request.query_params.get('preco_min')
        preco_max = request.query_params.get('preco_max')
        fornecido_em_mari = request.query_params.get('fornecido_em_mari') == 'true'

        produtos = Produto.objects.all()

        if nome:
            produtos = produtos.filter(nome__icontains=nome)

        if preco_min:
            produtos = produtos.filter(valor_produto__gte=preco_min)

        if preco_max:
            produtos = produtos.filter(valor_produto__lte=preco_max)

        if fornecido_em_mari:
            produtos = produtos.filter(fornecimentos__fornecedor__nome__iexact="Mari").distinct()

        dados = [{
            'cod_produto': p.cod_produto,
            'nome': p.nome,
            'valor_produto': float(p.valor_produto),
            'estoque': p.estoque
        } for p in produtos]

        return Response(dados, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['get'], url_path='filtrar-vendedor') 
    def filtrar_vendedor(self, request):
        nome = request.query_params.get('nome')
        preco_min = request.query_params.get('preco_min')
        preco_max = request.query_params.get('preco_max')
        fornecido_em_mari = request.query_params.get('fornecido_em_mari') == 'true'
        estoque_baixo = request.query_params.get('estoque_baixo') == 'true'

        produtos = Produto.objects.all()

        if nome:
            produtos = produtos.filter(nome__icontains=nome)

        if preco_min:
            produtos = produtos.filter(valor_produto__gte=preco_min)

        if preco_max:
            produtos = produtos.filter(valor_produto__lte=preco_max)

        if fornecido_em_mari:
            produtos = produtos.filter(fornecimentos__fornecedor__nome__iexact="Mari").distinct()

        if estoque_baixo:
            produtos = produtos.filter(estoque__lt=5)

        dados = [{
            'cod_produto': p.cod_produto,
            'nome': p.nome,
            'valor_produto': float(p.valor_produto),
            'estoque': p.estoque,
            'desc_produto': p.desc_produto
        } for p in produtos]

        return Response(dados, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='listar-nomes')
    def listar_nomes(self, request):
        produtos = Produto.objects.all().values('cod_produto', 'nome')
        return Response({'produtos': list(produtos)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='buscar-por-id')
    def buscar_por_id(self, request):
        """
        Retorna o nome e o valor do produto a partir do ID informado via query param.
        Exemplo: /api/produtos/buscar-por-id/?id=1
        """
        produto_id = request.query_params.get('id')
        if not produto_id:
            return Response({'erro': 'Parâmetro "id" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        produto = get_object_or_404(Produto, cod_produto=produto_id)

        return Response({
            'nome': produto.nome,
            'valor_produto': float(produto.valor_produto)
        })
