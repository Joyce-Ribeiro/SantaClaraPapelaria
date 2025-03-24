from db import get_connection
from datetime import datetime

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
    """Registra um novo fornecimento com validações de fornecedor, distribuidor, produto, data e valor."""
    data = input("Data do fornecimento (YYYY-MM-DD): ")
    valor = input("Valor do fornecimento: ")
    id_distribuidor = input("ID do Distribuidor (ou pressione Enter para ignorar): ")
    cod_produto = input("Código do Produto: ")
    id_fornecedor = input("ID do Fornecedor: ")

    try:
        data_fornecimento = datetime.strptime(data, "%Y-%m-%d").date()
        if data_fornecimento > datetime.today().date():
            print("Erro: A data não pode ser maior que hoje.")
            return
    except ValueError:
        print("Erro: Data inválida.")
        return

    try:
        valor = round(float(valor), 2)
    except ValueError:
        print("Erro: Valor deve ser um número válido com até duas casas decimais.")
        return

    if not verificar_existencia("fornecedor", "id_fornecedor", id_fornecedor):
        print("Erro: Fornecedor não encontrado.")
        return

    if id_distribuidor and not verificar_existencia("distribuidor", "id_distribuidor", id_distribuidor):
        print("Erro: Distribuidor não encontrado.")
        return

    if not verificar_existencia("produto", "cod_produto", cod_produto):
        print("Erro: Produto não encontrado.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO comercial.fornecimento (data, valor, id_distribuidor, cod_produto, id_fornecedor) VALUES (%s, %s, %s, %s, %s) RETURNING id_fornecimento',
        (data, valor, id_distribuidor if id_distribuidor else None, cod_produto, id_fornecedor)
    )
    id_fornecimento = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Fornecimento {id_fornecimento} cadastrado com sucesso!")

def inserir_fornecimento(cod_produto):
    """Solicita dados para registrar um fornecimento logo após o cadastro do produto."""
    data = datetime.today().strftime('%Y-%m-%d')  # Data de hoje
    valor = input(f"Valor do Fornecimento para o Produto {cod_produto}: ")
    id_distribuidor = input("ID do Distribuidor (ou Enter para ignorar): ")
    id_fornecedor = input("ID do Fornecedor: ")

    if not verificar_existencia("fornecedor", "id_fornecedor", id_fornecedor):
        print("Erro: Fornecedor não encontrado.")
        return

    if id_distribuidor and not verificar_existencia("distribuidor", "id_distribuidor", id_distribuidor):
        print("Erro: Distribuidor não encontrado.")
        return

    try:
        valor = round(float(valor), 2)
    except ValueError:
        print("Erro: O valor deve ser numérico com até duas casas decimais.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cadastro.fornecimento (data, valor, id_distribuidor, cod_produto, id_fornecedor) VALUES (%s, %s, %s, %s, %s) RETURNING id_fornecimento',
        (data, valor, id_distribuidor if id_distribuidor else None, cod_produto, id_fornecedor)
    )
    id_fornecimento = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Fornecimento {id_fornecimento} registrado para o produto {cod_produto}.")
