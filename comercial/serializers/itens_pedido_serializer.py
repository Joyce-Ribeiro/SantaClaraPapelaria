from rest_framework import serializers
from comercial.models.itens_pedido import ItensPedido

class ItensPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItensPedido
        fields = '__all__'
