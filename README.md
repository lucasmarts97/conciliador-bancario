# 📊 Conciliador Bancário

Aplicação em Python/Streamlit que automatiza a conciliação entre o **razão contábil** (extraído em PDF) e o **extrato bancário** (arquivo OFX), identificando automaticamente pendências e lançamentos futuros.

> Projeto desenvolvido para resolver um problema real de rotina financeira: o cruzamento manual entre extrato bancário e razão contábil, que antes era feito lançamento a lançamento em planilha.

## 🎯 O problema

Em uma rotina de conciliação bancária, é comum precisar comparar dezenas (ou centenas) de lançamentos entre dois documentos com formatos completamente diferentes — um PDF de razão contábil e um extrato bancário em OFX — para descobrir:

- Quais lançamentos do razão **ainda não caíram no banco**;
- Quais lançamentos do banco **ainda não foram lançados no razão**;
- Quais desses lançamentos são, na verdade, **datados no futuro** (e portanto não são pendência real).

Esse cruzamento manual é repetitivo e sujeito a erro humano. O Conciliador Bancário automatiza esse processo.

## ✨ Funcionalidades

- 📄 Extração de lançamentos (data, histórico e valor) direto de um PDF de razão contábil, via `pdfplumber`;
- 🏦 Leitura de extratos bancários no padrão OFX, via `ofxparse`;
- 🔎 Motor de conciliação que cruza os dois conjuntos de lançamentos pelo valor;
- 🗓️ Classificação automática das sobras do banco em **"Falta lançar no Razão"** ou **"Lançamento Futuro"**, comparando com a data mais recente do razão;
- 📊 Painel com métricas e tabelas interativas para conferência rápida;
- 🏛️ Seleção de banco (Sicredi, Bradesco, Caixa Econômica) pela barra lateral.

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — interface web
- [Pandas](https://pandas.pydata.org/) — manipulação dos dados
- [pdfplumber](https://github.com/jsvine/pdfplumber) — extração de texto do PDF
- [ofxparse](https://github.com/jseutter/ofxparse) — leitura do extrato OFX

## 📂 Estrutura do projeto

```
conciliador-bancario/
├── app.py                     # Interface Streamlit (camada de apresentação)
├── src/
│   ├── leitores.py            # Leitura/extração dos arquivos PDF e OFX
│   └── motor_conciliacao.py   # Lógica de cruzamento e classificação das pendências
├── iniciar_conciliador.bat    # Atalho Windows: prepara o ambiente e roda o app
├── requirements.txt
└── README.md
```

A lógica foi separada da interface: `leitores.py` cuida apenas da extração dos dados brutos, `motor_conciliacao.py` cuida apenas da regra de negócio do cruzamento, e `app.py` cuida apenas da apresentação. Isso deixa cada parte testável e reutilizável de forma isolada — por exemplo, o motor de conciliação poderia futuramente virar um endpoint de API sem tocar em nenhuma linha da interface.

## ▶️ Como executar localmente

### Opção 1 — Windows, com um clique

Dê duplo clique em `iniciar_conciliador.bat`:

- **Na primeira execução**, o script cria automaticamente um ambiente virtual (`venv`) e instala as dependências do `requirements.txt`.
- **Nas execuções seguintes**, ele apenas ativa o ambiente já existente e abre o app direto no navegador.
- O script detecta sozinho se o Python está disponível como `python` ou pelo launcher `py`.

> **Pré-requisito**: ter o [Python](https://www.python.org/downloads/) instalado com a opção **"Add python.exe to PATH"** marcada durante a instalação. Sem isso, o Windows não encontra o comando `python` e o script avisa com uma mensagem explicando como corrigir.

### Opção 2 — Manual (Windows, Linux ou Mac)

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/conciliador-bancario.git
cd conciliador-bancario

# Crie e ative um ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
streamlit run app.py
```

Em ambos os casos, a aplicação abre no navegador em `http://localhost:8501`. Basta anexar um PDF de razão e um OFX de extrato e clicar em "Processar Conciliação".

## ⚠️ Sobre os dados

Este repositório **não contém nenhum dado real** de extrato bancário ou razão contábil — apenas o código da aplicação. Os arquivos `.pdf` e `.ofx` usados nos testes ficam de fora do controle de versão (veja `.gitignore`), já que contêm informações financeiras sensíveis.

## 🚧 Possíveis evoluções

- Suporte a outros formatos de extrato (CSV, CNAB);
- Exportação dos resultados da conciliação em Excel/PDF;
- Testes automatizados para o motor de conciliação;
- Ajuste fino do parser de PDF para lidar com outros layouts de razão contábil.

## 👤 Autor

**Lucas Martins**
[LinkedIn](https://linkedin.com/in/lucasmarts97)
