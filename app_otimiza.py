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

# --- 2. CSS AVANÇADO (CORREÇÃO DE CONTRASTE E ALINHAMENTO) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* 1. Forçar Fundo Geral Claro e Texto Escuro (Resolve o bug do texto branco) */
        .stApp {
            background-color: #F4F7FE; /* Cinza azulado muito claro (igual referência) */
            font-family: 'Roboto', sans-serif;
        }
        
        /* Forçar cor de texto global para evitar conflito com Dark Mode */
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: #2B3674; /* Azul marinho escuro para textos */
        }

        /* 2. Estilização da Sidebar (Para ficar branca igual a referência) */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #F0F0F0;
        }
        [data-testid="stSidebar"] * {
            color: #A3AED0 !important; /* Texto cinza claro para menus */
        }
        [data-testid="stSidebar"] h1 {
            color: #2B3674 !important; /* Título do app escuro */
        }

        /* 3. Cards (Caixas Brancas) */
        .css-card {
            background-color: #FFFFFF;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0px 18px 40px rgba(112, 144, 176, 0.12);
            margin-bottom: 20px;
            height: 100%; /* Para alinhar alturas */
        }

        /* 4. Card Destaque (Teal/Verde) - Texto DEVE ser branco aqui */
        .css-highlight-card {
            background: linear-gradient(135deg, #17A2B8 0%, #008080 100%);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0px 18px 40px rgba(23, 162, 184, 0.2);
            margin-bottom: 20px;
            color: white !important;
        }
        /* Forçando texto branco ESPECIFICAMENTE dentro do card destaque */
        .css-highlight-card h1, .css-highlight-card h3, .css-highlight-card p, .css-highlight-card span {
            color: #FFFFFF !important;
        }

        /* 5. Ajustes de Espaçamento */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }
        
        /* Títulos de Seção */
        .section-title {
            font-size: 14px;
            color: #A3AED0;
            font-weight: 500;
            margin-bottom: 10px;
        }
        
        /* Remove padding padrão dos botões para alinhar melhor */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 500;
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

