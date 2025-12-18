import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Otimiza Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS "HARDCORE" (Para forçar visual Clean/Branco) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* RESET GERAL - Força fundo claro ignorando tema do sistema */
        .stApp {
            background-color: #F4F7FE;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Esconder Header padrão e Rodapé do Streamlit */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 5rem;}

        /* ESTILO DA SIDEBAR (Branca e Clean) */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {
            color: #2B3674 !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
            color: #A3AED0 !important;
        }

        /* Corrigir Inputs (Selectbox) na Sidebar */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #F4F7FE !important;
            color: #2B3674 !important;
            border: none;
            border-radius: 10px;
        }
        .stSelectbox svg {
            fill: #2B3674 !important;
        }

        /* ESTILIZAR BOTÕES (Tirar o vermelho/padrão) */
        /* Botão Primário (Dashboard) vira Teal */
        div.stButton > button:first-child {
            background-color: #FFFFFF;
            color: #A3AED0;
            border: 1px solid #F4F7FE;
            border-radius: 12px;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }
        div.stButton > button:hover {
            color: #17A2B8;
            border-color: #17A2B8;
            background-color: #F0FDFA;
        }
        /* Botão Ativo (Simulação visual) */
        div.stButton > button:active, div.stButton > button:focus {
            background-color: #17A2B8 !important;
            color: white !important;
            border: none;
        }

        /* CARDS GERAIS */
        .css-card {
            background-color: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05); /* Sombra mais suave */
            margin-bottom: 20px;
            height: 100%;
        }

        /* CARD DESTAQUE (Teal) */
        .css-highlight-card {
            background: linear-gradient(135deg, #17A2B8 0%, #008080 100%);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0px 10px 25px rgba(23, 162, 184, 0.4);
            margin-bottom: 20px;
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        /* Texto Global Escuro (Para evitar texto branco no fundo branco) */
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #2B3674;
        }
        /* Texto dentro do Card Destaque deve ser branco */
        .css-highlight-card h1, .css-highlight-card h3, .css-highlight-card div, .css-highlight-card span {
            color: #FFFFFF !important;
        }

    </style>
""", unsafe_allow_html=True)

# --- 3. DADOS (MANTIDOS) ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    data = []
    vistoriadores = ['Carlos Silva', 'Ana Souza', 'Roberto Dias', 'Fernanda Lima']
    resultados = ['Aprovado', 'Reprovado', 'Aprovado com Restrição']
    
    for _ in range(500):
        dt = np.random.choice(dates)
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'data': dt,
            'vistoriador': np.random.choice(vistoriadores),
            'resultado': np.random.choice(resultados, p=[0.7, 0.2, 0.1]),
            'valor': np.random.choice([100, 120, 150])
        })
    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'])
    df['dia_str'] = df['data'].dt.strftime('%d/%m')
    return df.sort_values('data')

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    # Avatar e Nome
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=55)
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:16px;'>Gestor Otimiza</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#A3AED0;'>Administrador</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu (Usando botões estilizados pelo CSS acima)
    st.caption("MENU")
    if st.button("📊 Dashboard Geral"):
        pass # Lógica de navegação iria aqui
    if st.button("💰 Financeiro"):
        pass
    if st.button("👥 Equipe"):
        pass
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("FILTRAGEM")
    vistoriador_sel = st.multiselect("Selecionar Vistoriador", df['vistoriador'].unique())

if vistoriador_sel:
    df = df[df['vistoriador'].isin(vistoriador_sel)]

# --- 5. LAYOUT PRINCIPAL ---

col_left, col_right = st.columns([1, 2], gap="medium")

with col_left:
    # 1. CARD DESTAQUE (TEAL)
    faturamento_total = df['valor'].sum()
    st.markdown(f"""
        <div class="css-highlight-card">
            <h3 style="font-size:14px; opacity:0.9; margin-bottom:5px; font-weight:400;">Faturamento Acumulado</h3>
            <h1 style="font-size:36px; margin:0; font-weight:700; letter-spacing:-1px;">R$ {faturamento_total:,.2f}</h1>
            <div style="margin-top:20px; display:flex; align-items:center;">
                <span style="background-color:rgba(255,255,255,0.25); padding:5px 12px; border-radius:20px; font-size:12px; font-weight:600;">
                +12% vs mês anterior
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. LISTA DE VISTORIAS (CORRIGIDA)
    st.markdown("""<div class="css-card"><h4 style="margin-bottom:20px;">Últimas Vistorias</h4>""", unsafe_allow_html=True)
    
    recentes = df.tail(4).sort_values('data', ascending=False)
    
    for index, row in recentes.iterrows():
        icon_bg = "#E6F7F0" if row['resultado'] == 'Aprovado' else "#FFF0F0"
        icon_color = "#00C853" if row['resultado'] == 'Aprovado' else "#FF5252"
        icon_symbol = "check_circle" if row['resultado'] == 'Aprovado' else "warning"
        
        # Usando CSS Flexbox inline para alinhar perfeitamente
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #F4F7FE; padding-bottom:10px;">
                <div style="display:flex; align-items:center;">
                    <div style="width:40px; height:40px; background-color:{icon_bg}; border-radius:12px; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                        <span style="color:{icon_color}; font-weight:bold; font-size:16px;">●</span>
                    </div>
                    <div>
                        <div style="font-weight:bold; font-size:14px; color:#2B3674;">{row['vistoriador']}</div>
                        <div style="font-size:11px; color:#A3AED0;">ID: {row['id_laudo']} • {row['dia_str']}</div>
                    </div>
                </div>
                <div style="font-weight:bold; color:#17A2B8; font-size:14px;">+R$ {row['valor']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # 3. GRÁFICO DE ÁREA
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-bottom:15px;">Volume Diário de Laudos</h4>', unsafe_allow_html=True)
    
    df_day = df.groupby('dia_str')['id_laudo'].count().reset_index()
    
    fig = px.area(df_day, x='dia_str', y='id_laudo')
    fig.update_traces(line_color='#17A2B8', fillcolor='rgba(23, 162, 184, 0.2)')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=10, b=0, l=0, r=0),
        xaxis=dict(showgrid=False, title=None, tickfont=dict(color='#A3AED0', size=11)),
        yaxis=dict(showgrid=True, gridcolor='#F4F7FE', title=None, tickfont=dict(color='#A3AED0', size=11)),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. MINI CARDS LADO A LADO
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="css-card" style="display:flex; align-items:center; padding:25px;">
                <div style="width:50px; height:50px; background-color:#F4F7FE; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px; font-size:20px;">
                🏷️
                </div>
                <div>
                    <div style="font-size:12px; color:#A3AED0; margin-bottom:2px;">Ticket Médio</div>
                    <div style="font-size:20px; font-weight:bold; color:#2B3674;">R$ {df['valor'].mean():.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        reprovados = len(df[df['resultado'] == 'Reprovado'])
        st.markdown(f"""
            <div class="css-card" style="display:flex; align-items:center; padding:25px;">
                <div style="width:50px; height:50px; background-color:#FFF0F0; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px; font-size:20px;">
                ⚠️
                </div>
                <div>
                    <div style="font-size:12px; color:#A3AED0; margin-bottom:2px;">Reprovações</div>
                    <div style="font-size:20px; font-weight:bold; color:#2B3674;">{reprovados} un.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- RODAPÉ: PERFORMANCE (CORRIGIDO O ERRO DAS CAIXAS PRETAS) ---
st.markdown('<h4 style="margin-top:10px; margin-bottom:15px;">Performance da Equipe</h4>', unsafe_allow_html=True)
cols = st.columns(4)
stats_vistoriador = df.groupby('vistoriador')['id_laudo'].count().sort_values(ascending=False)

i = 0
for vistoriador, qtd in stats_vistoriador.items():
    if i < 4: 
        with cols[i]:
            # CORREÇÃO CRÍTICA: Removemos a indentação dentro do HTML para evitar que vire bloco de código
            html_card = f"""
            <div class="css-card" style="text-align:center; padding:25px;">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={vistoriador}" style="width:60px; height:60px; border-radius:50%; margin-bottom:15px; border:3px solid #F4F7FE;">
                <h4 style="margin:0; font-size:16px; color:#2B3674;">{vistoriador}</h4>
                <p style="font-size:11px; color:#A3AED0; margin-bottom:20px;">Técnico Especialista</p>
                <div style="background-color:#F4F7FE; border-radius:12px; padding:10px;">
                    <span style="font-weight:800; color:#17A2B8; font-size:20px;">{qtd}</span>
                    <br><span style="font-size:10px; color:#A3AED0; text-transform:uppercase;">Laudos Totais</span>
                </div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        i += 1
