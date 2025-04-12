from rest_framework import serializers
from cadastro.models.distribuidor import Distribuidor

class DistribuidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribuidor
        fields = '__all__'
