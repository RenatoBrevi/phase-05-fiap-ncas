# NCAS - REGRAS LÓGICAS
# ARQUIVO RESPONSÁVEL PELAS REGRAS BOOLEANAS UTILIZADAS NO NCAS
# PARA QUE O SISTEMA TOME DECISÕES BASEADAS NOS DADOS ARMAZENADOS

# Função reponsável pela expressão booleana original
# Expressão será:
# P = A AND ((C AND E) OR (C AND NOT E))
# A = alerta aberto
# C = alerta crítico
# E = módulo essencial
def regra_prioridade_original(aberto, critico, essencial):
    return aberto and ((critico and essencial) or (critico and not essencial))

# Função que respresenta a expressão booleana simplificada
# Expressão simplificada:
# P = A AND C
# Bastando verificar se o alerta está "aberto" e se ele é "crítico"
def regra_prioridade_simplificada(aberto, critico):
    return aberto and critico

# Função responsável por aplicar a regra lógica em alerta escolhido pelo usuário
def analisar_alerta_operacional(dados):
    print("\n" + "=" * 70)
    print("########### ANÁLISE LÓGICA DE ALERTA ##########")
    print("=" * 70)

    # Puxando a lista de alertas armazenados
    alertas = dados["alertas"]

    # Verificando se existem alertas cadastrados
    if len(alertas) == 0:
        print("\n[NCAS] - Nenhum alerta disponível para análise.")
        return 
    print("\nAlertas Disponíveis:\n")
    
    # Exibindo lista resumida dos alertas
    for alerta in alertas:
        print(
            f"ID {alerta['id']} - "
            f"{alerta["modulo"]} - "
            f"{alerta['tipo']} - "
            f"{alerta["prioridade"]}"
        )

    # Escolha do alerta
    while True:
        id_informado = input("\nInforme o ID do alerta que deseja analisa: ").strip()

        alerta_escolhido = None # Alerta zerado inicialmente

        # Percorrendo alertas procurando o ID informado
        for alerta in alertas:
            if id_informado == str(alerta['id']):
                alerta_escolhido = alerta 
                break 
        
        # Se encontrado um alerta válido, encerra o loop while
        if alerta_escolhido is not None:
            break

        print("\n[ERRO] - ID de alerta inválido.")

    # Localizando o módulo do alerta
    modulo_escolhido = None

    # Procurando o módulo na lista de módulos para descobrir se é essencial
    for modulo in dados["modulos"]:
        if modulo["nome"] == alerta_escolhido["modulo"]:
            modulo_escolhido = modulo
            break
        
    # Caso o módulo não seja encontrado
    if modulo_escolhido is None:
        print("\n[ERRO] - Módulo relacionado ao alerta não encontrado.")
        return
        
    # Definindo as variáveis booleanas
    # Será True caso o status do alerta for "Aberto"
    aberto = alerta_escolhido["status"].strip().lower() == "aberto"
        
    critico = alerta_escolhido["critico"] # True or False já armazenado

    essencial = modulo_escolhido["essencial"] # True or False já armazenado

    # Excecutando as expressões
    resultado_original = regra_prioridade_original(aberto, critico, essencial)
    resultado_simplificado = regra_prioridade_simplificada(aberto, critico)

    # Exibindo os dados utilizados
    print("\n" + "=" * 70)
    print("########## DADOS UTILIZADOS NA REGRA ##########")
    print("-" * 70)

    print(f"Alerta ID: {alerta_escolhido['id']}")
    print(f"Módulo: {alerta_escolhido['modulo']}")
    print(f"Prioridade Cadastrada: {alerta_escolhido['prioridade']}")
    print(f"Status: {alerta_escolhido['status']}")

    # Convertendo booleanos em Sim/Não para facilitar a visualização
    if critico:
        print("Crítico: Sim")
    else:
        print("Crítico: Não")

    if essencial:
        print("Essencial: Sim")
    else:
        print("Essencial: Não")

    # Exibindo as expressões
    print("\n" + "-" * 70)
    print("########### REGRA BOOLEANA ##########")
    print("-" * 70)

    print(
        "Original: "
        "A AND ((C AND E) OR (C AND NOT E))"
    )

    print(
        "Simplificada: "
        "A AND C"
    )

    # Verificando a equivalência
    print("\nResultado da Expressão Original:", resultado_original)
    print("Resultado da Expressão Simplificada:", resultado_simplificado)

    if resultado_original == resultado_simplificado:
        print("\n[NCAS] - As duas expressões são logicamente equivalentes.")
    else:
        print("\n[ERRO] - As expressões apresentaram resultados diferentes.")

    # Decisão do NCAS
    print("\n" + "-" * 70)
    print("########## DECISÃO DO NCAS ##########")
    print("-" * 70)

    if resultado_simplificado:
        print("[PRIORIDADE] - O alerta requer atendimento prioritário.")
    else:
        print("[NCAS] - O alerta não atende aos critérios de prioridade da regra.")