from rest_framework import serializers
from cadastro.models.vendedor import Vendedor

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'
        
class AutenticacaoVendedorSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=8)
    senha = serializers.CharField(max_length=100)