from rest_framework import serializers
from comercial.models.fornecimento import Fornecimento

class FornecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecimento
        fields = '__all__'
