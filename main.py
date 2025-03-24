from cadastro.services import (
    vendedor_service, 
    produto_service, 
    pedido_service, 
    cliente_service, 
    fornecedor_service, 
    distribuidor_service
)

def menu():
    print("\n==== MENU PRINCIPAL ====")
    print("1. Gerenciar Vendedores")
    print("2. Gerenciar Produtos")
    print("3. Gerenciar Pedidos")
    print("4. Gerenciar Clientes")
    print("5. Gerenciar Fornecedores")
    print("6. Gerenciar Distribuidores")
    print("0. Sair")

def submenu(entidade):
    print(f"\n==== {entidade.upper()} ====")
    print("1. Inserir")
    print("2. Alterar")
    print("3. Pesquisar por Nome")
    print("4. Remover")
    print("5. Listar Todos")
    print("6. Exibir Um")
    print("0. Voltar")

def executar_opcao(opcao, service):
    if opcao == "1":
        service.inserir()
    elif opcao == "2":
        service.alterar()
    elif opcao == "3":
        service.pesquisar_por_nome()
    elif opcao == "4":
        service.remover()
    elif opcao == "5":
        service.listar_todos()
    elif opcao == "6":
        service.exibir_um()
    elif opcao == "0":
        return
    else:
        print("Opção inválida!")

def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            while True:
                submenu("Vendedores")
                escolha = input("Escolha uma opção: ")
                executar_opcao(escolha, vendedor_service)
                if escolha == "0":
                    break
        
        elif opcao == "2":
            while True:
                submenu("Produtos")
                escolha = input("Escolha uma opção: ")
                if escolha == "1":  # Cadastro especial para Produto
                    produto_service.inserir()
                else:
                    executar_opcao(escolha, produto_service)
                if escolha == "0":
                    break
        
        elif opcao == "3":
            while True:
                print("\n==== PEDIDOS ====")
                print("1. Criar Pedido")
                print("2. Listar Pedidos")
                print("0. Voltar")
                escolha = input("Escolha uma opção: ")

                if escolha == "1":
                    pedido_service.inserir()
                elif escolha == "2":
                    pedido_service.listar_todos()
                elif escolha == "0":
                    break
                else:
                    print("Opção inválida!")

        elif opcao == "4":
            while True:
                submenu("Clientes")
                escolha = input("Escolha uma opção: ")
                executar_opcao(escolha, cliente_service)
                if escolha == "0":
                    break

        elif opcao == "5":
            while True:
                submenu("Fornecedores")
                escolha = input("Escolha uma opção: ")
                executar_opcao(escolha, fornecedor_service)
                if escolha == "0":
                    break
        
        elif opcao == "6":
            while True:
                submenu("Distribuidores")
                escolha = input("Escolha uma opção: ")
                executar_opcao(escolha, distribuidor_service)
                if escolha == "0":
                    break

        elif opcao == "0":
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
