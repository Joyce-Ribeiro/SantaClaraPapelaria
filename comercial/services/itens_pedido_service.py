from db import get_connection
from cadastro.services.produto_service import ProdutoService

class ItensPedidoService:
    
    @staticmethod
    def verificar_existencia(tabela, coluna, valor):
        """Verifica se um registro existe no banco de dados."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM cadastro.{tabela} WHERE {coluna} = %s", (valor,))
        existe = cur.fetchone() is not None
        cur.close()
        conn.close()
        return existe

    @staticmethod
    def inserir():
        from cadastro.services.pedido_service import PedidoService

        """Insere um novo item no pedido após verificar a existência do pedido e do produto."""
        id_pedido = input("ID do Pedido: ")
        id_produto = input("Código do Produto: ")
        quantidade = input("Quantidade: ")

        if not PedidoService.verificar_existencia("pedido", "pedido_id", id_pedido):
            print("Erro: Pedido não encontrado.")
            return

        if not PedidoService.verificar_existencia("produto", "produto_id", id_produto):
            print("Erro: Produto não encontrado.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO comercial.itenspedido (quantidade, id_pedido, id_produto) VALUES (%s, %s, %s) RETURNING id_itenspedido',
            (quantidade, id_pedido, id_produto)
        )
        id_itenspedido = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print(f"Item {id_itenspedido} adicionado ao pedido {id_pedido} com sucesso!")

    @staticmethod
    def inserir_itens_pedido(id_pedido):
        from cadastro.services.pedido_service import PedidoService
        """Adiciona um item ao pedido existente."""
        ProdutoService.listar_todos()
        id_produto = input("Código do Produto: ")
        quantidade = input("Quantidade: ")

        if not PedidoService.verificar_existencia("produto", "produto.cod_produto", id_produto):
            print("Erro: Produto não encontrado.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO comercial.itens_pedido (quantidade, pedido_id, produto_id) VALUES (%s, %s, %s) RETURNING "id_itensPedido"',
            (quantidade, id_pedido, id_produto)
        )
        id_itenspedido = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print(f"Item {id_itenspedido} adicionado ao Pedido {id_pedido} com sucesso!")
