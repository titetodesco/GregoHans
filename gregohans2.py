import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Análise de Segurança Offshore")

# === Upload ===
st.sidebar.header("📁 Upload da Planilha")
uploaded_file = st.sidebar.file_uploader("Selecione um arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
    else:
        st.success("Arquivo carregado com sucesso!")

        # Verifica se colunas principais existem
        required_cols = ['Location', 'Risk Area', 'Event Type', 'RAM Potential', 'Task / Activity', 'Consequences']
        if all(col in df.columns for col in required_cols):
            df_filtered = df[required_cols].dropna()

            # Tabs para separar visualizações
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "🔥 Heatmap por Location",
                "📌 Tipo de Evento",
                "🧯 Severidade (RAM Potential)",
                "🛠️ Tarefas / Atividades",
                "⚠️ Consequências",
                "💥 Severidade vs Risk Area"
            ])

            # === Tab 1: Heatmap Location vs Risk Area ===
            with tab1:
                st.subheader("Heatmap - Risk Area por Location")
                all_locations = sorted(df_filtered["Location"].unique())
                selected_locations = st.multiselect("Filtrar por Location:", all_locations, default=all_locations)

                if selected_locations:
                    df_sel = df_filtered[df_filtered["Location"].isin(selected_locations)]
                    heatmap_data = pd.crosstab(df_sel["Location"], df_sel["Risk Area"])

                    fig, ax = plt.subplots(figsize=(14, 6))
                    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.yticks(rotation=0)
                    st.pyplot(fig)
                else:
                    st.warning("Selecione pelo menos uma Location.")

            # === Tab 2: Tipo de Evento ===
            with tab2:
                st.subheader("Distribuição por Tipo de Evento")
                event_counts = df["Event Type"].value_counts()

                fig, ax = plt.subplots()
                sns.barplot(x=event_counts.values, y=event_counts.index, ax=ax)
                ax.set_xlabel("Número de Eventos")
                ax.set_ylabel("Tipo de Evento")
                st.pyplot(fig)

            # === Tab 3: RAM Potential ===
            with tab3:
                st.subheader("Distribuição por Severidade (RAM Potential)")
                severity_counts = df["RAM Potential"].value_counts()

                fig, ax = plt.subplots()
                ax.pie(severity_counts.values, labels=severity_counts.index, autopct="%1.1f%%", startangle=90)
                ax.axis("equal")
                st.pyplot(fig)

            # === Tab 4: Tarefas / Atividades ===
            with tab4:
                st.subheader("Atividades Mais Registradas")
                task_counts = df["Task / Activity"].value_counts().head(10)

                fig, ax = plt.subplots()
                sns.barplot(x=task_counts.values, y=task_counts.index, ax=ax)
                ax.set_xlabel("Ocorrências")
                ax.set_ylabel("Task / Activity")
                st.pyplot(fig)

            # === Tab 5: Consequências ===
            with tab5:
                st.subheader("Distribuição das Consequências")
                consequence_counts = df["Consequences"].value_counts()

                fig, ax = plt.subplots()
                sns.barplot(x=consequence_counts.values, y=consequence_counts.index, ax=ax)
                ax.set_xlabel("Ocorrências")
                ax.set_ylabel("Consequências")
                st.pyplot(fig)

            # === Tab 6: RAM Potential vs Risk Area ===
            with tab6:
                st.subheader("Correlação entre Severidade (RAM Potential) e Risk Area")

                correlation_data = pd.crosstab(df_filtered['RAM Potential'], df_filtered['Risk Area'])

                if correlation_data.empty:
                    st.warning("Não há dados suficientes para gerar a correlação.")
                else:
                    fig, ax = plt.subplots(figsize=(14, 6))
                    sns.heatmap(correlation_data, annot=True, fmt="d", cmap="Blues", linewidths=0.5, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.yticks(rotation=0)
                    st.pyplot(fig)

        else:
            st.error(f"A planilha deve conter as colunas: {', '.join(required_cols)}")
else:
    st.info("Faça o upload de uma planilha para visualizar os gráficos.")
