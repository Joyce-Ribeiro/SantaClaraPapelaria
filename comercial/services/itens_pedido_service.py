from db import get_connection

def verificar_existencia(tabela, coluna, valor):
    """Verifica se um registro existe no banco de dados."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM cadastro.{tabela} WHERE {coluna} = %s", (valor,))
    existe = cur.fetchone() is not None
    cur.close()
    conn.close()
    return existe

def inserir():
    """Insere um novo item no pedido após verificar a existência do pedido e do produto."""
    id_pedido = input("ID do Pedido: ")
    cod_produto = input("Código do Produto: ")
    quantidade = input("Quantidade: ")

    if not verificar_existencia("pedido", "id_pedido", id_pedido):
        print("Erro: Pedido não encontrado.")
        return

    if not verificar_existencia("produto", "cod_produto", cod_produto):
        print("Erro: Produto não encontrado.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO comercial.itenspedido (quantidade, id_pedido, cod_produto) VALUES (%s, %s, %s) RETURNING id_itenspedido',
        (quantidade, id_pedido, cod_produto)
    )
    id_itenspedido = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Item {id_itenspedido} adicionado ao pedido {id_pedido} com sucesso!")

def inserir_itens_pedido(id_pedido):
    """Adiciona um item ao pedido existente."""
    cod_produto = input("Código do Produto: ")
    quantidade = input("Quantidade: ")

    if not verificar_existencia("produto", "cod_produto", cod_produto):
        print("Erro: Produto não encontrado.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadastro.itenspedido (quantidade, id_pedido, cod_produto) VALUES (%s, %s, %s) RETURNING id_itenspedido',
        (quantidade, id_pedido, cod_produto)
    )
    id_itenspedido = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Item {id_itenspedido} adicionado ao Pedido {id_pedido} com sucesso!")

