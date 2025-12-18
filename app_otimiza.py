import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Otimiza Operacional",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS "HARDCORE" (Manter Estética Clean/Teal) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* RESET GERAL */
        .stApp {
            background-color: #F4F7FE;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Ocultar elementos padrão */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 5rem;}

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {color: #2B3674 !important;}
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {color: #A3AED0 !important;}

        /* Inputs na Sidebar */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #F4F7FE !important;
            color: #2B3674 !important;
            border: none;
            border-radius: 10px;
        }
        .stSelectbox svg {fill: #2B3674 !important;}

        /* BOTÕES (Estilo Menu Passivo) */
        div.stButton > button {
            background-color: #FFFFFF;
            color: #A3AED0;
            border: 1px solid #F4F7FE;
            border-radius: 12px;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            width: 100%;
            text-align: left;
            padding-left: 20px;
        }
        /* Botão Ativo (Simulação) */
        .botao-ativo > button {
            background-color: #17A2B8 !important;
            color: white !important;
            border: none;
        }

        /* CARDS */
        .css-card {
            background-color: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
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
        }
        
        /* TIPOGRAFIA */
        h1, h2, h3, h4, h5, h6, p, span, div {color: #2B3674;}
        .css-highlight-card h1, .css-highlight-card h3, .css-highlight-card div, .css-highlight-card span {color: #FFFFFF !important;}

    </style>
""", unsafe_allow_html=True)

# --- 3. DADOS OPERACIONAIS SIMULADOS ---
@st.cache_data
def load_operational_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    data = []
    vistoriadores = ['Carlos Silva', 'Ana Souza', 'Roberto Dias', 'Fernanda Lima']
    
    for _ in range(600):
        dt = np.random.choice(dates)
        hora = np.random.randint(8, 18) # 08h as 18h
        dt_full = dt.replace(hour=hora, minute=np.random.randint(0, 59))
        
        # Simulando tempos das etapas (em minutos)
        t_vistoria = np.random.normal(15, 3) # Vistoria física
        t_upload = np.random.normal(5, 2)    # Upload fotos
        t_validacao = np.random.normal(8, 4) # Validação sistema
        
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'data_hora': dt_full,
            'dia_semana': dt_full.strftime('%A'), # Nome do dia
            'hora': hora,
            'vistoriador': np.random.choice(vistoriadores),
            'tempo_vistoria': t_vistoria,
            'tempo_upload': t_upload,
            'tempo_validacao': t_validacao,
            'tempo_total': t_vistoria + t_upload + t_validacao,
            'status': np.random.choice(['Concluído', 'Pendente', 'Refazer'], p=[0.85, 0.1, 0.05])
        })
    
    df = pd.DataFrame(data)
    
    # Traduzir dias da semana para ordenação
    dias_map = {'Monday': 'Seg', 'Tuesday': 'Ter', 'Wednesday': 'Qua', 'Thursday': 'Qui', 'Friday': 'Sex', 'Saturday': 'Sab', 'Sunday': 'Dom'}
    df['dia_semana_curto'] = df['dia_semana'].map(dias_map)
    
    return df

df = load_operational_data()

# --- 4. SIDEBAR (MENU DE EXEMPLO) ---
with st.sidebar:
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/9630/9630386.png", width=55) # Ícone Engrenagem/Ops
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:16px;'>Módulo Operacional</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#A3AED0;'>Chão de Fábrica</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu Visual (Sem lógica de redirecionamento, apenas protótipo)
    st.caption("NAVEGAÇÃO")
    
    # Gambiarra CSS para simular o botão ativo apenas no primeiro
    st.markdown('<div class="botao-ativo">', unsafe_allow_html=True)
    st.button("⏱️ Eficiência & Tempos")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.button("📅 Agenda & Boxes")
    st.button("📉 Controle de Qualidade")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("FILTROS DE TURNO")
    periodo = st.selectbox("Período", ["Todos", "Manhã", "Tarde"])
    equipe = st.multiselect("Vistoriadores", df['vistoriador'].unique(), default=df['vistoriador'].unique())

# Filtragem básica
if equipe:
    df = df[df['vistoriador'].isin(equipe)]

# --- 5. DASHBOARD OPERACIONAL ---

col_left, col_right = st.columns([1, 2], gap="medium")

# --- COLUNA ESQUERDA: KPIs GERAIS ---
with col_left:
    
    # 1. CARD PRINCIPAL: TEMPO MÉDIO GLOBAL
    avg_total = df['tempo_total'].mean()
    st.markdown(f"""
        <div class="css-highlight-card">
            <h3 style="font-size:14px; opacity:0.9; margin-bottom:5px; font-weight:400;">Tempo Médio Total (TMA)</h3>
            <h1 style="font-size:42px; margin:0; font-weight:700;">{avg_total:.1f} min</h1>
            <div style="margin-top:15px; display:flex; align-items:center; justify-content:space-between;">
                <span style="font-size:12px; opacity:0.8;">Meta: 25.0 min</span>
                <span style="background-color:rgba(255,255,255,0.25); padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;">
                ⚠ +2.3 min vs Meta
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. MINI CARDS: VOLUME E GARGALO
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="css-card" style="padding:15px; text-align:center;">
                <div style="font-size:12px; color:#A3AED0;">Vistorias Hoje</div>
                <div style="font-size:24px; font-weight:bold; color:#2B3674;">{len(df[df['data_hora'].dt.date == df['data_hora'].dt.date.max()])}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        # Lógica simples para achar o gargalo (etapa mais demorada)
        medias = df[['tempo_vistoria', 'tempo_upload', 'tempo_validacao']].mean()
        gargalo = medias.idxmax().replace('tempo_', '').capitalize()
        st.markdown(f"""
            <div class="css-card" style="padding:15px; text-align:center;">
                <div style="font-size:12px; color:#A3AED0;">Maior Gargalo</div>
                <div style="font-size:20px; font-weight:bold; color:#FF5252;">{gargalo}</div>
            </div>
        """, unsafe_allow_html=True)

    # 3. ANÁLISE DE GARGALOS (Etapas)
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h5 style="margin-bottom:15px;">Tempo por Etapa (min)</h5>', unsafe_allow_html=True)
    
    # Preparando dados para gráfico de barras empilhadas ou simples
    etapas_df = pd.DataFrame({
        'Etapa': ['Vistoria Física', 'Upload Fotos', 'Validação'],
        'Tempo': [df['tempo_vistoria'].mean(), df['tempo_upload'].mean(), df['tempo_validacao'].mean()],
        'Cor': ['#17A2B8', '#A3AED0', '#2B3674']
    })
    
    fig_bar = px.bar(etapas_df, x='Tempo', y='Etapa', orientation='h', text='Tempo')
    fig_bar.update_traces(marker_color=etapas_df['Cor'], texttemplate='%{text:.1f}', textposition='inside')
    fig_bar.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(showgrid=False, showticklabels=False, title=None),
        yaxis=dict(showgrid=False, title=None, tickfont=dict(color='#2B3674', size=12)),
        height=200, showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- COLUNA DIREITA: VISUALIZAÇÕES PRINCIPAIS ---
with col_right:
    
    # 4. MAPA DE CALOR (Ocupação dos Boxes)
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-bottom:5px;">Mapa de Calor: Ocupação dos Boxes</h4>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px; color:#A3AED0; margin-bottom:15px;">Intensidade de vistorias por Dia da Semana e Horário</p>', unsafe_allow_html=True)
    
    # Criando matriz para Heatmap
    heatmap_data = df.groupby(['dia_semana_curto', 'hora']).size().reset_index(name='qtd')
    # Ordenar dias corretamente
    dias_ordem = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    
    fig_heat = px.density_heatmap(
        heatmap_data, 
        x='hora', 
        y='dia_semana_curto', 
        z='qtd', 
        category_orders={"dia_semana_curto": dias_ordem},
        color_continuous_scale=['#F4F7FE', '#17A2B8', '#004D40'] # Branco -> Teal -> Escuro
    )
    
    fig_heat.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(title="Horário", dtick=1, tickfont=dict(color='#A3AED0')),
        yaxis=dict(title=None, tickfont=dict(color='#2B3674', size=12)),
        height=320,
        coloraxis_showscale=False # Remove a barra lateral de cores para limpar
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. RANKING DE PRODUTIVIDADE E EFICIÊNCIA
    st.markdown('<h5 style="margin-top:10px;">Eficiência da Equipe Técnica</h5>', unsafe_allow_html=True)
    
    # Agrupando dados por vistoriador
    team_stats = df.groupby('vistoriador').agg(
        total=('id_laudo', 'count'),
        tempo_medio=('tempo_total', 'mean')
    ).sort_values('tempo_medio', ascending=True) # Melhor é quem faz em menos tempo (com qualidade)

    cols = st.columns(4)
    i = 0
    for vistoriador, row in team_stats.iterrows():
        if i < 4:
            with cols[i]:
                # Definir cor do indicador de tempo (Verde se rápido, Vermelho se lento)
                cor_tempo = "#00C853" if row['tempo_medio'] < 28 else "#FF5252"
                
                html_card = f"""
                <div class="css-card" style="padding: 15px; text-align: center;">
                    <div style="font-weight:bold; color:#2B3674; font-size:14px; margin-bottom:5px;">{vistoriador}</div>
                    <div style="display:flex; justify-content:center; align-items:baseline; margin-bottom:5px;">
                        <span style="font-size:24px; font-weight:800; color:{cor_tempo};">{row['tempo_medio']:.0f}</span>
                        <span style="font-size:12px; color:#A3AED0; margin-left:3px;">min/méd</span>
                    </div>
                    <div style="font-size:11px; color:#A3AED0; background-color:#F4F7FE; padding:4px; border-radius:8px;">
                        {row['total']} vistorias totais
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
            i += 1
