# INTERFACE WEB COM FLASK DO SISTEMA NCAS
# ESTE ARQUIVO CRIA A INTERFACE WEB DO NÚCLEO COGNITIVO DA AURORA SIGER
# O NEVAGADOR ENVIA A PERGUNTA PARA O FLASK, O FLASK UTILIZA O IA_GROQ.PY PARA
# CONVERSAR COM O GROQ

import re
import json

# Importando os recursos necessários do Flask
from flask import Flask, render_template, request

# Importando função de envio de prompt
from ia_groq import enviar_prompt_groq

# Importando dados estruturados da colônia
from arquivos import carregar_dados_json

# Importando prompts
from prompts import (
    criar_prompt_zero_shot,
    criar_prompt_few_shot,
    criar_prompt_saida_estruturada
)

# Importando regras
from regras import (
    regra_prioridade_original,
    regra_prioridade_simplificada
)

# Função responsável por limpar caracteres de formatação enviados pela LLM
# antes de exibir a resposta na interface web usando regular expression
def limpar_resposta_ia(texto):
    if not texto: # Caso nenhuma resposta seja recebida
        return texto
    
    # Substituindo tags <br>, <br/> ou <br /> por quebra de linha
    texto = re.sub(
        r"<br\s*/?>",
        "\n",
        texto,
        flags=re.IGNORECASE
    )

    # Remove marcação de negrito do markdown
    texto = texto.replace("**", "")

    # Remove marcação de itálico
    texto = texto.replace("__", "")
    
    # Remove blocos de markdown
    texto = texto.replace("```", "")

    # Remove pipes utilizado em markdown
    texto = texto.replace("|", " ")

    # Remove espaço excessivo no final das linhas
    texto = re.sub(r"[ \t]+\n", "\n", texto)
    
    # Evita mais de duas linhas vazias consecutivas
    texto = re.sub(r"\n{3,}", "\n\n", texto)

    return texto.strip()

# Função para preparar os dados utilizados na interface web
def montar_contexto_web():
    dados = carregar_dados_json()

    # Caso o arquivo não carregue
    if dados is None:
        return {
            "dados": None,
            "colonia": {
                "nome": "Aurora Siger",
                "status_geral": "Indisponível"
            },
            
            "modulos": [],
            "alertas": []
        }
    
    return { # Para não repetir os dados em toda rota
        "dados": dados,
        "colonia": dados["colonia"],
        "modulos": dados["modulos"],
        "alertas": dados["alertas"]
    }

# Criando aplicação Flask
app = Flask(__name__) # __name__ ajuda o Flask a localizar os arquivos do projeto

# Separação de rotas
# Rota página principal
@app.route("/")
def index():
    contexto = montar_contexto_web()

    return render_template(
        "index.html",
        
        colonia=contexto["colonia"],
        modulos=contexto["modulos"],
        alertas=contexto["alertas"],

        pergunta="",
        resposta=None,
        erro=None,

        resultado_alerta=None
    )

# Rota de pergunta livre para LLM
@app.route("/perguntar", methods=["POST"])
def perguntar():
    contexto = montar_contexto_web()

    pergunta = request.form.get(
        "pergunta",
        ""
    ).strip()

    resposta = None
    erro = None

    if pergunta == "":
        erro = "Digite uma pergunta antes de enviar."
    elif len(pergunta) > 2000:
        erro = ("A pergunta deve possuir no máximo 2000 caracteres.")
    else:
        resposta = enviar_prompt_groq(pergunta)

        if resposta is not None:
            resposta = limpar_resposta_ia(resposta) # Função regex/replace
        else:
            erro = ("Não foi possível obter uma respsota do Assistente Inteligente.")

    return render_template(
        "index.html",
        colonia=contexto["colonia"],
        modulos=contexto["modulos"],
        alertas=contexto["alertas"],

        pergunta=pergunta,
        resposta=resposta,
        erro=erro,

        resultado_alerta=None
    )

