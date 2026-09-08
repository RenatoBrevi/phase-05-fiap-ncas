# INTEGRANDO O SISTEMA NCAS COM IA GENERATIVA
# ESTE SERÁ O ARQUIVO RESPONSÁVEL PELA COMUNICAÇÃO ENTRE O
# NÚCLEO COGNITIVO DA AURORA SIGER E A API GROQ

# Bibliotecas
import os
import json 

from dotenv import load_dotenv


# Erros documentados próprios para problema específicos:
from groq import (
    Groq,
    AuthenticationError, # Erro para problema de autenticação
    APIConnectionError, # Erro para problema de conexão
    RateLimitError, # Erro para problema de limite de requisições
    APIStatusError # Erro para resposta da API
)

# Importando os prompts
from prompts import (
    selecionar_alerta,
    criar_prompt_zero_shot,
    criar_prompt_few_shot,
    criar_prompt_saida_estruturada
)

# Carregando variáveis armazenadas no arquivo .env
load_dotenv()

# Modelo que será utilizado pelo sistema NCAS
modelo_groq = "openai/gpt-oss-20b"

# Função que será responsável por criar o cliente do Groq
def criar_cliente_groq():
    api_key = os.getenv("GROQ_API_KEY") # Recuperando API Key armazenada no .env

    # Verificando se a chave realmente foi encontrada.
    if not api_key:
        print("\n[ERRO] - A chave GROQ_API_KEY não foi encontrada.")
        print("[NCAS] - Verifique se o arquivo .env está configurado corretamente.")

        return None
    
    # Criando e retornando o cliente Groq
    cliente = Groq(api_key=api_key)

    return cliente

# Função responsável por enviar o prompt para a LLM através da API do Groq
def enviar_prompt_groq(prompt, formato_json=False):
    cliente = criar_cliente_groq() # Criando cliente

    # Caso não tenha sido possível criar o cliente encerra-se a função
    if cliente is None:
        return None
    
    try:
        # Mensagens que serão enviadas para a LLM
        mensagens = [
            {
                "role": "system",
                "content":
                    "Você é o assistente inteligente do "
                    "Núcleo Cognitivo da Aurora Siger (NCAS). "
                    "Responda sempre em português brasileiro, "
                    "com linguagem objetiva, técnica e profissional."
                    "Em respostas textuais comuns, não utilize HTM, "
                    "tabelas Markdown ou tags como <br>. "
                    "Prefira texto simples, títulos e listas com hífen."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # Saída normal
        if not formato_json:
            resposta = cliente.chat.completions.create(
                model=modelo_groq,
                messages=mensagens,
                temperature=0.3 # Controla a variabilidade da resposta
            )
        else: # Saída json
            resposta = cliente.chat.completions.create(
                model=modelo_groq,
                messages=mensagens,
                response_format={ # Forçando o modelo a produzir objeto JSON válido
                    "type": "json_object"
                },

                temperature=0.2 # Controla a variabilidade da resposta
            )
        # Recuperando apenas o texto da resposta
        return resposta.choices[0].message.content
    
    # Chave inválida ou problema na autenticação
    except AuthenticationError:
        print("\n[ERRO] - Não foi possível autenticar na Groq.")
        print("[NCAS] - Verifique sua GROQ_API_KEY.")

    # Problema na internet ou conexão com o servidor
    except APIConnectionError:
        print("\n[ERRO] - Não foi possível conectar à API Groq.")

    # Quantidade máxima de requisições excedida
    except RateLimitError:
        print("\n[ERRO] - Limite de requisições da Groq atingido.")

    # Outros erros retornados pela API
    except APIStatusError as erro:
        print(f"\n[ERRO] - A API Groq retornou status {erro.status_code}.")

    return None

# Função responsável pelo funcionamento do Assistente Inteligente
def assistente_inteligente(dados):
    while True:
        print("\n" + "=" * 50)
        print("########## ASSISTENTE INTELIGENTE ##########")
        print("=" * 50)

        print("\n1 - Analisar Alerta com Zero-Shot")
        print("2 - Analisar Alerta com Few-Show")
        print("3 - Analisar Alerta com Saída Estruturada")
        print("4 - Fazer uma Pergunta ao NCAS")
        print("0 - Voltar ao Menu Principal")

        opcao = input("\nDigite o número opção desejada: ").strip()

        #Zero-Shot
        if opcao == "1":
            alerta = selecionar_alerta(dados)
            if alerta is not None:
                prompt = criar_prompt_zero_shot(alerta)
                print("\n[NCAS] - Enviando alerta para análise...")
                resposta = enviar_prompt_groq(prompt)
                if resposta is not None:
                    print("\n" + "=" * 60)
                    print("######### RESPOSTA DA IA - ZERO-SHOT ##########")
                    print("=" * 60)
                    print(resposta)
        #Few-Shot
        elif opcao == "2":
            alerta = selecionar_alerta(dados)
            if alerta is not None:
                prompt = criar_prompt_few_shot(alerta)
                print("\n[NCAS] - Enviando alerta para análise...")
                resposta = enviar_prompt_groq(prompt)
                if resposta is not None:
                    print("\n" + "=" * 60)
                    print("########## RESPOSTA DA IA - FEW-SHOT ##########")
                    print("=" * 60)
                    print(resposta)
        # Strctured Output
        elif opcao == "3":
            alerta = selecionar_alerta(dados)
            if alerta is not None:
                prompt = criar_prompt_saida_estruturada(alerta)
                print("\n[NCAS] - Gerando análise estruturada...")
                resposta = enviar_prompt_groq(prompt, formato_json=True)
                if resposta is not None:
                    print("\n" + "=" * 60)
                    print("########## RESPOSTA ESTRUTURADA DA IA ##########")
                    print("=" * 60)

                    try: # Transforma a string JSON em dicionário Python
                        resposta_json = json.loads(resposta)
                        print(
                            json.dumps(
                                resposta_json,
                                ensure_ascii=False,
                                indent=4
                            )
                        )
                    except json.JSONDecodeError:
                        print("[ERRO] - A resposta recebida não pôde ser convertida em JSON.")
        # Pergunta livre para a IA
        elif opcao == "4":
            pergunta = input("\nDigite sua pergunta para o NCAS: ").strip()
            if pergunta == "":
                print("[ERRO] - A pergunta não pode estar vazia.")
            else:
                resposta = enviar_prompt_groq(pergunta)
                if resposta is not None:
                    print("\n" + "=" * 60)
                    print("########## RESPOSTA DO NCAS ##########")
                    print("=" * 60)
                    print(resposta)
        # Sair
        elif opcao == "0":
            break
        else:
            print("\n[ERRO] - Digite apenas uma opção entre 0 e 4.")

        input("\n##### Pressione 'ENTER' para continuar. #####")