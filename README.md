# phase-05-fiap-ncas# NCAS — Núcleo Cognitivo Aurora Siger

Sistema de apoio à gestão operacional de uma colônia espacial fictícia ("Aurora Siger"), com cadastro de registros e alertas, análise lógica de prioridade e um assistente inteligente integrado à API da Groq (LLM). Possui duas formas de uso: **terminal** (menu interativo) e **web** (interface Flask).

## Funcionalidades

- **Cadastro e consulta de registros** da colônia, salvos em arquivo de texto (`registros_colonia.txt`).
- **Cadastro e consulta de alertas operacionais**, armazenados em `dados_colonia.json`, vinculados aos módulos da colônia (Energia, Suporte à Vida, Comunicações, Habitação, Laboratório, Armazenamento, Segurança, Cultivo e Alimentos).
- **Consulta dos dados gerais da colônia** (status geral e status de cada módulo).
- **Análise lógica de alertas**: aplica e compara uma expressão booleana original com sua versão simplificada para decidir se um alerta é prioritário, com base em três variáveis — alerta aberto, alerta crítico e módulo essencial.
- **Assistente inteligente (IA)** via API da Groq, com três modos de prompt:
  - Zero-shot
  - Few-shot
  - Saída estruturada (JSON)
  - Além de perguntas livres ao assistente.
- **Interface web (Flask)**: página única onde o usuário digita uma pergunta e recebe a resposta do assistente inteligente.
- **Visualização de prompts**: exibe no terminal os prompts construídos (zero-shot, few-shot, estruturado) e um exemplo simulado de saída estruturada.

## Estrutura do projeto

```
.
├── app.py                  # Interface web (Flask)
├── codigo_fonte.py         # Menu principal do sistema (versão terminal)
├── arquivos.py             # Leitura/escrita de registros (.txt) e dados (.json)
├── regras.py               # Regras lógicas booleanas para priorização de alertas
├── prompts.py               # Engenharia de prompts (zero-shot, few-shot, structured output)
├── ia_groq.py               # Integração com a API da Groq (LLM)
├── dados_colonia.json       # Dados estruturados da colônia (módulos e alertas)
├── registros_colonia.txt    # Histórico de registros cadastrados
└── requirements.txt         # Dependências do projeto
```

## Pré-requisitos

- Python 3.10+ (o código usa f-strings com aspas duplas aninhadas, recurso disponível a partir do Python 3.12; em versões anteriores pode ser necessário ajustar essas linhas)
- Conta e chave de API na [Groq](https://console.groq.com/)

## Instalação

1. Clone ou copie os arquivos do projeto.
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto com sua chave da API Groq:
   ```
   GROQ_API_KEY=sua_chave_aqui
   ```

## Como executar

### Versão terminal (menu interativo)

```bash
python codigo_fonte.py
```

Menu principal:
```
1 - Cadastrar Registro da Colônia
2 - Consultar Registros Salvos
3 - Consultar Dados da Colônia
4 - Alertas Operacionais
5 - Assistente Inteligente
6 - Visualizar Prompts
7 - Visualizar Logs (ainda não implementado)
0 - Encerrar Sistema
```

### Versão web (Flask)

```bash
python app.py
```

Acesse `http://127.0.0.1:5000/` no navegador (é necessário ter o template `index.html` configurado, veja observação acima).

## Modelo de IA utilizado

O assistente usa o modelo `openai/gpt-oss-20b` via API da Groq, com um prompt de sistema fixo que instrui o assistente a responder em português brasileiro, com linguagem técnica e objetiva.

## Regra lógica de priorização

O módulo `regras.py` implementa e compara duas expressões booleanas equivalentes para decidir se um alerta é prioritário:

- **Original:** `A AND ((C AND E) OR (C AND NOT E))`
- **Simplificada:** `A AND C`

Onde `A` = alerta aberto, `C` = alerta crítico, `E` = módulo essencial. O sistema executa as duas expressões e verifica se os resultados coincidem, exibindo a decisão final ao usuário.


