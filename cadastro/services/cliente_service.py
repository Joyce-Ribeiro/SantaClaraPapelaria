from db import get_connection

def inserir():
    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")
    senha = input("Senha: ")
    email = input("Email (opcional): ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadastro.cliente (nome, telefone, senha, email) VALUES (%s, %s, %s, %s)',
        (nome, telefone, senha, email if email else None)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Cliente cadastrado com sucesso!")

def alterar():
    id_cliente = input("ID do cliente para alterar: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_cliente, nome, telefone, senha, email FROM cadastro.cliente WHERE id_cliente = %s', (id_cliente,))
    cliente = cur.fetchone()

    if not cliente:
        print("Cliente não encontrado.")
        cur.close()
        conn.close()
        return

    print(f"Cliente atual: Nome: {cliente[1]}, Telefone: {cliente[2]}, Senha: {cliente[3]}, Email: {cliente[4]}")

    novo_nome = input(f"Novo nome ({cliente[1]}): ") or cliente[1]
    novo_telefone = input(f"Novo telefone ({cliente[2]}): ") or cliente[2]
    nova_senha = input(f"Nova senha ({cliente[3]}): ") or cliente[3]
    novo_email = input(f"Novo email ({cliente[4]}): ") or cliente[4]

    cur.execute(
        'UPDATE cadastro.cliente SET nome = %s, telefone = %s, senha = %s, email = %s WHERE id_cliente = %s',
        (novo_nome, novo_telefone, nova_senha, novo_email if novo_email else None, id_cliente)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Cliente alterado com sucesso!")

def pesquisar_por_nome():
    nome = input("Nome para pesquisa: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_cliente, nome, telefone, senha, email FROM cadastro.cliente WHERE nome ILIKE %s', (f'%{nome}%',))
    clientes = cur.fetchall()
    if clientes:
        for c in clientes:
            print(f"ID: {c[0]}, Nome: {c[1]}, Telefone: {c[2]}, Senha: {c[3]}, Email: {c[4]}")
    else:
        print("Nenhum cliente encontrado.")
    cur.close()
    conn.close()

def remover():
    id_cliente = input("ID do cliente para remover: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cadastro.cliente WHERE id_cliente = %s', (id_cliente,))
    if cur.rowcount == 0:
        print("Cliente não encontrado.")
    else:
        print("Cliente removido com sucesso.")
    conn.commit()
    cur.close()
    conn.close()

def listar_todos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_cliente, nome, telefone, senha, email FROM cadastro.cliente')
    clientes = cur.fetchall()
    if clientes:
        for c in clientes:
            print(f"ID: {c[0]}, Nome: {c[1]}, Telefone: {c[2]}, Senha: {c[3]}, Email: {c[4]}")
    else:
        print("Nenhum cliente cadastrado.")
    cur.close()
    conn.close()

def exibir_um():
    id_cliente = input("ID do cliente: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id_cliente, nome, telefone, senha, email FROM cadastro.cliente WHERE id_cliente = %s', (id_cliente,))
    c = cur.fetchone()
    if c:
        print(f"ID: {c[0]}, Nome: {c[1]}, Telefone: {c[2]}, Senha: {c[3]}, Email: {c[4]}")
    else:
        print("Cliente não encontrado.")
    cur.close()
    conn.close()
