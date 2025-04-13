from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.http import HttpResponse
from io import BytesIO, TextIOWrapper
import csv

class RelatorioViewSet(ViewSet):

    @action(detail=False, methods=['get'])
    def faturamento_csv(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        if not data_inicio or not data_fim:
            return HttpResponse("Parâmetros 'data_inicio' e 'data_fim' são obrigatórios.", status=400)

        sql = "SELECT * FROM comercial.relatorio_faturamento(%s, %s)"
        params = [data_inicio, data_fim]
        return self._generate_csv(sql, "relatorio_faturamento.csv", params)

    @action(detail=False, methods=['get'])
    def alerta_estoque_csv(self, request):
        return self._generate_csv("SELECT * FROM alerta_estoque", "alerta_estoque.csv")

    @action(detail=False, methods=['get'])
    def vendas_vendedor_csv(self, request):
        return self._generate_csv("SELECT * FROM comercial.relatorio_vendas_vendedor()", "relatorio_vendas_vendedor.csv")

    def _generate_csv(self, sql, filename, params=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        buffer = BytesIO()
        text_stream = TextIOWrapper(buffer, encoding='utf-8-sig', newline='') 

        writer = csv.writer(text_stream, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)

        text_stream.flush()
        buffer.seek(0)

        response = HttpResponse(buffer.read(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
