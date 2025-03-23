from rest_framework import serializers
from cadastro.models.fornecedor import Fornecedor

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'  # Isso inclui todos os campos do modelo Fornecedor