# NCAS — Núcleo Cognitivo da Aurora Siger

Projeto desenvolvido para a **Atividade Integradora da Fase 05**, com o objetivo de criar um protótipo capaz de **registrar, organizar, consultar e interpretar informações operacionais da colônia Aurora Siger**.

O sistema combina recursos de Python, arquivos texto, arquivos JSON, lógica booleana, engenharia de prompts, integração com IA generativa via Groq e uma interface web construída com Flask.

---

## Objetivo do projeto

O NCAS foi desenvolvido para representar um núcleo cognitivo responsável por centralizar informações operacionais da colônia Aurora Siger.

Atualmente, o sistema permite:

- Cadastrar registros operacionais em arquivo texto;
- Consultar registros já armazenados;
- Ler e gravar dados estruturados em JSON;
- Consultar os módulos da colônia;
- Cadastrar alertas operacionais;
- Consultar alertas cadastrados;
- Analisar alertas utilizando regras booleanas;
- Demonstrar simplificação de expressões lógicas;
- Visualizar prompts Zero-shot, Few-shot e Structured Output;
- Utilizar uma LLM real através da API Groq;
- Fazer perguntas livres ao Assistente Inteligente;
- Executar o NCAS através de um menu no terminal;
- Executar parte das funcionalidades através de uma interface web com Flask.

---

## Tecnologias utilizadas

- Python
- JSON
- Arquivos texto (`.txt`)
- Flask
- HTML
- CSS
- Groq API
- `python-dotenv`
- Prompt Engineering

---

## Estrutura atual do projeto

```text
NCAS/
│
├── codigo_fonte.py
├── arquivos.py
├── regras.py
├── prompts.py
├── ia_groq.py
├── app.py
│
├── dados_colonia.json
├── registros_colonia.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── requirements.txt
│
├── .env
├── .gitignore
│
└── teste_groq.py
```

### Arquivos principais

#### `codigo_fonte.py`

Arquivo principal da versão em terminal do NCAS.

Contém:

- Menu principal;
- Navegação entre funcionalidades;
- Cadastro e consulta de registros;
- Consulta de dados da colônia;
- Submenu de alertas;
- Integração com regras booleanas;
- Assistente Inteligente;
- Visualização dos prompts.

A opção **Visualizar Logs** ainda está reservada para implementação futura.

---

#### `arquivos.py`

Responsável pelas operações de leitura e escrita de arquivos.

Entre as funcionalidades implementadas estão:

- Cadastro de registros em `registros_colonia.txt`;
- Consulta dos registros;
- Leitura de `dados_colonia.json`;
- Escrita de `dados_colonia.json`;
- Consulta dos dados da colônia;
- Cadastro de alertas;
- Consulta de alertas.

O arquivo utiliza recursos estudados na Fase 05, como:

```python
open()
with
readlines()
writelines()
json.load()
json.dump()
```

Também são utilizados os modos de abertura:

```text
a
r
w
```

---

#### `dados_colonia.json`

Arquivo responsável pelo armazenamento estruturado das informações da Aurora Siger.

Atualmente contém:

- Dados gerais da colônia;
- 8 módulos;
- 12 alertas operacionais;
- Lista de solicitações;
- Lista de interações.

A estrutura principal é:

```json
{
    "colonia": [],
    "modulos": [],
    "alertas": [],
    "solicitacoes": [],
    "interacoes": []
}
```

Os módulos atuais são:

1. Energia
2. Suporte à Vida
3. Comunicações
4. Habitação
5. Laboratório
6. Armazenamento
7. Segurança
8. Cultivo e Alimentos

Cada módulo possui informações como:

- ID;
- Nome;
- Status;
- Indicação se é essencial ou não.

Os alertas possuem dados como:

- ID;
- Módulo;
- Tipo;
- Prioridade;
- Indicação de criticidade;
- Data e hora;
- Mensagem;
- Status.

---

#### `registros_colonia.txt`

Arquivo de texto utilizado para manter registros sequenciais das ocorrências da colônia.

Os registros atuais podem conter:

- Data e hora;
- Módulo;
- Tipo da ocorrência;
- Prioridade;
- Responsável;
- Status;
- Descrição.

O arquivo é aberto no modo `append`, permitindo adicionar novos registros sem apagar os anteriores.

Isso demonstra a persistência das informações mesmo após o encerramento do programa.

---

## Regra lógica do NCAS

O projeto possui uma regra booleana utilizada para definir se um alerta deve receber atendimento prioritário.

### Variáveis

```text
A = alerta está aberto
C = alerta é crítico
E = módulo é essencial
```

### Expressão original

```text
P = A AND ((C AND E) OR (C AND NOT E))
```

### Simplificação

Colocando `C` em evidência:

```text
P = A AND (C AND (E OR NOT E))
```

Pelo Teorema do Complemento:

```text
E OR NOT E = 1
```

Então:

```text
P = A AND (C AND 1)
```

Pelo Teorema da Identidade:

```text
C AND 1 = C
```

Logo:

```text
P = A AND C
```

### Expressão simplificada

```text
P = A AND C
```

Portanto, no NCAS, um alerta recebe prioridade quando está **aberto** e é **crítico**.

As duas expressões são implementadas em `regras.py`.

---

## Engenharia de Prompts

O arquivo `prompts.py` contém os três tipos de prompt exigidos pelo projeto.

### Zero-shot

O modelo recebe:

- Instrução;
- Dados do alerta;
- Tarefa a executar.

Nenhum exemplo é fornecido anteriormente.

### Few-shot

O modelo recebe exemplos de classificação antes de analisar o alerta atual.

Os exemplos ajudam a orientar o padrão esperado da resposta sem alterar os pesos da LLM.

### Structured Output

O modelo é instruído a responder utilizando uma estrutura JSON.

