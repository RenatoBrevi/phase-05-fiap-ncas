# Esse arquivo será responsável pelas operações referente aos arquivos de texto
# sendo utilizado como funções dentro do codigo_fonte.py

# Bibliotecas
from datetime import datetime
import json

# Nome do arquivo que armazenará os registros
arquivo_registro = "registros_colonia.txt"

# Nome do arquivo que armazenará os dados estruturados da colônia
arquivo_dados = "dados_colonia.json"

# Função responsável por cadastrar um novo registro da colônia
def cadastrar_registro():
    print("\n" + "=" * 50)
    print("########## CADASTRO DE REGISTRO #########")
    print("=" * 50)

    # Coletando as informações do registro
    modulo = input("\nInforme o módulo da colônia: ")
    tipo = input("Informe o tipo da ocorrência: ")
    
    # Forçando a prioridade para não ser possível outra opção
    while True:
        prioridade = input("Informe a prioridade (Baixa/Média/Alta/Crítica): ").strip().lower()

        if prioridade == "baixa":
            prioridade = "Baixa"
            break
        elif prioridade == "media" or prioridade == "média":
            prioridade = "Média"
            break
        elif prioridade == "alta":
            prioridade = "Alta"
            break 
        elif prioridade == "critica" or prioridade == "crítica":
            prioridade = "Crítica"
            break
        else:
            print("\n[ERRO]: Prioridade inválida")
            print("Digite apenas: Baixa, Média, Alta ou Crítica.\n")

    responsavel = input("Informe o responsável pelo registro: ")
    descricao = input("Descreva a ocorrência: ")

    # Obtendo a data e hora atual do computador
    data_hora_atual = datetime.now()

    # Forçando o formato que será apresentado
    data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S") # day/month/year - hour/minute/second

    # Status do registro
    status = "Aberto"

    # Cada elemento da lista representa uma linha que será gravada posteriormente no arquivo de texto.
    registro = [
        "\n" + "=" * 60 + "\n",
        f"Data e Hora: {data_hora_formatada}\n"
        f"Módulo: {modulo}\n",
        f"Tipo de Ocorrência: {tipo}\n",
        f"Prioridade: {prioridade}\n",
        f"Responsável: {responsavel}\n",
        f"Status: {status}\n",
        f"Descrição: {descricao}\n",
        "=" * 60 + "\n"
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

# Função responsável pelo carregamento dos dados armazenados no arquivo JSON
def carregar_dados_json():
    try:
        with open(arquivo_dados, "r", encoding="utf-8") as arquivo: # Abrindo JSON em modo read
            dados = json.load(arquivo) # Transformando JSON em dicionário e listas em Python

        return dados
     
    except FileNotFoundError:
        print("\n[ERRO] - O arquivo dados_colonia.json não foi encontrado.")
        return None 
    
    except json.JSONDecodeError:
        print("\n[ERRO] - O arquivo JSON possui uma estrutura inválida.")
        return None
    
# Função responsável por salver os dados no arquivo JSON
def salvar_dados_json(dados):
    with open(arquivo_dados, "w", encoding="utf-8") as arquivo: # Abrindo em modo writing
        json.dump( #JSON transforma estrutura do Python em dados no formato JSON e grava no arquivo.
            dados,
            arquivo,
            ensure_ascii=False, # Para não alterar a palavra com símbolos
            indent=4 # Para deixar estruturado com dicionário
        )

# Função responsável por cadastrar um novo alerta operacional dentro do arquivo dados_colonia.json
def cadastrar_alerta():
    print("\n" + "=" * 50)
    print("########## CADASTRO DE ALERTA ##########")
    print("=" * 50)

    dados = carregar_dados_json() # Carregando os dados atuais do arquivo JSON.

    if dados is None: # Caso os dados não retorne algo durante a leitura, a função será encerrada
        return
    
    # Exibindo os módulos disponíveis
    print("\nMódulos da Aurora Siger:\n")

    # Percorrendo os módulos armazenados no JSON
    for modulo in dados["modulos"]:
        print(f"{modulo['id']} - {modulo['nome']}")

    # Escolha e validação do módulo
    while True:
        opcao_modulo = input("\nInforme o número do módulo relacionado ao alerta: ").strip()

        modulo_escolhido = None # Inicialmente o nenhum módulo será encontrado

        # Percorrendo os módulos procurando o ID informado.
        for modulo in dados["modulos"]:
            if opcao_modulo == str(modulo["id"]):
                modulo_escolhido = modulo
                break 

        # Se um módulo válido for encontrado encerra-se o while
        if modulo_escolhido is not None:
            break 

        print("\n[ERRO] - Módulo inválido. Escolha uma opção da lista.")

    # Informações do alerta
    tipo = input("\nInforme o tipo do alerta: ")

    # Validação da prioridade
    while True:
        prioridade = input("Informe a prioridade (Baixa/Média/Alta/Crítica): ").strip().lower()

        if prioridade == "baixa":
            prioridade = "Baixa"
            break
        elif prioridade == "media" or prioridade == "média":
            prioridade = "Média"
            break
        elif prioridade == "alta":
            prioridade = "Alta"
            break 
        elif prioridade == "critica" or prioridade == "crítica":
            prioridade = "Crítica"
            break
        else:
            print("\n[ERRO]: Prioridade inválida")
            print("Digite apenas: Baixa, Média, Alta ou Crítica.\n")
    
    mensagem = input("Descreva o alerta operacional: ")

    # Data e hora
    data_hora_atual = datetime.now() # Obtendo horário automático
    data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")

    # Gerando o ID do laerta
    ultimo_id = 0 # Inicialmente o não existem alertas

    # Percorrendo os alertas já armazenados
    for alerta in dados["alertas"]: # Se o id encontrado for maior que o último conhecido, atualiza
        if alerta["id"] > ultimo_id:
            ultimo_id = alerta["id"]
    
    novo_id = ultimo_id + 1 # Novo alerta recebe o próximo número disponível.

    # Definindo se o alerta é crítico
    critico = prioridade == "Crítica" # Retornará True quando a prioridade for crítica

    status = "Aberto" # Todo alerta novo começa com o status "Aberto"

    # Criando dicionário do alerta
    novo_alerta = {
        "id": novo_id,
        "modulo": modulo_escolhido["nome"],
        "tipo": tipo,
        "prioridade": prioridade,
        "critico": critico,
        "data_hora": data_hora_formatada,
        "mensagem": mensagem,
        "status": status
    }

    # Adicionando o alerta ao JSON
    dados["alertas"].append(novo_alerta)

    salvar_dados_json(dados) # Regravando o arquivo JSON com os dados atualiados

    print("\n[NCAS] - Alerta operacional cadastrado com sucesso.")
    print(f"[NCAS] - ID do alerta: {novo_id}")

# Função responsável por consultar os alertas armazenados no arquivo dados_colonia.json
def consultar_alertas():
    print("\n" + "=" * 50)
    print("########## ALERTAS OPERACIONAIS ##########")
    print("=" * 50)
    
    # Carregando os dados armazenados no arquivo JSON
    dados = carregar_dados_json()

    # Se dados não tiver nada, encerra a função
    if dados is None:
        return
    
    alertas = dados["alertas"] # Recuperando a lsita de alertas do dicionário

    # Verificando se a lista está vazia
    if len(alertas) == 0:
        print("\n[NCAS] - Nenhum alerta operacional foi cadastrado.")
        return
    
    # Percorrendo todos os alertas armazenados.
    for alerta in alertas:
        print("\n" + "=" * 60)
        print(f"ID: {alerta['id']}")
        print(f"Módulo: {alerta['modulo']}")
        print(f"Tipo: {alerta['tipo']}")
        print(f"Prioridade: {alerta['prioridade']}")

        if alerta["critico"]:
            print("Crítico: Sim")
        else:
            print("Crítico: Não")

        print(f"Data e Hora: {alerta['data_hora']}")
        print(f"Status: {alerta['status']}")
        print(f"Mensagem: {alerta['mensagem']}")

        print("=" * 60)