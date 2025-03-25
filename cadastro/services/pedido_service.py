import psycopg2
from db import get_connection
from datetime import datetime
from comercial.services.itens_pedido_service import ItensPedidoService
from comercial.services.ordem_servico_service import OrdemServicoService
from cadastro.services.cliente_service import ClienteService
from cadastro.services.vendedor_service import VendedorService

class PedidoService:
    def inserir():
        data_pedido = datetime.now()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO cadastro.pedido (data_pedido) VALUES (%s) RETURNING id_pedido', (data_pedido,))
        id_pedido = cur.fetchone()[0]
        
        resp = input("Pedido por cliente ou vendedor? [C/V]: ").strip().upper()
        
        if resp == "V":
            VendedorService.listar_todos()
            vendedor = input("ID do vendedor: ")
            sucesso = OrdemServicoService.inserir_ordem_servico_vendedor(cur, vendedor, id_pedido)
        elif resp == "C":
            ClienteService.listar_todos()
            cliente = input("ID do cliente: ")
            sucesso = OrdemServicoService.inserir_ordem_servico_cliente(cur, cliente, id_pedido)
        else:
            print("Opção inválida!")
            return
        
        if sucesso:
            conn.commit()
            print(f"Pedido {id_pedido} cadastrado com sucesso!")
        else:
            conn.rollback()
            print("Erro ao cadastrar ordem de serviço.")
        
        cur.close()
        conn.close()
        
        resposta = input("Adicionar itens ao pedido? [S/N]: ").strip().upper()
        if resposta == 'S':
            ItensPedidoService.inserir_itens_pedido(id_pedido)
        else:
            print("Pedido sem itens adicionados.")

    def alterar():
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
        
        cur.execute('UPDATE cadastro.pedido SET data_pedido = %s WHERE id_pedido = %s', (nova_data_pedido, id_pedido))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Pedido {id_pedido} alterado com sucesso!")

    def pesquisar_por_data():
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
        try:
            id_pedido = int(input("Id do pedido para remover: "))
        except ValueError:
            print("Erro: Id inválido. Deve ser um número inteiro.")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM cadastro.pedido WHERE id_pedido = %s', (id_pedido,))
            if cur.rowcount == 0:
                print("Pedido não encontrado.")
            else:
                conn.commit()
                print("Pedido removido com sucesso.")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "foreign key" in str(e).lower():
                print("Erro: Este pedido não pode ser removido porque está sendo referenciado em outra tabela.")
            else:
                print(f"Erro ao remover pedido: {e}")
        finally:
            cur.close()
            conn.close()

    def listar_todos():
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


    def pesquisar_produtos_por_pedido():
        id_pedido = input("Digite o ID do pedido: ")

        conn = get_connection()
        cur = conn.cursor()
        
        query = """
            SELECT p.cod_produto, p.nome
            FROM comercial.itens_pedido ip
            JOIN cadastro.produto p ON ip.produto_id = p.cod_produto
            WHERE ip.pedido_id = %s
        """
        
        cur.execute(query, (id_pedido,))
        produtos = cur.fetchall()
        
        if produtos:
            print("Produtos do pedido: ")
            for p in produtos:
                print(f"Código: {p[0]}, Nome: {p[1]}")
        else:
            print("Nenhum produto encontrado para esse pedido.")
        
        cur.close()
        conn.close()
