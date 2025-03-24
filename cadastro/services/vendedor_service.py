from db import get_connection

def inserir():
    matricula = input("Matrícula (8 caracteres): ")
    nome = input("Nome do vendedor: ")
    comissao = input("Comissão (opcional, deixe vazio se não quiser): ")
    senha = input("Senha: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadastro.vendedor (matricula, nome, comissao, senha) VALUES (%s, %s, %s, %s)',
        (matricula, nome, comissao if comissao else None, senha)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Vendedor cadastrado com sucesso!")

def alterar():
    matricula = input("Matrícula do vendedor para alterar: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor WHERE matricula = %s', (matricula,))
    vendedor = cur.fetchone()

    if not vendedor:
        print("Vendedor não encontrado.")
        cur.close()
        conn.close()
        return

    print(f"Vendedor atual: Nome: {vendedor[1]}, Comissão: {vendedor[2]}, Senha: {vendedor[3]}")

    novo_nome = input(f"Novo nome ({vendedor[1]}): ") or vendedor[1]
    nova_comissao = input(f"Nova comissão ({vendedor[2]}): ") or vendedor[2]
    nova_senha = input(f"Nova senha ({vendedor[3]}): ") or vendedor[3]

    cur.execute(
        'UPDATE cadastro.vendedor SET nome = %s, comissao = %s, senha = %s WHERE matricula = %s',
        (novo_nome, nova_comissao if nova_comissao else None, nova_senha, matricula)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Vendedor alterado com sucesso!")

def pesquisar_por_nome():
    nome = input("Nome para pesquisa: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor WHERE nome ILIKE %s', (f'%{nome}%',))
    vendedores = cur.fetchall()
    if vendedores:
        for v in vendedores:
            print(f"Matrícula: {v[0]}, Nome: {v[1]}, Comissão: {v[2]}, Senha: {v[3]}")
    else:
        print("Nenhum vendedor encontrado.")
    cur.close()
    conn.close()

def remover():
    matricula = input("Matrícula do vendedor para remover: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cadastro.vendedor WHERE matricula = %s', (matricula,))
    if cur.rowcount == 0:
        print("Vendedor não encontrado.")
    else:
        print("Vendedor removido com sucesso.")
    conn.commit()
    cur.close()
    conn.close()

def listar_todos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor')
    vendedores = cur.fetchall()
    if vendedores:
        for v in vendedores:
            print(f"Matrícula: {v[0]}, Nome: {v[1]}, Comissão: {v[2]}, Senha: {v[3]}")
    else:
        print("Nenhum vendedor cadastrado.")
    cur.close()
    conn.close()

def exibir_um():
    matricula = input("Matrícula do vendedor: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT matricula, nome, comissao, senha FROM cadastro.vendedor WHERE matricula = %s', (matricula,))
    v = cur.fetchone()
    if v:
        print(f"Matrícula: {v[0]}, Nome: {v[1]}, Comissão: {v[2]}, Senha: {v[3]}")
    else:
        print("Vendedor não encontrado.")
    cur.close()
    conn.close()