# Rota analise de alerta
@app.route("/analisar-alerta", methods=["POST"])
def analisar_alerta():
    contexto = montar_contexto_web()
    dados = contexto["dados"]

    # Caso o JSON não esteja disponível
    if dados is None:
        return render_template(
            "index.html",

            colonia=contexto["colonia"],
            modulos=contexto["modulos"],
            alertas=contexto["alertas"],

            pergunta="",
            resposta=None,

            erro="Os dados da colônia não puderam ser carregados.",

            resultado_alerta=None
        )
    
    # Recuperando o ID escohido no formulário HTML
    alerta_id = request.form.get(
        "alerta_id",
        ""
    ).strip()

    # Recuperando qual análise o usuário deseja executar
    acao = request.form.get(
        "acao",
        ""
    ).strip()

    alerta_escolhido = None # Inicialmente nenhum alerta

    # Procurando o alerta pelo ID
    for alerta in dados["alertas"]:
        if alerta_id == str(alerta["id"]):
            alerta_escolhido = alerta
            break

    # Se o ID não for encontrado
    if alerta_escolhido is None:
        return render_template(
            "index.html",
            colonia=contexto["colonia"],
            modulos=contexto["modulos"],
            alertas=contexto["alertas"],

            pergunta="",
            resposta=None,

            erro="Selecione um alerta válido.",

            resultado_alerta=None
        )
    
    resultado_alerta=None
    erro = None

    # ZERO-SHOT
    if acao == "zero":
        prompt = criar_prompt_zero_shot(alerta_escolhido)
        resultado_alerta = enviar_prompt_groq(prompt)

        if resultado_alerta is not None:
            resultado_alerta = limpar_resposta_ia(resultado_alerta)
        else:
            erro = ("Não foi possível executar a análise Zero-Shot.")
    # Few-Shot
    elif acao == "few":
        prompt = criar_prompt_few_shot(alerta_escolhido)
        resultado_alerta = enviar_prompt_groq(prompt)

        if resultado_alerta is not None:
            resultado_alerta = limpar_resposta_ia(resultado_alerta)
        else:
            erro = ("Não foi possível executar a análise Few-Shot.")
    # Structured Output
    elif acao == "structured":
        prompt = criar_prompt_saida_estruturada(alerta_escolhido)
        resposta_json = enviar_prompt_groq(
            prompt,
            formato_json=True
        )

        if resposta_json is not None:
            try:
                resposta_convertida = json.loads(resposta_json) # Converte a resposta em Dict.
                resultado_alerta = json.dumps( # Depois volta para texto JSON formatado para exibição na página
                    resposta_convertida,
                    ensure_ascii=False,
                    indent=4
                )
            except json.JSONDecodeError:
                erro = ("A resposta da IA não pôde ser convertida em JSON.")
        else:
            erro = ("Não foi possível gerar a saída estruturada.")
    # Regra booleana
    elif acao == "regra":
        modulo_escolhido = None

        for modulo in dados["modulos"]:
            if modulo["nome"] == alerta_escolhido["modulo"]:
                modulo_escolhido = modulo
                break 
        if modulo_escolhido is None:
            erro = ("O módulo relacionado ao alerta não foi encontrado.")
        else:
            aberto = (alerta_escolhido["status"].strip().lower() == "aberto")

            critico = alerta_escolhido["critico"]
            essencial = modulo_escolhido["essencial"]

            # Excecutando as regras original e simplificada
            original = regra_prioridade_original(
                aberto,
                critico,
                essencial
            )

            simplificada = regra_prioridade_simplificada(
                aberto,
                critico
            )

            # Transformando os valores booleanos em texto
            aberto_texto = ("Sim" if aberto else "Não")
            critico_texto = ("Sim" if critico else "Não")
            essencial_texto = ("Sim" if essencial else "Não")
            original_texto = ("Verdadeiro" if original else "Falso")
            simplificada_texto = ("Verdadeiro" if simplificada else "Falso")

            if simplificada: 
                decisao = ("O alerta requer atendimento prioritário.")
            else:
                decisao = ("O alerta não atendo aos critérios de prioridade.")

            resultado_alerta = f"""
ANÁLISE LÓGICA DO NCAS

Alerta ID: {alerta_escolhido["id"]}
Módulo: {alerta_escolhido["modulo"]}

VARIÁVEIS

A - Alerta aberto: {aberto_texto}
C - Alerta crítico: {critico_texto}
E - Módulo essencial: {essencial_texto}

EXPRESSÃO ORIGINAL
A AND ((C AND E) OR (C AND NOT E))
Resultado: {original_texto}

EXPRESSÃO SIMPLIFICADA
A AND C
Resultado: {simplificada_texto}

DECISÃO DO NCAS
{decisao}
""".strip()
    else:
        erro = "Tipo de análise inválido."
    
    return render_template(
        "index.html",
        colonia=contexto["colonia"],
        modulos=contexto["modulos"],
        alertas=contexto["alertas"],

        pergunta="",
        resposta=None,
        erro=erro,

        resultado_alerta=resultado_alerta,

        alerta_selecionado=alerta_id
    )

# Execução local
if __name__ == "__main__":
    app.run(debug=True)