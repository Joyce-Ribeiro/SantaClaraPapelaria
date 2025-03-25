from db import get_connection
from datetime import datetime
from comercial.services.itens_pedido_service import (inserir_itens_pedido, verificar_existencia)

def inserir():
    """Insere um novo pedido no banco de dados."""
    data_pedido = datetime.now()  # Registra a data e hora atuais

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadastro.pedido (data_pedido) VALUES (%s) RETURNING id_pedido',
        (data_pedido,)
    )
    id_pedido = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Pedido {id_pedido} cadastrado com sucesso!")

    resposta = input("Adicionar itens ao pedido [S/N]: ").strip().upper()
    if resposta == 'S':
        inserir_itens_pedido(id_pedido)
    else:
        print("Pedido sem itens adicionados.")


def alterar():
    """Altera a data de um pedido existente."""
    id_pedido = input("ID do pedido para alterar: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_pedido, data_pedido FROM cadastro.pedido WHERE id_pedido = %s', (id_pedido,))
    pedido = cur.fetchone()

    if not pedido:
        print("Pedido não encontrado.")
        cur.close()
        conn.close()
        return

    print(f"Data atual do pedido: {pedido[1]}")
    nova_data_str = input("Nova data do pedido (YYYY-MM-DD HH:MM:SS): ")
    nova_data_pedido = datetime.strptime(nova_data_str, "%Y-%m-%d %H:%M:%S")

    cur.execute(
        'UPDATE cadastro.pedido SET data_pedido = %s WHERE id_pedido = %s',
        (nova_data_pedido, id_pedido)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Pedido {id_pedido} alterado com sucesso!")

def pesquisar_por_data():
    """Pesquisa pedidos por data."""
    data_str = input("Digite a data do pedido (YYYY-MM-DD): ")
    
    try:
        data_pesquisa = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de data inválido. Use YYYY-MM-DD.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_pedido, data_pedido FROM cadastro.pedido WHERE DATE(data_pedido) = %s", (data_pesquisa,))
    pedidos = cur.fetchall()
    
    if pedidos:
        for p in pedidos:
            print(f"ID: {p[0]}, Data: {p[1]}")
    else:
        print("Nenhum pedido encontrado para esta data.")
    
    cur.close()
    conn.close()

def remover():
    """Remove um pedido do banco de dados."""
    id_pedido = input("ID do pedido para remover: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cadastro.pedido WHERE id_pedido = %s', (id_pedido,))
    
    if cur.rowcount == 0:
        print("Pedido não encontrado.")
    else:
        print(f"Pedido {id_pedido} removido com sucesso.")

    conn.commit()
    cur.close()
    conn.close()

def listar_todos():
    """Lista todos os pedidos cadastrados."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_pedido, data_pedido FROM cadastro.pedido ORDER BY data_pedido DESC')
    pedidos = cur.fetchall()
    
    if pedidos:
        for p in pedidos:
            print(f"ID: {p[0]}, Data: {p[1]}")
    else:
        print("Nenhum pedido cadastrado.")

    cur.close()
    conn.close()

def exibir_um():
    """Exibe detalhes de um pedido específico."""
    id_pedido = input("ID do pedido: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_pedido, data_pedido FROM cadastro.pedido WHERE id_pedido = %s', (id_pedido,))
    p = cur.fetchone()
    
    if p:
        print(f"ID: {p[0]}, Data: {p[1]}")
    else:
        print("Pedido não encontrado.")
    
    cur.close()
    conn.close()

def listar_produtos():
    """Lista os produtos disponíveis com seus IDs."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cod_produto, nome, valor_produto FROM cadastro.produto")
    produtos = cur.fetchall()
    cur.close()
    conn.close()

    print("\nProdutos Disponíveis:")
    for p in produtos:
        print(f"ID: {p[0]} - Nome: {p[1]} - Valor: R${p[2]:.2f}")

    return produtos

def inserir_pedido():
    """Cadastra um pedido e permite adicionar vários produtos a ele."""

    escolha = input("Criar pedido para (1) Cliente ou (2) Vendedor? ")

    if escolha == "1":
        id_cliente = input("ID do Cliente: ")
        if not verificar_existencia("cliente", "id_cliente", id_cliente):
            print("Erro: Cliente não encontrado.")
            return
        matricula_vendedor = None
    elif escolha == "2":
        matricula_vendedor = input("Matrícula do Vendedor: ")
        if not verificar_existencia("vendedor", "matricula", matricula_vendedor):
            print("Erro: Vendedor não encontrado.")
            return
        id_cliente = None
    else:
        print("Escolha inválida.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadastro.pedido (data_pedido) VALUES (CURRENT_TIMESTAMP) RETURNING id_pedido'
    )
    id_pedido = cur.fetchone()[0]
    conn.commit()

    print(f"\nPedido {id_pedido} criado com sucesso!")

    # Adicionar produtos ao pedido
    listar_produtos()
    while True:
        inserir_itens_pedido(id_pedido)
        continuar = input("Deseja adicionar outro produto? (S/N): ").strip().lower()
        if continuar != 's':
            break

    cur.close()
    conn.close()
    print(f"\nPedido {id_pedido} finalizado com sucesso!")
