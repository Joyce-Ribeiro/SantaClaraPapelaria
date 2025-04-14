import re
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cadastro.models.cliente import Cliente
from cadastro.serializers.cliente_serializer import ClienteSerializer
from rest_framework.permissions import AllowAny

from django.db.models import Case, When, Value, IntegerField
from comercial.models.ordem_servico import OrdemServico 

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def cadastrar(self, request):
        """
        Cadastra um cliente.
        """
        nome = request.data.get('nome')
        telefone = request.data.get('telefone')
        senha = request.data.get('senha')
        email = request.data.get('email', None)
        cidade = request.data.get('cidade', None)

        if not nome or not telefone or not senha:
            return Response({'erro': 'Nome, telefone e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        cliente = Cliente.objects.create(
            nome=nome,
            telefone=telefone,
            senha=senha,
            email=email,
            cidade=cidade
        )

        return Response({
            'mensagem': f'Cliente {cliente.nome} cadastrado com sucesso.',
            'id_cliente': cliente.id_cliente
        }, status=status.HTTP_201_CREATED)

    
    # GET /api/clientes/pesquisar/?nome=xxx
    @action(detail=False, methods=['get'])
    def pesquisar(self, request):
        nome = request.query_params.get('nome', '')
        clientes = Cliente.objects.filter(nome__icontains=nome)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)

    # GET /api/clientes/exibir/<id>/
    @action(detail=True, methods=['get'])
    def exibir(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

    # DELETE /api/clientes/remover/<id>/
    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        try:
            cliente.delete()
            return Response({'mensagem': 'Cliente removido com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': f'Erro ao remover cliente: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # PUT /api/clientes/alterar/<id>/
    @action(detail=True, methods=['put'])
    def alterar(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = self.get_serializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Cliente alterado com sucesso.', 'cliente': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # GET /api/clientes/autenticar/
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='autenticar')
    def autenticar(self, request):
        telefone = request.query_params.get('telefone')
        senha = request.query_params.get('senha')

        if not telefone or not senha:
            return Response({'erro': 'Telefone e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        telefone_normalizado = re.sub(r'\D', '', telefone)

        try:
            cliente = Cliente.objects.get(
                telefone__regex=r'\D*'.join(telefone_normalizado),
                senha=senha
            )
            return Response({
                'id_cliente': cliente.id_cliente,
                'nome': cliente.nome,
                'telefone': cliente.telefone,
                'cidade': cliente.cidade
            })
        except Cliente.DoesNotExist:
            return Response({
                'id_cliente': None,
                'nome': None,
                'telefone': None,
                'cidade': None
            })


    
    @action(detail=False, methods=['get'], url_path='resumo-por-cliente')
    def resumo_por_cliente(self, request):
        telefone = request.query_params.get('telefone')
        if not telefone:
            return Response({'erro': 'Parâmetro "telefone" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        cliente = get_object_or_404(Cliente, telefone=telefone)

        ordering = Case(
            When(pedido__pagamento__status_pagamento='pendente', then=Value(0)),
            When(pedido__pagamento__status_pagamento='recusado', then=Value(1)),
            When(pedido__pagamento__status_pagamento='confirmado', then=Value(2)),
            default=Value(3),
            output_field=IntegerField()
        )

        ordens = OrdemServico.objects.select_related(
            'pedido__pagamento'
        ).prefetch_related(
            'pedido__itens_pedido__produto'
        ).filter(
            cliente=cliente
        ).annotate(
            ordem_status=ordering
        ).order_by('ordem_status')

        resultado = []
        for ordem in ordens:
            pedido = ordem.pedido
            pagamento = getattr(pedido, 'pagamento', None)

            produtos_info = []
            valor_total = 0

            # Aplica a lógica de desconto: cidade ou cupom
            cidade_desconto = cliente.cidade and cliente.cidade.lower() == "sousa"
            cupom_desconto = pedido.cupom and pedido.cupom.lower() in ["onepiece", "flamengo"]
            tem_desconto = cidade_desconto or cupom_desconto

            for item in pedido.itens_pedido.all():
                valor_unitario = item.produto.valor_produto
                if tem_desconto:
                    valor_unitario *= 0.9  # aplica 10% de desconto

                subtotal = item.quantidade * valor_unitario
                valor_total += subtotal

                produtos_info.append({
                    "nome_produto": item.produto.nome,
                    "quantidade": item.quantidade,
                    "valor_unitario": float(valor_unitario),
                    "subtotal": float(subtotal)
                })

            resultado.append({
                "id_pedido": pedido.id_pedido,
                "produtos": produtos_info,
                "valor_total": round(valor_total, 2),
                "forma_pagamento": pagamento.forma_pagamento if pagamento else "sem pagamento",
                "status_pagamento": pagamento.status_pagamento if pagamento else "sem pagamento",
                "desconto_aplicado": tem_desconto
            })

        return Response(resultado, status=status.HTTP_200_OK)
