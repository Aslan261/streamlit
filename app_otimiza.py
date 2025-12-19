import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Financeiro",
    page_icon="💲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS AJUSTADO (ALINHAMENTO PERFEITO) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* RESET GERAL */
        .stApp {
            background-color: #F4F7FE;
            font-family: 'Roboto', sans-serif;
        }
        
        /* CORREÇÃO BARRA PRETA SUPERIOR */
        .block-container {
            padding-top: 3.5rem; 
            padding-bottom: 3rem;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {color: #2B3674 !important;}
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {color: #A3AED0 !important;}

        /* TAGS */
        span[data-baseweb="tag"] {
            background-color: rgba(23, 162, 184, 0.15) !important;
            border: 1px solid rgba(23, 162, 184, 0.5);
        }
        span[data-baseweb="tag"] span {
            color: #17A2B8 !important;
        }

        /* CARDS UNIFICADOS (Tamanho igual) */
        .css-card {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.04);
            margin-bottom: 0px; 
            height: 160px; /* Altura fixa para alinhar a primeira linha */
            border: 1px solid #EFF0F6;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        /* Card Grande (Gráfico de Barras) - Altura Automática */
        .css-card-large {
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.04);
            border: 1px solid #EFF0F6;
            height: 100%;
        }

        /* CARD DESTAQUE (Teal) */
        .css-highlight-card {
            background: linear-gradient(135deg, #17A2B8 0%, #008080 100%);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0px 8px 20px rgba(23, 162, 184, 0.3);
            color: white;
            height: 160px; /* Mesma altura dos vizinhos */
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        /* Títulos */
        .card-title {
            font-size: 14px;
            font-weight: 600;
            color: #A3AED0;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .card-value {
            font-size: 32px;
            font-weight: 700;
            color: #2B3674;
        }

        /* TIPOGRAFIA */
        h1, h2, h3, h4, h5, h6, p, span, div {color: #2B3674;}
        .css-highlight-card h1, .css-highlight-card h3, .css-highlight-card div, .css-highlight-card span {color: #FFFFFF !important;}

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

# --- 4. SIDEBAR ---
with st.sidebar:
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/2953/2953363.png", width=50)
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:15px;'>Módulo Financeiro</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px; color:#A3AED0;'>Receita & Vendas</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    periodo = st.selectbox("Período", ["Últimos 30 Dias", "Este Mês", "Ano Atual"])
    equipe = st.multiselect("Filtrar Vistoriador", df['vistoriador'].unique(), default=df['vistoriador'].unique())

if equipe:
    df = df[df['vistoriador'].isin(equipe)]

# --- 5. DASHBOARD LAYOUT ---

# LINHA 1: 3 CARDS ALINHADOS (Receita | Ticket | Status)
c1, c2, c3 = st.columns([1, 1, 1], gap="medium")

with c1:
    # KPI 1: RECEITA TOTAL (TEAL)
    receita_total = df['valor'].sum()
    st.markdown(f"""
        <div class="css-highlight-card">
            <div style="font-size:13px; opacity:0.9; margin-bottom:5px;">RECEITA TOTAL</div>
            <div style="font-size:30px; font-weight:700; margin-bottom:5px;">R$ {receita_total:,.2f}</div>
            <div style="font-size:11px; opacity:0.8;">
                <span style="background-color:rgba(255,255,255,0.2); padding:3px 8px; border-radius:8px;">🚀 +15% vs mês anterior</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    # KPI 2: TICKET MÉDIO (BRANCO)
    ticket_medio = df['valor'].mean()
    st.markdown(f"""
        <div class="css-card">
            <div class="card-title">Ticket Médio</div>
            <div class="card-value">R$ {ticket_medio:.2f}</div>
            <div style="font-size:11px; color:#A3AED0;">Média por vistoria</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    # KPI 3: STATUS (PIE CHART CORRIGIDO)
    #st.markdown('<div class="css-card" style="padding:15px 20px;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Status de Pagamento</div>', unsafe_allow_html=True)
    
    df_status = df['status'].value_counts().reset_index()
    df_status.columns = ['Status', 'Count']
    
    # GRÁFICO DE PIZZA (Sem hole)
    fig_pie = px.pie(df_status, names='Status', values='Count', 
                     color='Status', color_discrete_map={'Pago': '#17A2B8', 'Pendente': '#FF5252'})
    
    fig_pie.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        # Margens ajustadas para caber a legenda embaixo
        margin=dict(t=5, b=15, l=5, r=5), 
        height=115, # Altura ajustada para o card de 160px
        showlegend=True, 
        # Legenda horizontal na parte inferior para dar espaço ao gráfico
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=10))
    )
    # Config para remover a barra de ferramentas do plotly (mais limpo)
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)


# LINHA 2: GRÁFICO DE BARRAS (Veículos)
#st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="css-card-large">', unsafe_allow_html=True)
st.markdown('<div class="card-title" style="margin-bottom:20px;">Quantidade de Vistorias por Tipo de Veículo</div>', unsafe_allow_html=True)

df_veiculo = df.groupby('tipo_veiculo')['id_laudo'].count().reset_index().sort_values('id_laudo', ascending=False)

fig_bar = px.bar(
    df_veiculo, 
    x='tipo_veiculo', 
    y='id_laudo', 
    color='tipo_veiculo',
    color_discrete_sequence=['#17A2B8', '#20B2AA', '#008080', '#5F9EA0']
)

fig_bar.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=0, b=0, l=0, r=0),
    xaxis=dict(title=None, showgrid=False, tickfont=dict(color='#A3AED0')),
    yaxis=dict(title=None, showgrid=True, gridcolor='#F4F7FE', tickfont=dict(color='#A3AED0')),
    height=280,
    showlegend=False
)
fig_bar.update_traces(marker_line_width=0, texttemplate='%{y}', textposition='outside')
st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)


# LINHA 3: RANKING FINANCEIRO
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h5 style="color:#2B3674; margin-bottom:15px;">Receita Gerada por Vistoriador</h5>', unsafe_allow_html=True)

team_finance = df.groupby('vistoriador').agg(
    total_receita=('valor', 'sum'),
    qtd=('id_laudo', 'count')
).sort_values('total_receita', ascending=False)

cols = st.columns(4, gap="medium")
i = 0
for vistoriador, row in team_finance.iterrows():
    if i < 4:
        with cols[i]:
            border_color = "#17A2B8" if i == 0 else "#E0E0E0" 
            html_card = f"""
            <div class="css-card-large" style="padding: 20px; text-align: center; border-bottom: 4px solid {border_color}; border-radius: 16px;">
                <div style="font-weight:600; color:#2B3674; font-size:14px; margin-bottom:8px;">{vistoriador}</div>
                <div style="font-size:24px; font-weight:800; color:#17A2B8;">R$ {row['total_receita']:,.0f}</div>
                <div style="font-size:11px; color:#A3AED0; margin-top:5px;">{row['qtd']} vistorias</div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        i += 1




