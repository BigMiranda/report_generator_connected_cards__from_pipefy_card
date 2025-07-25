import streamlit as st
import requests
import pandas as pd
import json
from io import BytesIO
from pathlib import Path

st.set_page_config(page_title="Pipefy Query Runner", layout="wide")
st.title("📊 Executor de Query GraphQL (Pipefy) com Suporte a Sublistas")

QUERIES_FILE = Path("saved_queries.json")

# Carrega queries salvas
if QUERIES_FILE.exists():
    with open(QUERIES_FILE, "r", encoding="utf-8") as f:
        saved_queries = json.load(f)
else:
    saved_queries = {}

# Entradas
token = st.text_input("🔐 Token de Acesso (Bearer)", type="password")
query_names = list(saved_queries.keys())
selected_query = st.selectbox("📂 Escolher uma query salva", [""] + query_names)
query_text = st.text_area("✍️ Insira ou edite sua query GraphQL abaixo", value=saved_queries.get(selected_query, ""), height=300)

# Salvar nova query
with st.expander("💾 Salvar esta query"):
    new_name = st.text_input("Nome para salvar a query")
    if st.button("Salvar query"):
        if new_name:
            saved_queries[new_name] = query_text
            with open(QUERIES_FILE, "w", encoding="utf-8") as f:
                json.dump(saved_queries, f, indent=2, ensure_ascii=False)
            st.success(f"Query '{new_name}' salva!")
        else:
            st.warning("⚠️ Informe um nome válido.")

# Flatten recursivo com prefixo
def flatten_record(record, parent_key='', sep='_'):
    items = {}
    for k, v in record.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_record(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

# Função especial para extrair listas de subitens (ex: parent_relations[*].cards[*])
def extract_nested_lists(obj, key_chain=None):
    key_chain = key_chain or []
    collected = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, list):
                for idx, item in enumerate(v):
                    if isinstance(item, dict) and "cards" in item and isinstance(item["cards"], list):
                        collected.extend(item["cards"])
            else:
                collected.extend(extract_nested_lists(v, key_chain + [k]))

    elif isinstance(obj, list):
        for item in obj:
            collected.extend(extract_nested_lists(item, key_chain))

    return collected

# Executar a query
if st.button("▶️ Executar Query"):
    if not token or not query_text.strip():
        st.warning("⚠️ Token e query são obrigatórios.")
    else:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            with st.spinner("🔄 Executando query..."):
                response = requests.post("https://api.pipefy.com/graphql", json={"query": query_text}, headers=headers)
                response.raise_for_status()
                result = response.json()

            st.success("✅ Query executada com sucesso.")

            st.subheader("📥 Resposta bruta")
            st.json(result)

            with st.expander("🔍 Logs de Execução"):
                st.write("🔎 Buscando listas aninhadas (ex: parent_relations[*].cards[*])...")
                nested_list = extract_nested_lists(result.get("data", {}))

                if nested_list:
                    st.write(f"✅ Lista extraída com sucesso: {len(nested_list)} registros encontrados.")
                    st.write("🧾 Preview do primeiro item:")
                    st.json(nested_list[0])
                else:
                    st.warning("❌ Nenhuma sublista encontrada com chave 'cards'.")
                    st.stop()

            # Aplicar flatten
            flattened = [flatten_record(r) for r in nested_list]
            df = pd.DataFrame(flattened)
            st.subheader("📊 Tabela Final (flatten)")
            st.dataframe(df)

            # Exportar Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Resultado")

            st.download_button(
                label="📤 Baixar resultado em Excel",
                data=output.getvalue(),
                file_name="resultado_pipefy.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error("❌ Erro ao executar a query.")
            st.exception(e)
