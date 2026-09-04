# Iniciando a base NCAS

# Bibliotecas
import os

# Importando funções
from arquivos import cadastrar_registro, consultar_registros

# Função para limpar a tela no terminal
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear") # cls para limpar no Windows e clear no Linux/macOS

# Exibindo o título principal do sistema.
def exibir_cabecalho():
    print("\n" + "=" * 50)
    print("|||||| NCAS - NÚCLEO COGNITIVO AURORA SIGER ||||||")
    print("=" * 50)

# exibir_cabecalho() # Testando a função

# Exibindo as opções do menu principal.
def exibir_menu():
    print("\n################# MENU PRINCIPAL #################\n")
    print("1 - Cadastrar Registro da Colônia")
    print("2 - Consultar Registros Salvos")
    print("3 - Consultar Dados da Colônia")
    print("4 - Analisar Alerta Operacional")
    print("5 - Assistente Inteligente")
    print("6 - Visualizar Prompts")
    print("7 - Visualizar Logs")
    print("0 - Encerrar Sistema")

# exibir_menu() # Testando a função.

# Função que será responsável por fazer o sistema principal NCAS funcionar.
def executar_sistema():
    while True: # Enquanto for True, o menu continuará rodando.
        limpar_tela() # Sempre que o menu for exibido novamente, será limpado a tela anterior.
        exibir_cabecalho()
        exibir_menu()
        
        # Fazendo input e a estrutura de decisão
        opcao = input("\nDigite a opção desejada: ")

        if opcao == "1":
            cadastrar_registro()
        elif opcao == "2":
            consultar_registros()
        elif opcao == "3":
            print("\nConsulta aos Dados da Colônia")
            print("Será implementado nas próximas etapas")
        elif opcao == "4":
            print("\nAnálise de Alertas")
            print("Será implementado nas próximas etapas")
        elif opcao == "5":
            print("\nAssistente Inteligente")
            print("Será implementado nas próximas etapas")
        elif opcao == "6":
            print("\nVisualização de Prompts")
            print("Será implementado nas próximas etapas")
        elif opcao == "7":
            print("\nVisualização de Logs")
            print("Será implementado nas próximas etapas")
        elif opcao == "0":
            print("\nEncerrando o Sistema do NCAS...")
            print("Sistema encerrado com segurança.\n")
            break # Para que o while pare de rodar
        else:
            print("\n[ERRO]: Opção inválida. Digite apenas uma opção entre 0 a 7.")
        input("\n##### Pressione 'ENTER' para voltar ao MENU. #####")

# Condição que verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    executar_sistema()

