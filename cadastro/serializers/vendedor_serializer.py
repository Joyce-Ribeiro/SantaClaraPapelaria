from rest_framework import serializers
from cadastro.models.vendedor import Vendedor

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'  # Isso inclui todos os campos do modelo Vendedor
