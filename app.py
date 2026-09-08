# INTERFACE WEB COM FLASK DO SISTEMA NCAS
# ESTE ARQUIVO CRIA A INTERFACE WEB DO NÚCLEO COGNITIVO DA AURORA SIGER
# O NEVAGADOR ENVIA A PERGUNTA PARA O FLASK, O FLASK UTILIZA O IA_GROQ.PY PARA
# CONVERSAR COM O GROQ

# Importando os recursos necessários do Flask
from flask import Flask, render_template, request

# Importando função de envio de prompt
from ia_groq import enviar_prompt_groq

# Importando dados estruturados da colônia
from arquivos import carregar_dados_json

# Criando aplicação Flask
app = Flask(__name__) # __name__ ajuda o Flask a localizar os arquivos do projeto

# Rota Principal que representa a página inicial
# o GET é utilizado para abrir a página
# O POST é utilizado para quando o usuário envia uma pergunta
@app.route("/", methods=["GET", "POST"])
def index():
    # Variáveis inicialmente vazias
    pergunta = ""
    resposta = None
    erro = None 

    dados = carregar_dados_json() # Carregando os dados do NCAS

    if dados is not None: # Cas o JSON funcione, recupera-se os dados da coloônia
        colonia = dados["colonia"] 
    else:
        colonia = {
            "nome": "Aurora Siger",
            "status_geral": "Indisponível"
        }

    # Recebendo pergunta do nevagador
    if request.method == "POST":
        pergunta = request.form.get( # request.form recupera informações enviadas pelo formulário HTML
            "pergunta",
            ""
        ).strip()

        # Evita o envio de uma pergunta vazia
        if pergunta == "":
            erro = "Digite uma pergunta antes de enviar."
        elif len(pergunta) > 2000: # Limitando o tamanho da entra
            erro = "A pergunta deve possuir no máximo 2000 caracteres."
        else:
            # Envia a pergunta para a função que já conversa com A API
            resposta = enviar_prompt_groq(pergunta)

            if resposta is None:
                erro = (
                    "Não foi possível obter uma resposta do Assistente Inteligente."
                )
    # Exibindo o HTML
    return render_template(
        "index.html",
        colonia=colonia,
        pergunta=pergunta,
        resposta=resposta,
        erro=erro
    )

# Execução local
if __name__ == "__main__":
    app.run(debug=True)