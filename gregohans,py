import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Análise de Riscos por Localização (Heatmap)")

# === Upload de Arquivo ===
st.sidebar.header("📁 Upload da Planilha")
uploaded_file = st.sidebar.file_uploader("Selecione o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
    else:
        st.success("Arquivo carregado com sucesso!")
        
        # Verificar se colunas necessárias existem
        if "Location" in df.columns and "Risk Area" in df.columns:
            df_filtered = df[["Location", "Risk Area"]].dropna()

            # === Filtro de Location ===
            st.sidebar.header("🎯 Filtro de Localizações")
            all_locations = sorted(df_filtered["Location"].unique())
            selected_locations = st.sidebar.multiselect("Selecione as Location(s):", all_locations, default=all_locations)

            if selected_locations:
                df_sel = df_filtered[df_filtered["Location"].isin(selected_locations)]

                # === Tabela de Frequência ===
                heatmap_data = pd.crosstab(df_sel["Location"], df_sel["Risk Area"])

                # === Heatmap ===
                st.subheader("🔍 Heatmap - Risk Area por Location selecionadas")

                fig, ax = plt.subplots(figsize=(14, 6))
                sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, ax=ax)
                plt.xticks(rotation=45, ha='right')
                plt.yticks(rotation=0)
                st.pyplot(fig)
            else:
                st.warning("Selecione pelo menos uma Location para visualizar o heatmap.")
        else:
            st.error("As colunas 'Location' e/ou 'Risk Area' não foram encontradas na planilha.")
else:
    st.info("Faça o upload de uma planilha para começar.")