# --- 4. SIDEBAR (Estilo Clean) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
    st.markdown("<h3 style='margin-top:0'>Gestor Otimiza</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    # Botões simples (nativos do streamlit, mas o CSS vai limpar o visual ao redor)
    st.caption("MENU PRINCIPAL")
    st.button("📊 Dashboard", type="primary", use_container_width=True)
    st.button("💳 Financeiro", use_container_width=True)
    st.button("👥 Equipe Técnica", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("FILTROS")
    vistoriador_sel = st.multiselect("Vistoriador", df['vistoriador'].unique())

if vistoriador_sel:
    df = df[df['vistoriador'].isin(vistoriador_sel)]

# --- 5. LAYOUT PRINCIPAL ---

# Título da Página (Escondido visualmente mas bom para semântica)
# st.title("Visão Geral") 

col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    # --- CARD DE DESTAQUE (TEAL) ---
    faturamento_total = df['valor'].sum()
    st.markdown(f"""
        <div class="css-highlight-card">
            <h3 style="font-size:14px; opacity:0.8; margin-bottom:5px;">Faturamento Total</h3>
            <h1 style="font-size:32px; margin:0; font-weight:700;">R$ {faturamento_total:,.2f}</h1>
            <div style="margin-top:15px;">
                <span style="background-color:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px; font-size:12px; font-weight:bold;">
                🚀 +12% vs mês anterior
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- LISTA DE VISTORIAS (TIPO "INCOME" DA REFERÊNCIA) ---
    st.markdown("""<div class="css-card">
        <h4 style="color:#2B3674; margin-bottom:20px;">Últimas Vistorias</h4>
    """, unsafe_allow_html=True)
    
    recentes = df.tail(4).sort_values('data', ascending=False)
    
    for index, row in recentes.iterrows():
        # Lógica de ícone e cor
        if row['resultado'] == 'Aprovado':
            icon_bg = "#E6F7F0" # Fundo verde claro
            icon = "✅"
        else:
            icon_bg = "#FFF0F0" # Fundo vermelho claro
            icon = "⚠️"
            
        st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:15px; padding-bottom:10px; border-bottom:1px solid #F4F7FE;">
                <div style="display:flex; align-items:center;">
                    <div style="width:40px; height:40px; background-color:{icon_bg}; border-radius:10px; display:flex; align-items:center; justify-content:center; margin-right:12px; font-size:18px;">
                        {icon}
                    </div>
                    <div>
                        <div style="font-weight:bold; font-size:14px; color:#2B3674;">{row['vistoriador']}</div>
                        <div style="font-size:12px; color:#A3AED0;">Laudo #{row['id_laudo']} • {row['dia_str']}</div>
                    </div>
                </div>
                <div style="font-weight:bold; color:#17A2B8; font-size:14px;">+ R$ {row['valor']}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # --- GRÁFICO PRINCIPAL ---
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#2B3674; margin-bottom:5px">Volume Diário</h4>', unsafe_allow_html=True)
    
    df_day = df.groupby('dia_str')['id_laudo'].count().reset_index()
    
    fig = px.area(df_day, x='dia_str', y='id_laudo')
    
    # Customizando o gráfico para ficar clean (fundo branco, linhas cinzas)
    fig.update_traces(line_color='#17A2B8', fillcolor='rgba(23, 162, 184, 0.2)')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=10, b=10, l=0, r=0),
        xaxis=dict(
            showgrid=False, 
            title=None, 
            tickfont=dict(color='#A3AED0', size=10) # Cor da fonte do eixo X
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#F4F7FE', 
            title=None, 
            tickfont=dict(color='#A3AED0', size=10) # Cor da fonte do eixo Y
        ),
        height=320,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MINI CARDS DE MÉTRICAS ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="css-card" style="padding:15px; display:flex; align-items:center;">
                <div style="margin-right:15px; background-color:#F4F7FE; width:45px; height:45px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px;">
                🏷️
                </div>
                <div>
                    <div style="font-size:12px; color:#A3AED0;">Ticket Médio</div>
                    <div style="font-size:18px; font-weight:bold; color:#2B3674;">R$ {df['valor'].mean():.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        reprovados = len(df[df['resultado'] == 'Reprovado'])
        st.markdown(f"""
            <div class="css-card" style="padding:15px; display:flex; align-items:center;">
                <div style="margin-right:15px; background-color:#FFF0F0; width:45px; height:45px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px;">
                📉
                </div>
                <div>
                    <div style="font-size:12px; color:#A3AED0;">Reprovações</div>
                    <div style="font-size:18px; font-weight:bold; color:#2B3674;">{reprovados} un.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- RODAPÉ: PERFORMANCE (Estilo Cards Verticais) ---
st.markdown('<h4 style="color:#2B3674; margin-top:10px;">Performance da Equipe</h4>', unsafe_allow_html=True)
cols = st.columns(4)
stats_vistoriador = df.groupby('vistoriador')['id_laudo'].count().sort_values(ascending=False)

i = 0
for vistoriador, qtd in stats_vistoriador.items():
    if i < 4: 
        with cols[i]:
            # Avatar aleatório apenas para visual
            avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={vistoriador}"
            
            st.markdown(f"""
                <div class="css-card" style="text-align:center; padding: 20px;">
                    <img src="{avatar_url}" style="width:50px; height:50px; border-radius:50%; margin-bottom:10px;">
                    <h4 style="margin:0; font-size:16px; color:#2B3674;">{vistoriador}</h4>
                    <p style="font-size:12px; color:#A3AED0; margin-bottom:15px;">Técnico III</p>
                    
                    <div style="background-color:#F4F7FE; border-radius:10px; padding:10px;">
                        <span style="font-weight:bold; color:#17A2B8; font-size:18px;">{qtd}</span>
                        <br><span style="font-size:10px; color:#A3AED0;">LAUDOS</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        i += 1
