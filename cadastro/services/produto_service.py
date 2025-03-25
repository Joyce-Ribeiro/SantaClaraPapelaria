from db import get_connection
from comercial.services.fornecimento_service import FornecedorService
from comercial.services.fornecimento_service import FornecimentoService

class ProdutoService:
    @staticmethod
    def inserir():
        """Cadastra um produto e cria um fornecimento vinculado. Se o fornecimento falhar, o produto não será salvo."""
        
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

            sucesso = FornecimentoService.inserir_fornecimento(cod_produto, cur)
            if not sucesso:
                raise Exception("Erro ao criar fornecimento. Produto não será cadastrado.")

            conn.commit()
            print(f"Fornecimento cadastrado com sucesso para o produto {nome}.")
        
        except Exception as e:
            conn.rollback()
            print(f"Erro: {e}")
        
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def alterar():
        id_produto = input("ID do produto para alterar (busca pelo nome exato): ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT nome, valor_produto, estoque, desc_produto FROM cadastro.produto WHERE nome = %s', (id_produto,))
        produto = cur.fetchone()

        if not produto:
            print("Produto não encontrado.")
            cur.close()
            conn.close()
            return

        print(f"Produto atual: Nome: {produto[0]}, Valor: {produto[1]}, Estoque: {produto[2]}, Descrição: {produto[3]}")

        novo_nome = input(f"Novo nome ({produto[0]}): ") or produto[0]
        novo_valor = input(f"Novo valor ({produto[1]}): ") or produto[1]
        novo_estoque = input(f"Novo estoque ({produto[2]}): ") or produto[2]
        nova_desc = input(f"Nova descrição ({produto[3]}): ") or produto[3]

        cur.execute(
            'UPDATE cadastro.produto SET nome = %s, valor_produto = %s, estoque = %s, desc_produto = %s WHERE nome = %s',
            (novo_nome, novo_valor, novo_estoque, nova_desc, id_produto)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Produto alterado com sucesso!")

    @staticmethod
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

    @staticmethod
    def remover():
        nome_produto = input("Nome exato do produto para remover: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM cadastro.produto WHERE nome = %s', (nome_produto,))
        if cur.rowcount == 0:
            print("Produto não encontrado.")
        else:
            print("Produto removido com sucesso.")
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
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

    @staticmethod
    def exibir_um():
        nome_produto = input("Nome exato do produto: ")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT nome, valor_produto, estoque, desc_produto FROM cadastro.produto WHERE nome = %s', (nome_produto,))
        p = cur.fetchone()
        if p:
            print(f"Nome: {p[0]}, Valor: {p[1]}, Estoque: {p[2]}, Descrição: {p[3]}")
        else:
            print("Produto não encontrado.")
        cur.close()
        conn.close()