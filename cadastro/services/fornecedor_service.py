import psycopg2
from db import get_connection

class FornecedorService:
    def inserir():
        nome = input("Nome do fornecedor: ")
        cnpj = input("CNPJ: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO cadastro.fornecedor (nome, cnpj) VALUES (%s, %s)',
            (nome, cnpj)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Fornecedor cadastrado com sucesso!")

    def alterar():
        id_fornecedor = input("ID do fornecedor para alterar: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_fornecedor, nome, cnpj FROM cadastro.fornecedor WHERE id_fornecedor = %s', (id_fornecedor,))
        fornecedor = cur.fetchone()

        if not fornecedor:
            print("Fornecedor não encontrado.")
            cur.close()
            conn.close()
            return

        print(f"Fornecedor atual: Nome: {fornecedor[1]}, CNPJ: {fornecedor[2]}")

        novo_nome = input(f"Novo nome ({fornecedor[1]}): ") or fornecedor[1]
        novo_cnpj = input(f"Novo CNPJ ({fornecedor[2]}): ") or fornecedor[2]

        cur.execute(
            'UPDATE cadastro.fornecedor SET nome = %s, cnpj = %s WHERE id_fornecedor = %s',
            (novo_nome, novo_cnpj, id_fornecedor)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Fornecedor alterado com sucesso!")

    def pesquisar_por_id():
        id_fornecedor = input("Id para pesquisa: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_fornecedor, nome, cnpj FROM cadastro.fornecedor WHERE id_fornecedor = %s', (id_fornecedor,))
        fornecedores = cur.fetchall()
        if fornecedores:
            for f in fornecedores:
                print(f"ID: {f[0]}, Nome: {f[1]}, CNPJ: {f[2]}")
        else:
            print("Nenhum fornecedor encontrado.")
        cur.close()
        conn.close()

    def remover():
        try:
            id_fornecedor = int(input("Id do fornecedor para remover: "))
        except ValueError:
            print("Erro: Id inválido. Deve ser um número inteiro.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM cadastro.fornecedor WHERE id_fornecedor = %s', (id_fornecedor,))
            if cur.rowcount == 0:
                print("Fornecedor não encontrado.")
            else:
                conn.commit()
                print("Fornecedor removido com sucesso.")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "foreign key" in str(e).lower():
                print("Erro: Este fornecedor não pode ser removido porque está sendo referenciado em outra tabela.")
            else:
                print(f"Erro ao remover fornecedor: {e}")
        finally:
            cur.close()
            conn.close()
            
    def listar_todos():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_fornecedor, nome, cnpj FROM cadastro.fornecedor")
        fornecedores = cur.fetchall()
        cur.close()
        conn.close()

        if not fornecedores:
            print("Nenhum fornecedor encontrado.")
            return

        for fornecedor in fornecedores:
            print(f"ID: {fornecedor[0]} - Nome: {fornecedor[1]} - CNPJ: {fornecedor[2]}")

    def exibir_um():
        id_fornecedor = input("ID do fornecedor: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_fornecedor, nome, cnpj FROM cadastro.fornecedor WHERE id_fornecedor = %s', (id_fornecedor,))
        f = cur.fetchone()
        if f:
            print(f"ID: {f[0]}, Nome: {f[1]}, CNPJ: {f[2]}")
        else:
            print("Fornecedor não encontrado.")
        cur.close()
        conn.close()
