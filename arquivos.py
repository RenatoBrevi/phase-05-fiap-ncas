# Esse arquivo será responsável pelas operações referente aos arquivos de texto
# sendo utilizado como funções dentro do codigo_fonte.py

# Nome do arquivo que armazenará os registros
arquivo_registro = "registros_colonia.txt"

# Função responsável por cadastrar um novo registro da colônia
def cadastrar_registro():
    print("\n" + "=" * 50)
    print("########## CADASTRO DE REGISTRO #########")
    print("=" * 50)

    # Coletando as informações do registro
    modulo = input("\nInforme o módulo da colônia: ")
    tipo = input("Informe o tipo da ocorrência: ")
    descricao = input("Descreva a ocorrência: ")

    # Cada elemento da lista representa uma linha que será gravada posteriormente no arquivo de texto.
    registro = [
        "\n" + "=" * 50 + "\n",
        f"Módulo: {modulo}\n",
        f"Tipo de Ocorrência: {tipo}\n",
        f"Descrição: {descricao}\n",
        "=" * 50 + "\n"
    ]

    # Abrindo o arquivo em modo append 
    with open(arquivo_registro, "a", encoding="utf-8") as arquivo:
        arquivo.writelines(registro) # Gravando os elementos da lista no arquivo.

    print("\n[NCAS] - Registro cadastrado com sucesso.")

# Função responsável por consultar os registros armazenados
def consultar_registros():
    print("\n" + "=" * 50)
    print("########## REGISTROS DA COLÔNIA ##########")
    print("=" * 50)

    try:
        # Tentando abrir o arquivo no modo read
        with open(arquivo_registro, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines() # recuperando as linhas do arquivo e armazenando o resultadona lista

        # Verificando se o arquivo está vazio
        if len(linhas) == 0:
            print("\n[NCAS] - Nenhum registro foi encontrado.")
        else:
            print()
            # Percorrendo cada linha armazenada na lista
            for linha in linhas:
                print(linha, end="") # end="" para não gerar quebra de linha

    except FileNotFoundError:
        print("\n[NCAS] - Nenhum registro foi cadastrado até o momento.")