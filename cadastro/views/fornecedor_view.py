from rest_framework import viewsets
from cadastro.models.fornecedor import Fornecedor
from cadastro.serializers.fornecedor_serializer import FornecedorSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()  # Obtém todos os fornecedores
    serializer_class = FornecedorSerializer  # Define o serializer para este viewset