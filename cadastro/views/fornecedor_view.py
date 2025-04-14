from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cadastro.models.fornecedor import Fornecedor
from cadastro.serializers.fornecedor_serializer import FornecedorSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['get'])
    def pesquisar(self, request):
        nome = request.query_params.get('nome', '')
        fornecedores = Fornecedor.objects.filter(nome__icontains=nome)
        serializer = self.get_serializer(fornecedores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def exibir(self, request, pk=None):
        fornecedor = get_object_or_404(Fornecedor, pk=pk)
        serializer = self.get_serializer(fornecedor)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        fornecedor = get_object_or_404(Fornecedor, pk=pk)
        try:
            fornecedor.delete()
            return Response({'mensagem': 'Fornecedor removido com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': f'Erro ao remover fornecedor: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def alterar(self, request, pk=None):
        fornecedor = get_object_or_404(Fornecedor, pk=pk)
        serializer = self.get_serializer(fornecedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Fornecedor alterado com sucesso.', 'fornecedor': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='listar-nomes')
    def listar_nomes(self, request):
        fornecedores = Fornecedor.objects.all().values_list('nome', flat=True)
        return Response({'fornecedores': list(fornecedores)}, status=status.HTTP_200_OK)