Exemplo de formato esperado:

```json
{
    "id_alerta": 1,
    "modulo": "Energia",
    "classificacao": "Alta",
    "resumo": "Resumo objetivo da situação",
    "acao_recomendada": "Ação recomendada ao centro de controle",
    "necessita_intervencao_humana": true
}
```

---

## Integração com a Groq

A integração com IA generativa é realizada em:

```text
ia_groq.py
```

O modelo atualmente utilizado é:

```text
openai/gpt-oss-20b
```

O sistema permite:

- Analisar alertas com Zero-shot;
- Analisar alertas com Few-shot;
- Gerar Structured Output;
- Fazer perguntas livres ao NCAS.

Também há tratamento para erros relacionados a:

- Autenticação;
- Conexão;
- Limite de requisições;
- Erros retornados pela API.

---

## Segurança da API

A chave da Groq **não deve ser escrita diretamente no código**.

Ela deve ficar em:

```text
.env
```

Exemplo:

```env
GROQ_API_KEY=sua_chave_aqui
```

O `.env` deve permanecer ignorado pelo Git através do `.gitignore`.

Nunca publique sua chave da Groq no GitHub.

---

## Instalação

### 1. Clonar ou baixar o projeto

Entre na pasta do projeto:

```bash
cd https://github.com/RenatoBrevi/phase-05-fiap-ncas.git
```

### 2. Criar um ambiente virtual

No macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

O `requirements.txt` atual contém:

```text
groq
python-dotenv
flask
```

### 4. Configurar a API

Crie o arquivo:

```text
.env
```

E adicione:

```env
GROQ_API_KEY=sua_chave_da_groq
```

Crie sua API aqui: https://console.groq.com/home
---

## Executando o NCAS pelo terminal

Execute:

```bash
python3 codigo_fonte.py
```

O menu principal atual apresenta:

```text
1 - Cadastrar Registro da Colônia
2 - Consultar Registros Salvos
3 - Consultar Dados da Colônia
4 - Alertas Operacionais
5 - Assistente Inteligente
6 - Visualizar Prompts
7 - Visualizar Logs
0 - Encerrar Sistema
```

---

## Executando o NCAS com Flask

Execute:

```bash
python3 app.py
```

Durante o desenvolvimento local, o Flask será iniciado normalmente em:

```text
http://127.0.0.1:5000
```

Abra esse endereço no navegador.

> A execução atual utiliza o servidor de desenvolvimento do Flask e ainda não representa uma implantação pública de produção.

---

## Interface Web

A interface web utiliza:

```text
templates/index.html
static/style.css
```

O visual foi construído com aparência semelhante a um terminal operacional.

Atualmente a interface mostra:

- Nome da Aurora Siger;
- Status geral;
- Status do Assistente Inteligente;
- 8 módulos da colônia;
- Alertas operacionais;
- Área de análise de alerta;
- Área de pergunta livre ao NCAS.

Na análise de alertas estão disponíveis:

```text
ZERO-SHOT
FEW-SHOT
STRUCTURED OUTPUT
REGRA BOOLEANA
```

As três primeiras opções utilizam a API Groq.

A regra booleana é executada localmente em Python.

---

## Rotas Flask atuais

### `/`

Página principal do NCAS.

### `/perguntar`

Recebe perguntas livres enviadas pela interface e encaminha para a Groq.

### `/analisar-alerta`

Recebe:

- ID do alerta;
- Tipo de análise escolhida.

Pode executar:

- Zero-shot;
- Few-shot;
- Structured Output;
- Regra booleana.

---

## Tratamento das respostas da IA

O Flask possui uma função de limpeza das respostas textuais antes da exibição.

Ela utiliza `regex` e `replace()` para tratar elementos como:

```text
<br>
**
__
```

e alguns elementos de Markdown.

O Structured Output não utiliza essa limpeza, pois a resposta precisa permanecer em formato JSON válido.

---

## Persistência de dados

O NCAS demonstra persistência através de dois formatos.

### TXT

```text
registros_colonia.txt
```

Utilizado para registros sequenciais e legíveis.

### JSON

```text
dados_colonia.json
```

Utilizado para informações estruturadas que precisam ser recuperadas por chaves e atributos.

Fluxo simplificado:

```text
Usuário
   ↓
Python
   ↓
Memória
   ↓
Leitura / processamento
   ↓
TXT ou JSON
   ↓
Armazenamento persistente
```

---

## Estado atual do desenvolvimento

Funcionalidades implementadas:

- [x] Menu no terminal
- [x] Cadastro de registros TXT
- [x] Consulta de registros TXT
- [x] Persistência em arquivo texto
- [x] Leitura JSON
- [x] Escrita JSON
- [x] Consulta dos módulos
- [x] Cadastro de alertas
- [x] Consulta de alertas
- [x] Regra booleana
- [x] Simplificação lógica
- [x] Zero-shot Prompting
- [x] Few-shot Prompting
- [x] Structured Output
- [x] Integração com Groq
- [x] Pergunta livre à LLM
- [x] Flask
- [x] Interface HTML/CSS
- [x] Visualização de módulos na web
- [x] Visualização de alertas na web
- [x] Análise de alertas pela web
- [ ] Visualização de logs
- [ ] Utilização das listas `solicitacoes` e `interacoes`
- [ ] Preparação para produção pública
- [ ] Limitação de requisições e proteção contra abuso
- [ ] Hospedagem pública

---

O vídeo de apresentação demonstrará o funcionamento real do NCAS.

---

## Projeto acadêmico

**NCAS — Núcleo Cognitivo da Aurora Siger**

Atividade Integradora — Fase 05

Projeto desenvolvido com finalidade acadêmica para demonstrar integração entre persistência de dados, lógica computacional e inteligência artificial generativa.