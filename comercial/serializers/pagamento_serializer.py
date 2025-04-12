from rest_framework import serializers
from comercial.models.pagamento import Pagamento

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
