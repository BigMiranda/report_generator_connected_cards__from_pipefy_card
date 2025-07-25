# 🔗 Relatório de Cards Conectados no Pipefy (via Streamlit)

Este projeto gera um relatório completo com todos os cards conectados a um card específico no Pipefy, utilizando a API GraphQL.

Você poderá visualizar os dados diretamente no navegador, exportar os resultados em Excel e verificar detalhes como:

- ID e título do card conectado  
- Pipe ao qual pertence (ID e nome)  
- Fase atual (ID e nome)  
- Link direto para o card no Pipefy

---

## 🚀 Como Rodar com Docker Compose

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/pipefy-connected-cards.git
cd pipefy-connected-cards
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

### 3️⃣ Acessar no Navegador
```
http://localhost:8501
```

---

## 🧾 Requisitos

Para utilizar o projeto, você precisará de um **Access Token (Bearer Token)** do Pipefy.

📌 Crie ou gerencie seu token aqui:  
[https://app.pipefy.com/tokens](https://app.pipefy.com/tokens)

---

## 📌 Funcionalidades

✅ Entrada do ID de um card do Pipefy  
✅ Consulta à API GraphQL para buscar todos os cards conectados (via `parent_relations`)  
✅ Retorno em tabela interativa com:
- ID e título do card  
- ID e nome do pipe  
- ID e nome da fase atual  
- Link direto para o card  

✅ Download do relatório em Excel (.xlsx)  
✅ Visualização do log completo da execução e debug da query

---

## 🧱 Estrutura do Projeto

```
pipefy-connected-cards/
│── app.py                 # Código principal em Streamlit
├── saved_queries.json     # Salva queries nomeadas
│── Dockerfile             # Imagem base Python + instalação
│── docker-compose.yml     # Orquestração com Docker Compose
│── requirements.txt       # Bibliotecas necessárias
│── README.md              # Documentação do projeto
```

---

## 📦 Tecnologias Utilizadas

- **Streamlit** – Interface web interativa  
- **GraphQL** – Integração com a API do Pipefy  
- **Pandas** – Manipulação de dados e exportação  
- **XlsxWriter** – Geração de arquivos Excel  
- **Docker & Docker Compose** – Deploy simples e padronizado

---

## 📖 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e contribuir.  
Caso precise de ajuda, abra uma issue no repositório. 🚀
