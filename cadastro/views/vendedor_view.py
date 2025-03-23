from rest_framework import viewsets
from cadastro.models.vendedor import Vendedor
from cadastro.serializers.vendedor_serializer import VendedorSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()  # Obtém todos os vendedores
    serializer_class = VendedorSerializer  # Define o serializer para este viewset
