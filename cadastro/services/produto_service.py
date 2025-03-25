import psycopg2
from db import get_connection
from comercial.services.fornecimento_service import FornecimentoService

class ProdutoService:
    def inserir():
        """Cadastra um produto e cria um fornecimento vinculado, caso o usuário deseje."""
        
        nome = input("Nome do Produto: ")
        valor_produto = input("Valor do Produto: ")
        estoque = input("Quantidade em Estoque: ")
        desc_produto = input("Descrição (opcional): ")

        try:
            valor_produto = round(float(valor_produto), 2)
        except ValueError:
            print("Erro: O valor do produto deve ser numérico com até duas casas decimais.")
            return

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                'INSERT INTO cadastro.produto (nome, valor_produto, estoque, desc_produto) VALUES (%s, %s, %s, %s) RETURNING cod_produto',
                (nome, valor_produto, estoque, desc_produto if desc_produto else None)
            )
            cod_produto = cur.fetchone()[0]
            print(f"Produto {nome} cadastrado temporariamente. Código: {cod_produto}")

            adicionar_fornecedor = input("Deseja adicionar um fornecedor para este produto? (s/n): ").lower()

            if adicionar_fornecedor == 's':
                sucesso = FornecimentoService.inserir_fornecimento(cod_produto, cur)
                if not sucesso:
                    raise Exception("Erro ao criar fornecimento. Produto não será cadastrado.")
                print(f"Fornecimento cadastrado com sucesso para o produto {nome}.")
            else:
                print("Fornecedor não adicionado ao produto.")

            conn.commit()
        
        except Exception as e:
            conn.rollback()
            print(f"Erro: {e}")
        
        finally:
            cur.close()
            conn.close()

    def alterar():
        id_produto = input("Código do produto para alterar: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT cod_produto, nome, valor_produto, estoque, desc_produto FROM cadastro.produto WHERE cod_produto = %s', (id_produto,))
        produto = cur.fetchone()

        if not produto:
            print("Produto não encontrado.")
            cur.close()
            conn.close()
            return

        print(f"Produto atual: Código: {produto[0]}, Nome: {produto[1]}, Valor: {produto[2]}, Estoque: {produto[3]}, Descrição: {produto[4]}")

        novo_nome = input(f"Novo nome ({produto[1]}): ") or produto[1]
        novo_valor = input(f"Novo valor ({produto[2]}): ") or produto[2]
        novo_estoque = input(f"Novo estoque ({produto[3]}): ") or produto[3]
        nova_desc = input(f"Nova descrição ({produto[4]}): ") or produto[4]

        cur.execute(
            'UPDATE cadastro.produto SET nome = %s, valor_produto = %s, estoque = %s, desc_produto = %s WHERE cod_produto = %s',
            (novo_nome, novo_valor, novo_estoque, nova_desc, id_produto)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Produto alterado com sucesso!")

    def pesquisar_por_nome():
        nome = input("Nome para pesquisa: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT nome, valor_produto, estoque, desc_produto FROM cadastro.produto WHERE nome ILIKE %s', (f'%{nome}%',))
        produtos = cur.fetchall()
        if produtos:
            for p in produtos:
                print(f"Nome: {p[0]}, Valor: {p[1]}, Estoque: {p[2]}, Descrição: {p[3]}")
        else:
            print("Nenhum produto encontrado.")
        cur.close()
        conn.close()

    def remover():
        try:
            cod_produto = int(input("Código do produto para remover: "))
        except ValueError:
            print("Erro: Código do produto inválido. Deve ser um número inteiro.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM cadastro.produto WHERE cod_produto = %s', (cod_produto,))
            if cur.rowcount == 0:
                print("Produto não encontrado.")
            else:
                conn.commit()
                print("Produto removido com sucesso.")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "foreign key" in str(e).lower():
                print("Erro: Este produto não pode ser removido porque está sendo referenciado em outra tabela.")
            else:
                print(f"Erro ao remover produto: {e}")
        finally:
            cur.close()
            conn.close()

    def listar_todos():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT cod_produto, nome, valor_produto, estoque, desc_produto FROM cadastro.produto')
        produtos = cur.fetchall()
        if produtos:
            for p in produtos:
                print(f"Codigo: {p[0]}, Nome: {p[1]}, Valor: {p[2]}, Estoque: {p[3]}, Descrição: {p[4]}")
        else:
            print("Nenhum produto cadastrado.")
        cur.close()
        conn.close()

    def exibir_um():
        cod_produto = input("Código do produto: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT cod_produto, nome, valor_produto, estoque, desc_produto FROM cadastro.produto WHERE cod_produto = %s', (cod_produto,))
        p = cur.fetchone()
        if p:
            print(f"Código: {p[0]}, Nome: {p[1]}, Valor: {p[2]}, Estoque: {p[3]}, Descrição: {p[4]}")
        else:
            print("Produto não encontrado.")
        cur.close()
        conn.close()