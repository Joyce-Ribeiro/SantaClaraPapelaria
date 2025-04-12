from rest_framework import viewsets
from comercial.models.pagamento import Pagamento
from comercial.serializers.pagamento_serializer import PagamentoSerializer

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
