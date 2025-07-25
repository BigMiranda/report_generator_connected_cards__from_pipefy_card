# 📄 Contexto do Projeto: Executor de Query GraphQL (Pipefy)

Este documento registra todas as funcionalidades, decisões de design e comportamentos esperados do projeto até o momento, para garantir integridade contra modificações indevidas ou regressivas.

---

## 📌 Objetivo
Criar uma aplicação web em Streamlit que permita a execução de queries GraphQL genéricas contra a API do Pipefy, exibindo os dados retornados em forma de tabela e permitindo exportação para Excel.

---

## 🧠 Funcionalidades

### ✅ Entrada de Query Genérica
- O usuário pode colar e editar livremente uma query GraphQL válida.
- A query deve ser executada contra o endpoint `https://api.pipefy.com/graphql` com autenticação via Bearer Token.

### ✅ Identificação Inteligente dos Dados
- O sistema identifica automaticamente **listas de objetos aninhadas**, especialmente o padrão `parent_relations[*].cards[*]`.
- Os objetos extraídos são **flattenizados** recursivamente, com colunas nomeadas no padrão: `obj_subobj_propriedade`.
- Campos ausentes ou vazios (`{}`, `[]`) são tratados como `NaN` ou células vazias.

### ✅ Tratamento de Listas Internas (Nova)
- Quando um campo do registro é uma lista de objetos:
  - Se a expansão da lista geraria até um limite de `N` colunas (padrão = 6), o sistema expande normalmente os campos em colunas individuais.
  - Se a expansão da lista ultrapassa esse limite, uma **subtabela** é criada para aquele campo.
    - Cada linha da subtabela recebe um identificador único e referência ao item pai.
    - A tabela principal mostra:
      - Uma coluna com os **IDs das linhas da subtabela** correspondentes
      - Uma segunda coluna com uma **prévia textual** do primeiro campo útil da sublista
  - O limite de colunas (`N`) é configurável via interface antes de executar a query.

### ✅ Visualização e Exportação
- Os dados retornados são exibidos como tabela via `st.dataframe()`.
- Subtabelas também são renderizadas com título e interatividade.
- O Excel gerado contém todas as tabelas (principal + subtabelas) em abas separadas.

### ✅ Salvamento de Queries
- O usuário pode salvar queries nomeadas em um arquivo local `saved_queries.json`.
- Queries salvas são listadas automaticamente para reutilização via dropdown.

### ✅ Logs e Debug
- A aplicação exibe:
  - A resposta bruta da API Pipefy (`st.json()`)
  - O caminho até a lista encontrada (ex: `data.card.parent_relations.cards`)
  - Preview do primeiro item da lista
  - Número de registros processados

---

## 🔐 Requisitos
- A API do Pipefy **requer um Bearer Token** para autenticação.
- O token deve ser inserido pelo usuário no campo indicado.

---

## 📦 Tecnologias Utilizadas
- Python 3.9+
- Streamlit
- Pandas
- Requests
- XlsxWriter

---

## 📂 Estrutura de Arquivos
```
pipefy-query-runner/
├── app.py                   # Código principal do aplicativo Streamlit
├── saved_queries.json       # Armazena queries nomeadas salvas pelo usuário
├── requirements.txt         # Dependências Python
├── Dockerfile               # (Opcional) Imagem Docker do projeto
├── docker-compose.yml       # (Opcional) Orquestração do Docker
├── README.md                # Documentação do projeto
```

---

## ⚠️ Diretrizes para Modificações Futuras
- Toda modificação no comportamento de leitura de dados deve preservar:
  - O padrão de flattenização de colunas
  - A leitura de listas aninhadas (`parent_relations[*].cards[*]`)
  - A compatibilidade com o formato atual de exportação
  - A lógica de criação de subtabelas para campos que excedem o limite configurável de colunas
- Qualquer alteração que modifique o parser de JSON deve manter os logs e estrutura de debug para validação dos dados.

---

## 📌 Versão Atual
**Stable v1.2.0 - Julho/2025**
- Suporte a sublistas internas com criação de subtabelas quando necessário
- Parâmetro configurável para limite de colunas antes de criar subtabela (padrão: 6)
- Flatten adaptativo robusto e exportação com múltiplas abas

---

## 🧾 Exemplo de Query Compatível
```graphql
{
  card(id: "123456") {
    parent_relations {
      cards {
        id
        title
        pipe {
          id
          name
        }
        current_phase {
          id
          name
        }
        assignees {
          id
          name
        }
      }
    }
  }
}
```

---

Este documento deve acompanhar o projeto para servir como base de verificação, validação e integridade do propósito original.
