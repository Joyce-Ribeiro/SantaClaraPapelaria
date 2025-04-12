from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cadastro.models.cliente import Cliente
from cadastro.serializers.cliente_serializer import ClienteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def cadastrar(self, request):
        """
        Cadastra um cliente.
        """
        nome = request.data.get('nome')
        telefone = request.data.get('telefone')
        senha = request.data.get('senha')
        email = request.data.get('email', None)
        cliente_especial = request.data.get('cliente_especial', False)

        if not nome or not telefone or not senha:
            return Response({'erro': 'Nome, telefone e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        cliente = Cliente.objects.create(
            nome=nome,
            telefone=telefone,
            senha=senha,
            email=email,
            cliente_especial=cliente_especial
        )

        return Response({'mensagem': f'Cliente {cliente.nome} cadastrado com sucesso.', 'id_cliente': cliente.id_cliente},
                        status=status.HTTP_201_CREATED)
    
    # GET /api/clientes/pesquisar/?nome=xxx
    @action(detail=False, methods=['get'])
    def pesquisar(self, request):
        nome = request.query_params.get('nome', '')
        clientes = Cliente.objects.filter(nome__icontains=nome)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)

    # GET /api/clientes/exibir/<id>/
    @action(detail=True, methods=['get'])
    def exibir(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

    # DELETE /api/clientes/remover/<id>/
    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        try:
            cliente.delete()
            return Response({'mensagem': 'Cliente removido com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': f'Erro ao remover cliente: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # PUT /api/clientes/alterar/<id>/
    @action(detail=True, methods=['put'])
    def alterar(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = self.get_serializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Cliente alterado com sucesso.', 'cliente': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # POST /api/clientes/autenticar/
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], parser_classes=[JSONParser])
    def autenticar(self, request):
        codigo = request.data.get('código')  # <-- com acento mesmo
        senha = request.data.get('senha')

        if not codigo or not senha:
            return Response({'erro': 'Código e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Cliente.objects.get(telefone=codigo, senha=senha)
            return Response({'id_cliente': cliente.id_cliente})
        except Cliente.DoesNotExist:
            return Response({'id_cliente': None})

