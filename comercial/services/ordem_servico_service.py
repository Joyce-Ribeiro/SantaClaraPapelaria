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
    """Insere uma nova ordem de serviço, garantindo que pelo menos Cliente ou Vendedor exista."""
    id_cliente = input("ID do Cliente (ou pressione Enter para ignorar): ")
    matricula_vendedor = input("Matrícula do Vendedor (ou pressione Enter para ignorar): ")
    id_pedido = input("ID do Pedido: ")

    if not id_cliente and not matricula_vendedor:
        print("Erro: Deve haver pelo menos um Cliente ou um Vendedor.")
        return

    if id_cliente and not verificar_existencia("cliente", "id_cliente", id_cliente):
        print("Erro: Cliente não encontrado.")
        return

    if matricula_vendedor and not verificar_existencia("vendedor", "matricula", matricula_vendedor):
        print("Erro: Vendedor não encontrado.")
        return

    if not verificar_existencia("pedido", "id_pedido", id_pedido):
        print("Erro: Pedido não encontrado.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO comercial.ordemservico (id_cliente, id_pedido, matricula_vendedor) VALUES (%s, %s, %s) RETURNING id_ordem',
        (id_cliente if id_cliente else None, id_pedido, matricula_vendedor if matricula_vendedor else None)
    )
    id_ordem = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Ordem de Serviço {id_ordem} cadastrada com sucesso!")
