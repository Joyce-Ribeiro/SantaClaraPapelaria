from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cadastro.models.cliente import Cliente
from cadastro.serializers.cliente_serializer import ClienteSerializer
from rest_framework.permissions import AllowAny
from decimal import Decimal
from cadastro.utils.criptografia_bcrypt_helper import CriptografiaBcryptHelper
from cadastro.utils.criptografia_sha_helper import CriptografiaShaHelper
from django.db import IntegrityError
from django.db.models import Case, When, Value, IntegerField
from comercial.models.ordem_servico import OrdemServico
import re

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def cadastrar(self, request):
        nome = request.data.get('nome')
        telefone = request.data.get('telefone')
        senha = request.data.get('senha')
        email = request.data.get('email', None)
        cidade = request.data.get('cidade', None)

        if not nome or not telefone or not senha:
            return Response({'erro': 'Nome, telefone e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        if not CriptografiaShaHelper.validar_telefone(telefone):
            return Response({'erro': 'Telefone inválido. Deve estar no formato com DDD e começar com 9.'}, status=status.HTTP_400_BAD_REQUEST)

        telefone_criptografado = CriptografiaShaHelper.hash_telefone(telefone)
        senha_criptografada = CriptografiaBcryptHelper.hash_senha(senha)

        try:
            cliente = Cliente.objects.create(
                nome=nome,
                telefone=telefone_criptografado,
                senha=senha_criptografada,
                email=email,
                cidade=cidade
            )
        except IntegrityError:
            return Response({'erro': 'Telefone já cadastrado.'}, status=status.HTTP_409_CONFLICT)

        return Response({
            'mensagem': f'Cliente {cliente.nome} cadastrado com sucesso.',
            'id_cliente': cliente.id_cliente
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def pesquisar(self, request):
        nome = request.query_params.get('nome', '')
        clientes = Cliente.objects.filter(nome__icontains=nome)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def exibir(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        serializer = self.get_serializer(cliente)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remover(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        try:
            cliente.delete()
            return Response({'mensagem': 'Cliente removido com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'erro': f'Erro ao remover cliente: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def alterar(self, request, pk=None):
        cliente = get_object_or_404(Cliente, pk=pk)
        dados = request.data.copy()

        telefone = dados.get('telefone')
        if telefone is not None and telefone != '':
            if not CriptografiaShaHelper.validar_telefone(telefone):
                return Response({'erro': 'Telefone inválido. Deve estar no formato com DDD e começar com 9.'}, status=status.HTTP_400_BAD_REQUEST)

            dados['telefone'] = CriptografiaShaHelper.hash_telefone(telefone)
        elif telefone == '':
            dados.pop('telefone', None)

        senha = dados.get('senha')
        if senha is not None and senha != '':
            dados['senha'] = CriptografiaBcryptHelper.hash_senha(senha)
        elif senha == '':
            dados.pop('senha', None)

        serializer = self.get_serializer(cliente, data=dados, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Cliente alterado com sucesso.', 'cliente': serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='autenticar')
    def autenticar(self, request):
        telefone = request.query_params.get('telefone')
        senha = request.query_params.get('senha')

        if not telefone or not senha:
            return Response({'erro': 'Telefone e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        telefone_normalizado = CriptografiaShaHelper.normalizar_telefone(telefone)
        telefone_hash = CriptografiaShaHelper.hash_telefone(telefone_normalizado)

        try:
            cliente = Cliente.objects.get(telefone=telefone_hash)
        except Cliente.DoesNotExist:
            return Response({'erro': 'Telefone ou senha inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)

        if CriptografiaBcryptHelper.verificar_senha(senha, cliente.senha):
            return Response({
                'id_cliente': cliente.id_cliente,
                'nome': cliente.nome,
                'telefone': telefone,
                'cidade': cliente.cidade
            })

        return Response({'erro': 'Telefone ou senha inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], url_path='resumo-por-cliente')
    def resumo_por_cliente(self, request):
        id_cliente = request.query_params.get('id_cliente')
        if not id_cliente:
            return Response({'erro': 'Parâmetro "id_cliente" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        cliente = get_object_or_404(Cliente, id_cliente=id_cliente)

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

            cidade_desconto = cliente.cidade and cliente.cidade.lower() == "sousa"
            cupom_desconto = pedido.cupom and pedido.cupom.lower() in ["onepiece", "flamengo"]
            tem_desconto = cidade_desconto or cupom_desconto

            for item in pedido.itens_pedido.all():
                valor_unitario = item.produto.valor_produto
                if tem_desconto:
                    valor_unitario *= Decimal('0.9')  # aplica 10% de desconto

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
