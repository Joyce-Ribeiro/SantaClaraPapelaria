import psycopg2
from db import get_connection

class DistribuidorService:
    def inserir():
        nome = input("Nome do distribuidor: ")
        cnpj = input("CNPJ: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO cadastro.distribuidor (nome, cnpj) VALUES (%s, %s)',
            (nome, cnpj)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Distribuidor cadastrado com sucesso!")

    def alterar():
        id_distribuidor = input("ID do distribuidor para alterar: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_distribuidor, nome, cnpj FROM cadastro.distribuidor WHERE id_distribuidor = %s', (id_distribuidor,))
        distribuidor = cur.fetchone()

        if not distribuidor:
            print("Distribuidor não encontrado.")
            cur.close()
            conn.close()
            return

        print(f"Distribuidor atual: Nome: {distribuidor[1]}, CNPJ: {distribuidor[2]}")

        novo_nome = input(f"Novo nome ({distribuidor[1]}): ") or distribuidor[1]
        novo_cnpj = input(f"Novo CNPJ ({distribuidor[2]}): ") or distribuidor[2]

        cur.execute(
            'UPDATE cadastro.distribuidor SET nome = %s, cnpj = %s WHERE id_distribuidor = %s',
            (novo_nome, novo_cnpj, id_distribuidor)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Distribuidor alterado com sucesso!")

    def pesquisar_por_nome():
        nome = input("Nome para pesquisa: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_distribuidor, nome, cnpj FROM cadastro.distribuidor WHERE nome ILIKE %s', (f'%{nome}%',))
        distribuidores = cur.fetchall()
        if distribuidores:
            for d in distribuidores:
                print(f"ID: {d[0]}, Nome: {d[1]}, CNPJ: {d[2]}")
        else:
            print("Nenhum distribuidor encontrado.")
        cur.close()
        conn.close()

    def remover():
        try:
            id_distribuidor = int(input("Id do distribuidor para remover: "))
        except ValueError:
            print("Erro: Id inválido. Deve ser um número inteiro.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM cadastro.distribuidor WHERE id_distribuidor = %s', (id_distribuidor,))
            if cur.rowcount == 0:
                print("Distribuidor não encontrado.")
            else:
                conn.commit()
                print("Distribuidor removido com sucesso.")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "foreign key" in str(e).lower():
                print("Erro: Este distribuidor não pode ser removido porque está sendo referenciado em outra tabela.")
            else:
                print(f"Erro ao remover distribuidor: {e}")
        finally:
            cur.close()
            conn.close()

    def listar_todos():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_distribuidor, nome, cnpj FROM cadastro.distribuidor')
        distribuidores = cur.fetchall()
        if distribuidores:
            for d in distribuidores:
                print(f"ID: {d[0]}, Nome: {d[1]}, CNPJ: {d[2]}")
        else:
            print("Nenhum distribuidor cadastrado.")
        cur.close()
        conn.close()

    def exibir_um():
        id_distribuidor = input("ID do distribuidor: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_distribuidor, nome, cnpj FROM cadastro.distribuidor WHERE id_distribuidor = %s', (id_distribuidor,))
        d = cur.fetchone()
        if d:
            print(f"ID: {d[0]}, Nome: {d[1]}, CNPJ: {d[2]}")
        else:
            print("Distribuidor não encontrado.")
        cur.close()
        conn.close()
