import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "🔥 Heatmap por Location",
                "📌 Tipo de Evento",
                "🧯 Severidade (RAM Potential)",
                "🛠️ Tarefas / Atividades",
                "⚠️ Consequências",
                "💥 Severidade vs Risk Area",
                "🎯 Análise Interativa"
            ])

            # === Tab 1: Heatmap Location vs Risk Area ===
            with tab1:
                st.subheader("Heatmap - Risk Area por Location (Interativo)")
                all_locations = sorted(df_filtered["Location"].unique())
                selected_locations = st.multiselect("Filtrar por Location:", all_locations, default=all_locations)

                if selected_locations:
                    df_sel = df_filtered[df_filtered["Location"].isin(selected_locations)]
                    heatmap_data = pd.crosstab(df_sel["Location"], df_sel["Risk Area"])

                    fig = px.imshow(heatmap_data, 
                                    labels=dict(x="Risk Area", y="Location", color="Ocorrências"),
                                    x=heatmap_data.columns,
                                    y=heatmap_data.index,
                                    color_continuous_scale="YlOrRd",
                                    text_auto=True,
                                    aspect="auto")
                    fig.update_xaxes(side="bottom")
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Selecione pelo menos uma Location.")

            # === Tab 2: Tipo de Evento ===
            with tab2:
                st.subheader("Distribuição por Tipo de Evento (Interativo)")
                event_counts = df["Event Type"].value_counts().reset_index()
                event_counts.columns = ['Tipo de Evento', 'Contagem']

                fig = px.bar(event_counts, 
                            x='Contagem', 
                            y='Tipo de Evento',
                            orientation='h',
                            color='Contagem',
                            color_continuous_scale='Blues',
                            text='Contagem')
                fig.update_traces(textposition='outside')
                fig.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig, use_container_width=True)

            # === Tab 3: RAM Potential ===
            with tab3:
                st.subheader("Distribuição por Severidade (RAM Potential) - Interativo")
                severity_counts = df["RAM Potential"].value_counts().reset_index()
                severity_counts.columns = ['RAM Potential', 'Contagem']

                col1, col2 = st.columns(2)
                with col1:
                    fig = px.pie(severity_counts, 
                                values='Contagem', 
                                names='RAM Potential',
                                title='Distribuição de Severidade',
                                hole=0.3,
                                color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.bar(severity_counts.sort_values('Contagem', ascending=True), 
                                x='Contagem', 
                                y='RAM Potential',
                                orientation='h',
                                title='Ranking de Severidade',
                                color='Contagem',
                                color_continuous_scale='Reds',
                                text='Contagem')
                    fig.update_traces(textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)

            # === Tab 4: Tarefas / Atividades ===
            with tab4:
                st.subheader("Atividades Mais Registradas (Interativo)")
                
                top_n = st.slider("Número de atividades a exibir:", min_value=5, max_value=20, value=10, step=1)
                task_counts = df["Task / Activity"].value_counts().head(top_n).reset_index()
                task_counts.columns = ['Task / Activity', 'Ocorrências']

                fig = px.bar(task_counts, 
                            x='Ocorrências', 
                            y='Task / Activity',
                            orientation='h',
                            color='Ocorrências',
                            color_continuous_scale='Viridis',
                            text='Ocorrências',
                            title=f'Top {top_n} Atividades')
                fig.update_traces(textposition='outside')
                fig.update_layout(showlegend=False, height=max(400, top_n * 30))
                st.plotly_chart(fig, use_container_width=True)

            # === Tab 5: Consequências ===
            with tab5:
                st.subheader("Distribuição das Consequências (Interativo)")
                consequence_counts = df["Consequences"].value_counts().reset_index()
                consequence_counts.columns = ['Consequências', 'Ocorrências']

                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(consequence_counts, 
                                x='Ocorrências', 
                                y='Consequências',
                                orientation='h',
                                color='Ocorrências',
                                color_continuous_scale='Oranges',
                                text='Ocorrências',
                                title='Distribuição de Consequências')
                    fig.update_traces(textposition='outside')
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.pie(consequence_counts, 
                                values='Ocorrências', 
                                names='Consequências',
                                title='Proporção de Consequências',
                                hole=0.4)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)

            # === Tab 6: RAM Potential vs Risk Area ===
            with tab6:
                st.subheader("Correlação entre Severidade (RAM Potential) e Risk Area (Interativo)")

                correlation_data = pd.crosstab(df_filtered['RAM Potential'], df_filtered['Risk Area'])

                if correlation_data.empty:
                    st.warning("Não há dados suficientes para gerar a correlação.")
                else:
                    fig = px.imshow(correlation_data,
                                    labels=dict(x="Risk Area", y="RAM Potential", color="Ocorrências"),
                                    x=correlation_data.columns,
                                    y=correlation_data.index,
                                    color_continuous_scale="Blues",
                                    text_auto=True,
                                    aspect="auto")
                    fig.update_xaxes(side="bottom")
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)

            # === Tab 7: Análise Interativa Avançada ===
            with tab7:
                st.subheader("🎯 Análise Interativa Avançada")
                
                st.markdown("### Filtros Dinâmicos")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    selected_event_types = st.multiselect(
                        "Tipo de Evento:",
                        options=df_filtered["Event Type"].unique(),
                        default=df_filtered["Event Type"].unique()
                    )
                
                with col2:
                    selected_ram = st.multiselect(
                        "RAM Potential:",
                        options=df_filtered["RAM Potential"].unique(),
                        default=df_filtered["RAM Potential"].unique()
                    )
                
                with col3:
                    selected_risk_areas = st.multiselect(
                        "Risk Area:",
                        options=df_filtered["Risk Area"].unique(),
                        default=df_filtered["Risk Area"].unique()
                    )
                
                df_interactive = df_filtered[
                    (df_filtered["Event Type"].isin(selected_event_types)) &
                    (df_filtered["RAM Potential"].isin(selected_ram)) &
                    (df_filtered["Risk Area"].isin(selected_risk_areas))
                ]
                
                if len(df_interactive) > 0:
                    st.markdown(f"**Registros filtrados:** {len(df_interactive)} de {len(df_filtered)}")
                    
                    st.markdown("---")
                    st.markdown("### Visualizações Interativas")
                    
                    viz_col1, viz_col2 = st.columns(2)
                    
                    with viz_col1:
                        st.markdown("#### 📊 Scatter: Risk Area vs Event Type")
                        scatter_data = df_interactive.groupby(['Risk Area', 'Event Type']).size().reset_index(name='count')
                        fig = px.scatter(scatter_data, 
                                        x='Risk Area', 
                                        y='Event Type',
                                        size='count',
                                        color='count',
                                        color_continuous_scale='Turbo',
                                        hover_data=['count'],
                                        title='Intensidade de Eventos por Área de Risco')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with viz_col2:
                        st.markdown("#### 🌳 Treemap: Hierarquia de Riscos")
                        treemap_data = df_interactive.groupby(['Location', 'Risk Area', 'RAM Potential']).size().reset_index(name='count')
                        fig = px.treemap(treemap_data,
                                        path=['Location', 'Risk Area', 'RAM Potential'],
                                        values='count',
                                        color='count',
                                        color_continuous_scale='RdYlGn_r',
                                        title='Hierarquia: Location > Risk Area > Severidade')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    
                    viz_col3, viz_col4 = st.columns(2)
                    
                    with viz_col3:
                        st.markdown("#### 🎻 Violin Plot: Distribuição por Location")
                        violin_data = df_interactive.copy()
                        violin_data['count'] = 1
                        aggregated = violin_data.groupby(['Location', 'RAM Potential']).size().reset_index(name='frequency')
                        
                        ram_mapping = {ram: i for i, ram in enumerate(sorted(df_interactive['RAM Potential'].unique()))}
                        aggregated['ram_numeric'] = aggregated['RAM Potential'].map(ram_mapping)
                        
                        fig = px.violin(aggregated, 
                                       y='Location', 
                                       x='ram_numeric',
                                       color='Location',
                                       box=True,
                                       points='all',
                                       hover_data=['RAM Potential', 'frequency'],
                                       title='Distribuição de Severidade por Location')
                        fig.update_layout(showlegend=False, height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with viz_col4:
                        st.markdown("#### 📈 Sunburst: Análise Circular")
                        sunburst_data = df_interactive.groupby(['Event Type', 'Risk Area', 'Consequences']).size().reset_index(name='count')
                        fig = px.sunburst(sunburst_data,
                                         path=['Event Type', 'Risk Area', 'Consequences'],
                                         values='count',
                                         color='count',
                                         color_continuous_scale='Plasma',
                                         title='Evento > Área > Consequência')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    st.markdown("### 📊 Dashboard Completo")
                    
                    fig = make_subplots(
                        rows=2, cols=2,
                        specs=[
                            [{"type": "bar"}, {"type": "bar"}],
                            [{"type": "bar"}, {"type": "bar"}]
                        ],
                        subplot_titles=("Eventos por Location", "RAM Potential Distribution",
                                       "Top 5 Atividades", "Top 5 Consequências")
                    )
                    
                    loc_counts = df_interactive['Location'].value_counts().head(10)
                    fig.add_trace(
                        go.Bar(x=loc_counts.values, y=loc_counts.index, orientation='h', 
                              marker_color='lightblue', name='Location'),
                        row=1, col=1
                    )
                    
                    ram_counts = df_interactive['RAM Potential'].value_counts()
                    fig.add_trace(
                        go.Bar(x=ram_counts.values, y=ram_counts.index, orientation='h',
                              marker_color='coral', name='RAM'),
                        row=1, col=2
                    )
                    
                    task_counts = df_interactive['Task / Activity'].value_counts().head(5)
                    fig.add_trace(
                        go.Bar(x=task_counts.values, y=task_counts.index, orientation='h',
                              marker_color='lightgreen', name='Tasks'),
                        row=2, col=1
                    )
                    
                    cons_counts = df_interactive['Consequences'].value_counts().head(5)
                    fig.add_trace(
                        go.Bar(x=cons_counts.values, y=cons_counts.index, orientation='h',
                              marker_color='lightyellow', name='Consequences'),
                        row=2, col=2
                    )
                    
                    fig.update_layout(height=800, showlegend=False, title_text="Resumo Geral dos Dados Filtrados")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    st.markdown("### 📋 Dados Filtrados (Amostra)")
                    st.dataframe(df_interactive.head(50), use_container_width=True)
                    
                    csv = df_interactive.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Baixar dados filtrados (CSV)",
                        data=csv,
                        file_name='dados_filtrados.csv',
                        mime='text/csv',
                    )
                else:
                    st.warning("Nenhum dado corresponde aos filtros selecionados. Ajuste os filtros acima.")

        else:
            st.error(f"A planilha deve conter as colunas: {', '.join(required_cols)}")
else:
    st.info("Faça o upload de uma planilha para visualizar os gráficos.")
