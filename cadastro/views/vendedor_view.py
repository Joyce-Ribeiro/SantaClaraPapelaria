from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from cadastro.models.vendedor import Vendedor
from cadastro.serializers.vendedor_serializer import (VendedorSerializer, AutenticacaoVendedorSerializer)
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def cadastrar(self, request):
        """
        Cadastra um vendedor.
        """
        matricula = request.data.get('matricula')
        nome = request.data.get('nome')
        senha = request.data.get('senha')
        comissao = request.data.get('comissao', None)

        if not matricula or not nome or not senha:
            return Response({'erro': 'Matrícula, nome e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(matricula) != 8:
            return Response({'erro': 'A matrícula deve conter exatamente 8 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        vendedor = Vendedor.objects.create(
            matricula=matricula,
            nome=nome,
            senha=senha,
            comissao=comissao
        )

        return Response({'mensagem': f'Vendedor {vendedor.nome} cadastrado com sucesso.', 'matricula': vendedor.matricula},
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def inserir(self, request):
        """
        Cadastra um vendedor.
        """
        matricula = request.data.get('matricula')
        nome = request.data.get('nome')
        comissao = request.data.get('comissao', None)
        senha = request.data.get('senha')

        if len(matricula) != 8:
            return Response({"erro": "A matrícula deve conter exatamente 8 caracteres."},
                            status=status.HTTP_400_BAD_REQUEST)

        vendedor = Vendedor.objects.create(
            matricula=matricula,
            nome=nome,
            comissao=comissao,
            senha=senha
        )

        return Response({"message": f"Vendedor {vendedor.nome} cadastrado com sucesso!"}, 
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def alterar(self, request, pk=None):
        """
        Altera os dados de um vendedor.
        """
        vendedor = Vendedor.objects.get(pk=pk)
        nome = request.data.get('nome', vendedor.nome)
        comissao = request.data.get('comissao', vendedor.comissao)
        senha = request.data.get('senha', vendedor.senha)

        vendedor.nome = nome
        vendedor.comissao = comissao
        vendedor.senha = senha
        vendedor.save()

        return Response({"message": f"Vendedor {vendedor.nome} alterado com sucesso!"}, 
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def pesquisar_por_nome(self, request):
        """
        Pesquisa vendedores por nome.
        """
        nome = request.query_params.get('nome')
        vendedores = Vendedor.objects.filter(nome__icontains=nome)

        if vendedores:
            serializer = VendedorSerializer(vendedores, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Nenhum vendedor encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        """
        Remove um vendedor.
        """
        try:
            vendedor = Vendedor.objects.get(pk=pk)
            vendedor.delete()
            return Response({"message": f"Vendedor {vendedor.nome} removido com sucesso!"}, 
                            status=status.HTTP_200_OK)
        except Vendedor.DoesNotExist:
            return Response({"erro": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='autenticar')
    def autenticar(self, request):
        """
        Autentica um vendedor com código (matrícula) e senha via GET.
        Exemplo: /api/vendedores/autenticar/?codigo=AE200403&senha=74185296
        """
        codigo = request.query_params.get('codigo')
        senha = request.query_params.get('senha')

        if not codigo or not senha:
            return Response({'erro': 'Código e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendedor = Vendedor.objects.get(matricula=codigo, senha=senha)
            return Response({'matricula': vendedor.matricula})
        except Vendedor.DoesNotExist:
            return Response({'matricula': None})
