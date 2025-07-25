import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import json

st.set_page_config(page_title="Cards Conectados Pipefy", layout="wide")
st.title("🔗 Relatório de Cards Conectados (via parent_relations)")

# Entradas
token = st.text_input("🔐 Token de Acesso (Bearer)", type="password")
card_id = st.text_input("🆔 ID do Card Pipefy")
executar = st.button("🔍 Buscar Cards Conectados")

# Logs
log = []

def gerar_query(card_id):
    return f"""
    {{
      card(id: "{card_id}") {{
        title
        parent_relations {{
          cards {{
            id
            title
            pipe {{
              id
              name
            }}
            current_phase {{
              id
              name
            }}
          }}
        }}
      }}
    }}
    """


if executar:
    if not token or not card_id:
        st.warning("⚠️ Por favor, preencha o Token e o ID do Card.")
    else:
        with st.spinner("🔄 Executando consulta GraphQL..."):
            query = gerar_query(card_id)
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            log.append("📤 Enviando requisição para Pipefy...")
            log.append(f"🔎 Query enviada:\n```graphql\n{query}\n```")

            try:
                response = requests.post(
                    "https://api.pipefy.com/graphql",
                    json={"query": query},
                    headers=headers
                )

                log.append(f"📬 Status da resposta: {response.status_code}")
                if response.status_code != 200:
                    raise Exception(f"Resposta HTTP inválida: {response.status_code}")

                result = response.json()
                log.append(f"📥 Resposta bruta:\n```json\n{json.dumps(result, indent=2)}\n```")

                if "data" not in result or "card" not in result["data"]:
                    raise KeyError("Estrutura da resposta não contém o campo 'data.card'.")

                parent_relations = result["data"]["card"]["parent_relations"]
                dados = []

                for relation in parent_relations:
                    for card in relation.get("cards", []):
                        dados.append({
                        "ID do Card": card["id"],
                        "Título do Card": card["title"],
                        "ID do Pipe": card["pipe"]["id"],
                        "Nome do Pipe": card["pipe"]["name"],
                        "ID da Fase": card["current_phase"]["id"],
                        "Nome da Fase": card["current_phase"]["name"],
                        "Link do Card": f"https://app.pipefy.com/open-cards/{card['id']}"
                    })


                if not dados:
                    st.warning("⚠️ Nenhum card conectado encontrado.")
                else:
                    df = pd.DataFrame(dados)
                    st.success(f"✅ {len(df)} cards conectados encontrados.")
                    st.dataframe(df)

                    # Botão Excel
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df.to_excel(writer, index=False, sheet_name='Cards Conectados')

                    st.download_button("📥 Baixar Excel", data=output.getvalue(),
                                       file_name="cards_conectados.xlsx",
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            except Exception as e:
                st.error("❌ Erro ao processar dados. Verifique o token e o ID do card.")
                log.append(f"❗Erro detectado: {str(e)}")

        # Mostrar log em expander
        with st.expander("📜 Ver Log Completo da Execução"):
            for linha in log:
                st.markdown(linha)
