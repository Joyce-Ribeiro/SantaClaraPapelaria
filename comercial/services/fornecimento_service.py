from db import get_connection
from datetime import datetime
from cadastro.services.distribuidor_service import listar_todos as listar_distribuidores
from cadastro.services.fornecedor_service import listar_todos as listar_fornecedores

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
    produto_id = input("Código do Produto: ")
    fornecedor_id = input("ID do Fornecedor: ")

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

    if not verificar_existencia("fornecedor", "fornecedor_id", fornecedor_id):
        print("Erro: Fornecedor não encontrado.")
        return

    if id_distribuidor and not verificar_existencia("distribuidor", "id_distribuidor", id_distribuidor):
        print("Erro: Distribuidor não encontrado.")
        return

    if not verificar_existencia("produto", "produto_id", produto_id):
        print("Erro: Produto não encontrado.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO comercial.fornecimento (data, valor, distribuidor_id, produto_id, fornecedor_id) VALUES (%s, %s, %s, %s, %s) RETURNING id_fornecimento',
        (data, valor, id_distribuidor if id_distribuidor else None, produto_id, fornecedor_id)
    )
    id_fornecimento = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Fornecimento {id_fornecimento} cadastrado com sucesso!")

def inserir_fornecimento(produto_id):
    """Solicita dados para registrar um fornecimento, listando distribuidores e fornecedores disponíveis."""
    data = datetime.today().strftime('%Y-%m-%d')  # Data de hoje
    valor = input(f"Valor do Fornecimento para o Produto {produto_id}: ")

    # Listar Fornecedores
    print("\nFornecedores disponíveis:")
    listar_fornecedores()

    fornecedor_id = input("Escolha o ID do Fornecedor: ")
    if not verificar_existencia("fornecedor", "id_fornecedor", fornecedor_id):
        print("Erro: Fornecedor não encontrado.")
        return

    # Listar Distribuidores (opcional)
    print("\nDistribuidores disponíveis:")
    listar_distribuidores()

    id_distribuidor = input("Escolha o ID do Distribuidor (ou aperte Enter para ignorar): ")
    
    # Se o distribuidor não foi informado, atribuir None
    if id_distribuidor and not verificar_existencia("distribuidor", "id_distribuidor", id_distribuidor):
        print("Erro: Distribuidor não encontrado.")
        return
    elif not id_distribuidor:
        id_distribuidor = None  # Caso o distribuidor não tenha sido escolhido

    # Validar o valor do fornecimento
    try:
        valor = round(float(valor), 2)
    except ValueError:
        print("Erro: O valor deve ser numérico com até duas casas decimais.")
        return

    # Conectar ao banco de dados e realizar a inserção
    conn = get_connection()
    cur = conn.cursor()

    # Inserir o fornecimento
    cur.execute(
        'INSERT INTO comercial.fornecimento (data, valor, distribuidor_id, produto_id, fornecedor_id) VALUES (%s, %s, %s, %s, %s) RETURNING id_fornecimento',
        (data, valor, id_distribuidor, produto_id, fornecedor_id)
    )
    id_fornecimento = cur.fetchone()[0]  # Recuperar o ID do fornecimento inserido
    conn.commit()
    cur.close()
    conn.close()

    print(f"Fornecimento {id_fornecimento} registrado para o produto {produto_id}.")
