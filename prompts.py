# ENGENHARIA DE PROMPTS
# ESTE ARQUIVO CONTÉM OS PROMPTS UTILIZADOS PELO ASSISTENTE INTELIGENTE DA AURORA SIGER

# Biblioteca
import json

# Função responsável por permitir ao usuário escolher um alerta armazenado
# no arquivo dados_colonia.json
def selecionar_alerta(dados):
    alertas = dados["alertas"] # Recuperando a lista de alertas

    # Verificando se existem alertas cadastrados
    if len(alertas) == 0:
        print("\n[NCAS] - Nenhum alerta disponível.")
        return None
    
    print("\nAlertas Disponíveis:\n")

    # Exibindo versão resumida de cada alerta
    for alerta in alertas:
        print(
            f"ID {alerta['id']} - "
            f"{alerta['modulo']} - "
            f"{alerta['tipo']} - "
            f"{alerta["prioridade"]}"
        )

    # Continua pedindo o ID enquanto o usuário não informar um alerta existente
    while True:
        id_informado = input("\nInforme o ID de alerta: ").strip()

        for alerta in alertas:
            if id_informado == str(alerta["id"]):
                return alerta
            
        print("\n[ERRO] - ID de alerta inválido.")

# ZERO-SHOT PROMPT
def criar_prompt_zero_shot(alerta):
    prompt =f"""
Você é o assistente inteligente do Núcleo Cognitivo da Aurora Siger (NCAS).

Analise o alerta operacional abaixo e determine a gravidade da situação.

Dados do alerta:
ID: {alerta["id"]}
Módulo: {alerta["modulo"]}
Tipo: {alerta["tipo"]}
Prioridade Registrada: {alerta["prioridade"]}
Status: {alerta["status"]}
Mensagem: {alerta["mensagem"]}

Forneça:
- Um resumo da situação;
- A classificação da gravidade;
- Uma ação recomendada para o centro de controle.

Utilize linguagem clara, objetiva e profissional.
"""
    
    return prompt

# FEW-SHOT PROMPT
def criar_prompt_few_shot(alerta):
    prompt = f"""
Você é o assistente inteligente do Núcleo Cognitivo da Aurora Siger (NCAS).

Analise alertas operacionais e forneça uma classificação e uma ação recomendada.

Observe os exemplos:

EXEMPLO 1

Módulo: Laboratório
Tipo: Manutenção
Mensagem: Equipamento de análise necessita recalibração

Respostas:
Classificação: Baixa
Ação recomendada: Programar recalibração do equipamento durante o próximo período de manutenção.

EXEMPLO 2

Módulo: Suporte à Vida
Tipo: Falha de oxigenação
Mensagem: O sistema principal apresentou redução crítica na produção de oxigênio.

Resposta:
Classificação: Crítica
Ação recomendada: Acionar imediatamente o protocolo de emergência e informar o centro de controle.

Agora analise o seguinte alerta:

ID: {alerta["id"]}
Módulo: {alerta["modulo"]}
Tipo: {alerta["tipo"]}
Prioridade Registrada: {alerta["prioridade"]}
Status: {alerta["status"]}
Mensagem: {alerta["mensagem"]}

Forneça: 

Classificação:
Ação recomendada:
"""
    return prompt

# STRUCTURED OUTPUT
def criar_prompt_saida_estruturada(alerta):
    prompt = f"""
Você é o assistente inteligente do Núcleo Cognitivo da Aurora Siger (NCAS).

Analise o alerta operacional abaixo:

ID: {alerta["id"]}
Módulo: {alerta["modulo"]}
Tipo: {alerta["tipo"]}
Prioridade Registrada: {alerta["prioridade"]}
Status: {alerta["status"]}
Mensagem: {alerta["mensagem"]}

Responda exclusivamente utilizando um objeto JSON válido com a seguinte estrutura:

{{
    "id_alerta": {alerta["id"]},
    "modulo": {alerta["modulo"]},
    "classificacao": "Baixa, Média, Alta ou Crítica",
    "resumo": "Resumo objetivo da situação",
    "acao_recomendada": "Ação recomendada ao centro de controle",
    "necessita_intervencao_humana": true ou false
}}

No campo "necessita_intervencao_humana", utilize true ou false de acordo com a
situação analisada.

Não escreva nenhum texto antes ou depois do JSON.
"""
    return prompt

# Função simulada de saída estruturada, para demonstrar o formato de resposta que
# será esperado receber peosteriormente da LLM
def criar_exemplo_saida_estruturada(alerta):
    necessita_intervencao = (
        alerta["prioridade"] == "Alta" or 
        alerta["prioridade"] == "Crítica"
    )

    exemplo_saida = {
        "id_alerta": alerta["id"],
        "modulo": alerta["modulo"],
        "classificacao": alerta["prioridade"],
        "resumo": alerta["mensagem"],
        "acao_recomendada": "Encaminha o alerta ao centro de controle para avaliação operacional.",
        "necessita_intervencao_humana": necessita_intervencao
    }

    return exemplo_saida

# Função responsável por exibir os prompts contruídos pelo NCAS
def visualizar_prompts(dados):
    print("\n" + "=" * 50)
    print("########### ENGENHARIA DE PROMPTS ##########")
    print("=" * 50)

    # O usuário escolhe o alerta real que está no JSON
    alerta = selecionar_alerta(dados)

    # Caso não existam alertas, encerramos a função
    if alerta is None:
        return
    
    # Criando os três prompts
    prompt_zero_shot = criar_prompt_zero_shot(alerta)
    prompt_few_shot = criar_prompt_few_shot(alerta)
    prompt_estruturado = criar_prompt_saida_estruturada(alerta)

    # Criando Exemplo local de resposta estruturada
    exemplo_saida = criar_exemplo_saida_estruturada(alerta)

    # ZERO-SHOT
    print("\n" + "=" * 60)
    print("######### ZERO-SHOT PROMPT ##########")
    print("=" * 60)
    print(prompt_zero_shot)

    # FEW-SHOT
    print("\n" + "=" * 60)
    print("########## FEW-SHOT PROMPT ##########")
    print("=" * 60)
    print(prompt_few_shot)

    # STRUCTURED OUTPUT
    print("\n" + "=" * 60)
    print("########## PROMPT COM STRUCTURED OUTPUT ##########")
    print("=" * 60)
    print(prompt_estruturado)

    # Exemplo de saída
    print("\n" + "=" * 60)
    print("######### EXEMPLO SIMULADO DE STRUCTURED OUTPUT ##########")
    print("=" * 60)

    print(
        json.dumps(
            exemplo_saida,
            ensure_ascii=False,
            indent=4
        )
    )