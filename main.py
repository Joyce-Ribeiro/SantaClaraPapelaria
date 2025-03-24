from cadastro.services import (
    vendedor_service,
    produto_service,
    pedido_service,
    cliente_service,
    fornecedor_service,
    distribuidor_service
)

def menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Vendedor")
    print("2. Produto")
    print("3. Pedido")
    print("4. Cliente")
    print("5. Fornecedor")
    print("6. Distribuidor")
    print("7. Sair")

def sub_menu(entidade, service):
    while True:
        print(f"\n--- {entidade.upper()} ---")
        print("1. Inserir")
        print("2. Alterar")
        print("3. Pesquisar por nome")
        print("4. Remover")
        print("5. Listar todos")
        print("6. Exibir um")
        print("7. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            service.inserir()
        elif opcao == '2':
            service.alterar()
        elif opcao == '3':
            service.pesquisar_por_nome()
        elif opcao == '4':
            service.remover()
        elif opcao == '5':
            service.listar_todos()
        elif opcao == '6':
            service.exibir_um()
        elif opcao == '7':
            print(f"Voltando ao menu principal...\n")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            sub_menu("Vendedor", vendedor_service)
        elif opcao == '2':
            sub_menu("Produto", produto_service)
        elif opcao == '3':
            sub_menu("Pedido", pedido_service)
        elif opcao == '4':
            sub_menu("Cliente", cliente_service)
        elif opcao == '5':
            sub_menu("Fornecedor", fornecedor_service)
        elif opcao == '6':
            sub_menu("Distribuidor", distribuidor_service)
        elif opcao == '7':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")
