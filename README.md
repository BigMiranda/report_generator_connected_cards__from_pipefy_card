# 🔗 Executor de Queries GraphQL do Pipefy com Subtabelas (via Streamlit)

Este projeto permite a execução de **queries GraphQL genéricas** contra a API do Pipefy, com foco em análise de dados estruturados. A aplicação identifica listas aninhadas automaticamente (como `parent_relations.cards`) e trata campos complexos de forma inteligente, exibindo os dados em tabelas interativas e exportáveis em Excel.

Você poderá:

- Substituir campos variáveis da query de forma prática
- Visualizar resultados em tabela principal e subtabelas
- Ver prévias de campos complexos e listas de objetos
- Exportar todos os dados para Excel com múltiplas abas
- Salvar e reutilizar queries nomeadas

---

## 🚀 Como Rodar com Docker Compose

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/pipefy-query-runner.git
cd pipefy-query-runner
```

### 2️⃣ Rodar com Docker Compose
```bash
docker compose up -d
```

### 3️⃣ Acessar no Navegador
```
http://localhost:8501
```

---

## 🛠 Como Rodar Localmente (sem Docker)

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Rodar o Streamlit
```bash
streamlit run app.py
```

---

## 🧾 Requisitos

Para utilizar o projeto, você precisará de um **Access Token (Bearer Token)** do Pipefy.

📌 Gere seu token aqui:  
👉 [https://app.pipefy.com/tokens](https://app.pipefy.com/tokens)

---

## 🧠 Funcionalidades

✅ Inserção e edição de queries GraphQL genéricas  
✅ Suporte a campos variáveis com substituição dinâmica (`$variável$`, `$$multi linha$$`)  
✅ Identificação automática de listas aninhadas, como `parent_relations[*].cards[*]`  
✅ Flattenização de dados com nomes de coluna no padrão `obj_subobj_campo`  
✅ Criação de subtabelas quando o número de colunas excede o limite definido  
✅ Prévia dos objetos complexos diretamente na tabela principal  
✅ Visualização de logs e resposta bruta da API  
✅ Exportação para Excel (.xlsx) com múltiplas abas  
✅ Salvamento e reuso de queries nomeadas

---

## 📂 Estrutura do Projeto

```
pipefy-query-runner/
├── app.py                 # Código principal da aplicação (Streamlit)
├── saved_queries.json     # Armazena queries salvas localmente
├── Dockerfile             # Build da imagem Docker
├── docker-compose.yml     # Orquestração via Docker Compose
├── requirements.txt       # Dependências Python
└── README.md              # Documentação do projeto
```

---

## 📆 Tecnologias Utilizadas

- **Streamlit** – Interface web interativa  
- **GraphQL** – Integração com a API do Pipefy  
- **Pandas** – Manipulação de dados  
- **XlsxWriter** – Exportação para Excel  
- **Docker & Docker Compose** – Execução padronizada e portátil

---

## 📖 Licença

Este projeto é de código aberto.  
Sinta-se à vontade para usar, modificar e contribuir!  
Se precisar de ajuda, abra uma issue. 🚀
