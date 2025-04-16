from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cadastro.models.distribuidor import Distribuidor
from cadastro.serializers.distribuidor_serializer import DistribuidorSerializer

class DistribuidorViewSet(viewsets.ModelViewSet):
    queryset = Distribuidor.objects.all()
    serializer_class = DistribuidorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    # GET /api/distribuidores/pesquisar/?nome=xxx
    @action(detail=False, methods=['get'])
    def pesquisar(self, request):
        nome = request.query_params.get('nome', '')
        distribuidores = Distribuidor.objects.filter(nome__icontains=nome)
        serializer = self.get_serializer(distribuidores, many=True)
        return Response(serializer.data)

    # GET /api/distribuidores/{id}/exibir/
    @action(detail=True, methods=['get'])
    def exibir(self, request, pk=None):
        distribuidor = get_object_or_404(Distribuidor, pk=pk)
        serializer = self.get_serializer(distribuidor)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def inserir(self, request):
        serializer = DistribuidorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Distribuidor inserido com sucesso.', 'distribuidor': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/distribuidores/{id}/remover/
    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        distribuidor = get_object_or_404(Distribuidor, pk=pk)
        try:
            distribuidor.delete()
            return Response({'mensagem': 'Distribuidor removido com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': f'Erro ao remover distribuidor: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # PUT /api/distribuidores/{id}/alterar/
    @action(detail=True, methods=['put'])
    def alterar(self, request, pk=None):
        distribuidor = get_object_or_404(Distribuidor, pk=pk)
        serializer = self.get_serializer(distribuidor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Distribuidor alterado com sucesso.', 'distribuidor': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='listar-nomes')
    def listar_nomes(self, request):
        distribuidores = Distribuidor.objects.all().values('id_distribuidor', 'nome')
        return Response({'distribuidores': list(distribuidores)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='listar')
    def listar(self, request):
        distribuidores = Distribuidor.objects.all().values('id_distribuidor', 'nome', 'cnpj')
        return Response({'distribuidores': list(distribuidores)}, status=status.HTTP_200_OK)

