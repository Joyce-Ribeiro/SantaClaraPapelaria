from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cadastro.models.cliente import Cliente
from cadastro.serializers.cliente_serializer import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

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
