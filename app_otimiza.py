pip install pandas
pip install plotly
pip install numpy
pip install setreamlit

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Módulo Inteligência Otimiza",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado
st.markdown("""
    <style>
        .block-container {padding-top: 1rem; padding-bottom: 0rem;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. SIMULAÇÃO DE DADOS ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    
    data = []
    vistoriadores = ['Carlos Silva', 'Ana Souza', 'Roberto Dias', 'Fernanda Lima']
    resultados = ['Aprovado', 'Reprovado', 'Aprovado com Restrição']
    
    for _ in range(500):
        dt = np.random.choice(dates)
        hora = np.random.randint(8, 18) 
        dt_full = dt.replace(hour=hora, minute=np.random.randint(0, 59))
        
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'data_hora': dt_full,
            'vistoriador': np.random.choice(vistoriadores),
            'resultado': np.random.choice(resultados, p=[0.7, 0.2, 0.1]),
            'tempo_execucao_min': np.random.normal(25, 5),
            'valor_servico': np.random.choice([100, 120, 150])
        })
    
    df = pd.DataFrame(data)
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    df['dia'] = df['data_hora'].dt.date
    df['hora'] = df['data_hora'].dt.hour
    return df

df = load_data()

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2554/2554936.png", width=50)
    st.title("Filtros Operacionais")
    
    min_date = df['dia'].min()
    max_date = df['dia'].max()
    date_range = st.date_input("Período de Análise", [min_date, max_date])
    
    vistoriador_filter = st.multiselect(
        "Selecionar Vistoriador", 
        options=df['vistoriador'].unique(),
        default=df['vistoriador'].unique()
    )

if len(date_range) == 2:
    mask = (df['dia'] >= date_range[0]) & (df['dia'] <= date_range[1]) & (df['vistoriador'].isin(vistoriador_filter))
    df_filtered = df.loc[mask]
else:
    df_filtered = df.loc[df['vistoriador'].isin(vistoriador_filter)]

# --- 4. DASHBOARD PRINCIPAL ---

st.header("📊 Painel Operacional - Vistoria Veicular")

# 4.1 KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_laudos = len(df_filtered)
    st.metric("Total de Laudos", total_laudos)

with col2:
    tempo_medio = df_filtered['tempo_execucao_min'].mean()
    st.metric("Tempo Médio (min)", f"{tempo_medio:.1f}")

with col3:
    reprovacoes = df_filtered[df_filtered['resultado'] == 'Reprovado'].shape[0]
    taxa_reprov = (reprovacoes / total_laudos) * 100 if total_laudos > 0 else 0
    st.metric("Taxa de Reprovação", f"{taxa_reprov:.1f}%", delta_color="inverse")

with col4:
    faturamento = df_filtered['valor_servico'].sum()
    st.metric("Receita Estimada", f"R$ {faturamento:,.2f}")

st.markdown("---")

# 4.2 Visualizações Gráficas

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Volume de Vistorias por Dia")
    df_day = df_filtered.groupby('dia').size().reset_index(name='contagem')
    fig_line = px.line(df_day, x='dia', y='contagem', markers=True, 
                       line_shape='spline', render_mode='svg')
    fig_line.update_layout(xaxis_title=None, yaxis_title="Qtd Laudos", template="plotly_white")
    fig_line.update_traces(line_color='#2E8B57')
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("Resultado dos Laudos")
    # CORREÇÃO APLICADA AQUI: px.pie com hole=0.4
    fig_pie = px.pie(df_filtered, names='resultado', hole=0.4, 
                     color_discrete_sequence=['#2E8B57', '#E74C3C', '#F1C40F'])
    fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("Produtividade por Vistoriador")
    df_prod = df_filtered.groupby('vistoriador').agg(
        qtd=('id_laudo', 'count'),
        tempo_medio=('tempo_execucao_min', 'mean')
    ).reset_index().sort_values('qtd', ascending=True)
    
    fig_bar = px.bar(df_prod, x='qtd', y='vistoriador', orientation='h', 
                     text='qtd', color='tempo_medio', 
                     color_continuous_scale='Greens')
    fig_bar.update_layout(xaxis_title="Qtd Laudos", yaxis_title=None)
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    st.subheader("Mapa de Calor: Horários de Pico")
    df_hour = df_filtered.groupby('hora').size().reset_index(name='volume')
    fig_heat = px.bar(df_hour, x='hora', y='volume')
    fig_heat.update_traces(marker_color='#2E8B57')
    fig_heat.update_layout(xaxis=dict(tickmode='linear', dtick=1), title="Ocupação dos Boxes por Hora")
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

st.caption("Módulo de Inteligência Otimiza v1.1 | Dados atualizados em tempo real via API.")
