import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Otimiza Financeiro",
    page_icon="💲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURAÇÃO DE ESTILO E CORES (PADRONIZAÇÃO) ---
# Definindo variáveis para garantir consistência em todo o código
CORES = {
    "teal": "#17A2B8",
    "teal_dark": "#008080",
    "navy": "#2B3674",
    "grey_light": "#A3AED0",
    "grey_text": "#64748B", # Cinza mais escuro para leitura (Eixos)
    "bg_light": "#F4F7FE",
    "white": "#FFFFFF",
    "black": "#000000"
}

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        .stApp {{
            background-color: {CORES['bg_light']};
            font-family: 'Roboto', sans-serif;
        }}
        
        .block-container {{
            padding-top: 3.5rem; 
            padding-bottom: 3rem;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* SIDEBAR */
        [data-testid="stSidebar"] {{
            background-color: {CORES['white']};
            border-right: 1px solid #E0E0E0;
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {{color: {CORES['white']} !important;}}
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{color: {CORES['black']} !important;}}

        /* CARDS HTML (Texto) */
        .css-card {{
            background-color: {CORES['white']};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.04);
            height: 180px; 
            border: 1px solid #EFF0F6;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .css-highlight-card {{
            background: linear-gradient(135deg, {CORES['teal']} 0%, {CORES['teal_dark']} 100%);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0px 8px 20px rgba(23, 162, 184, 0.3);
            color: white;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        /* ESTILIZAÇÃO DOS GRÁFICOS (Container Plotly) */
        div[data-testid="stPlotlyChart"] {{
            background-color: {CORES['white']};
            border-radius: 16px;
            padding: 15px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.04);
            border: 1px solid #EFF0F6;
        }}

        /* TIPOGRAFIA PADRONIZADA DOS CARDS HTML */
        .card-title {{
            font-size: 13px;
            font-weight: 600;
            color: {CORES['grey_light']};
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-family: 'Roboto', sans-serif;
        }}
        
        .card-value {{
            font-size: 30px;
            font-weight: 700;
            color: {CORES['navy']};
        }}

        h1, h2, h3, h4, h5, h6, p, span, div {{color: {CORES['navy']};}}
        .css-highlight-card h1, .css-highlight-card h3, .css-highlight-card div, .css-highlight-card span {{color: {CORES['white']} !important;}}

    </style>
""", unsafe_allow_html=True)

# --- 3. DADOS ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    data = []
    vistoriadores = ['Carlos Silva', 'Ana Souza', 'Roberto Dias', 'Fernanda Lima']
    tipos_veiculo = {'Passeio': 150, 'Moto': 100, 'SUV/Van': 200, 'Caminhão': 300}
    
    for _ in range(600):
        dt = np.random.choice(dates)
        tipo = np.random.choice(list(tipos_veiculo.keys()), p=[0.5, 0.2, 0.2, 0.1])
        preco = tipos_veiculo[tipo]
        
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'data': dt,
            'vistoriador': np.random.choice(vistoriadores),
            'tipo_veiculo': tipo,
            'valor': preco,
            'status': np.random.choice(['Pago', 'Pendente'], p=[0.85, 0.15])
        })
    return pd.DataFrame(data)

df = load_data()

# --- 4. FUNÇÃO AUXILIAR DE LAYOUT DE GRÁFICO (FUNCIONALIDADE) ---
# Esta função aplica o padrão visual a todos os gráficos automaticamente
def aplicar_estilo_padrao(fig, titulo):
    fig.update_layout(
        title=dict(
            text=titulo.upper(), # Padroniza tudo em maiúsculo igual CSS
            font=dict(size=13, color=CORES['grey_light'], family="Roboto"), # Mesma fonte/cor do CSS .card-title
            x=0, 
            y=0.96
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto"), # Fonte global do gráfico
        margin=dict(t=40, b=20, l=10, r=10), # Margens padronizadas
    )
    # Padronização de Eixos (Melhoria de Contraste)
    fig.update_xaxes(
        showgrid=False, 
        tickfont=dict(size=12, color=CORES['grey_text']) # Texto maior e mais escuro
    )
    fig.update_yaxes(
        showgrid=True, 
        gridcolor='#F0F2F6', # Grade sutil
        tickfont=dict(size=12, color=CORES['grey_text'])
    )
    return fig

# --- 5. SIDEBAR ---
with st.sidebar:
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/2953/2953363.png", width=50)
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:15px;'>Módulo Financeiro</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:11px; color:{CORES['grey_light']};'>Receita & Vendas</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    periodo = st.selectbox("Período", ["Últimos 30 Dias", "Este Mês", "Ano Atual"])
    equipe = st.multiselect("Filtrar Vistoriador", df['vistoriador'].unique(), default=df['vistoriador'].unique())

if equipe:
    df = df[df['vistoriador'].isin(equipe)]

# --- 6. DASHBOARD LAYOUT ---

# LINHA 1: 3 CARDS ALINHADOS
c1, c2, c3 = st.columns([1, 1, 1], gap="medium")

with c1:
    receita_total = df['valor'].sum()
    st.markdown(f"""
        <div class="css-highlight-card">
            <div style="font-size:12px; opacity:0.9; font-family: 'Roboto', sans-serif; margin-bottom:5px;">RECEITA TOTAL</div>
            <div style="font-size:28px; font-weight:700; margin-bottom:5px;">R$ {receita_total:,.2f}</div>
            <div style="font-size:11px; opacity:0.8;">
                <span style="background-color:rgba(255,255,255,0.2); padding:3px 8px; border-radius:8px;">🚀 +15% vs mês anterior</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    ticket_medio = df['valor'].mean()
    st.markdown(f"""
        <div class="css-card">
            <div class="card-title">Ticket Médio</div>
            <div class="card-value">R$ {ticket_medio:.2f}</div>
            <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">Média por vistoria</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    # --- GRÁFICO DE PIZZA (Padronizado) ---
    df_status = df['status'].value_counts().reset_index()
    df_status.columns = ['Status', 'Count']
    
    fig_pie = px.pie(df_status, names='Status', values='Count', 
                     color='Status', color_discrete_map={'Pago': CORES['teal'], 'Pendente': '#FF5252'})
    
    # Aplicar função de estilo padrão
    fig_pie = aplicar_estilo_padrao(fig_pie, "Status de Pagamento")
    
    # Ajustes específicos para Pizza (Legenda e Altura)
    fig_pie.update_layout(
        height=180, 
        legend=dict(
            orientation="v", 
            yanchor="middle", y=0.5, 
            xanchor="right", x=1,
            font=dict(size=11, color=CORES['grey_text']) # Fonte da legenda mais legível
        )
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})


# LINHA 2: GRÁFICO DE BARRAS (Padronizado)
st.markdown("<br>", unsafe_allow_html=True)

df_veiculo = df.groupby('tipo_veiculo')['id_laudo'].count().reset_index().sort_values('id_laudo', ascending=False)
fig_bar = px.bar(
    df_veiculo, x='tipo_veiculo', y='id_laudo', color='tipo_veiculo',
    color_discrete_sequence=[CORES['teal'], '#20B2AA', '#008080', '#5F9EA0']
)

# Aplicar função de estilo padrão
fig_bar = aplicar_estilo_padrao(fig_bar, "Quantidade de Vistorias por Tipo de Veículo")

# Ajustes específicos para Barras
fig_bar.update_layout(
    height=320,
    xaxis=dict(title=None), # Remove título X para limpar
    yaxis=dict(title=None), # Remove título Y
    showlegend=False
)
fig_bar.update_traces(marker_line_width=0, texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})


# LINHA 3: RANKING
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f'<h5 style="color:{CORES["navy"]}; margin-bottom:15px; font-family:Roboto;">Receita Gerada por Vistoriador</h5>', unsafe_allow_html=True)

team_finance = df.groupby('vistoriador').agg(
    total_receita=('valor', 'sum'),
    qtd=('id_laudo', 'count')
).sort_values('total_receita', ascending=False)

cols = st.columns(4, gap="medium")
i = 0
for vistoriador, row in team_finance.iterrows():
    if i < 4:
        with cols[i]:
            border_color = CORES['teal'] if i == 0 else "#E0E0E0" 
            html_card = f"""
            <div class="css-card" style="height:auto; padding: 20px; text-align: center; border-bottom: 4px solid {border_color};">
                <div style="font-weight:600; color:{CORES['navy']}; font-size:14px; margin-bottom:8px;">{vistoriador}</div>
                <div style="font-size:24px; font-weight:800; color:{CORES['teal']};">R$ {row['total_receita']:,.0f}</div>
                <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">{row['qtd']} vistorias</div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        i += 1



