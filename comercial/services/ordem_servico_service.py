from db import get_connection
from santaclara.service.auxiliar_funcao import FuncoesUteis

class OrdemServicoService:
    def inserir():
        """Insere uma nova ordem de serviço, garantindo que pelo menos Cliente ou Vendedor exista."""
        id_cliente = input("ID do Cliente (ou pressione Enter para ignorar): ")
        matricula_vendedor = input("Matrícula do Vendedor (ou pressione Enter para ignorar): ")
        id_pedido = input("ID do Pedido: ")

        if not id_cliente and not matricula_vendedor:
            print("Erro: Deve haver pelo menos um Cliente ou um Vendedor.")
            return

        if id_cliente and not FuncoesUteis.verificar_existencia("cliente", "id_cliente", id_cliente):
            print("Erro: Cliente não encontrado.")
            return

        if matricula_vendedor and not FuncoesUteis.verificar_existencia("vendedor", "matricula", matricula_vendedor):
            print("Erro: Vendedor não encontrado.")
            return

        if not FuncoesUteis.verificar_existencia("pedido", "id_pedido", id_pedido):
            print("Erro: Pedido não encontrado.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO comercial.ordemservico (id_cliente, id_pedido, vendedor_id) VALUES (%s, %s, %s) RETURNING id_ordem',
            (id_cliente if id_cliente else None, id_pedido, matricula_vendedor if matricula_vendedor else None)
        )
        id_ordem = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print(f"Ordem de Serviço {id_ordem} cadastrada com sucesso!")

    def inserir_ordem_servico_vendedor(cur, matricula_vendedor, id_pedido):
        """Insere uma ordem de serviço vinculada a um vendedor."""
        if not FuncoesUteis.verificar_existencia("vendedor", "matricula", matricula_vendedor):
            print("Erro: Vendedor não encontrado.")
            return False

        cur.execute(
            'INSERT INTO comercial.ordem_servico (vendedor_id, pedido_id) VALUES (%s, %s) RETURNING id_ordem',
            (matricula_vendedor, id_pedido)
        )
        id_ordem = cur.fetchone()[0]
        print(f"Ordem de Serviço {id_ordem} cadastrada com sucesso para o vendedor {matricula_vendedor}.")
        return True

    def inserir_ordem_servico_cliente(cur, id_cliente, id_pedido):
        """Insere uma ordem de serviço vinculada a um cliente."""
        if not FuncoesUteis.verificar_existencia("cliente", "id_cliente", id_cliente):
            print("Erro: Cliente não encontrado.")
            return False

        cur.execute(
            'INSERT INTO comercial.ordem_servico (cliente_id, pedido_id) VALUES (%s, %s) RETURNING id_ordem',
            (id_cliente, id_pedido)
        )
        id_ordem = cur.fetchone()[0]
        print(f"Ordem de Serviço {id_ordem} cadastrada com sucesso para o cliente {id_cliente}.")
        return True
