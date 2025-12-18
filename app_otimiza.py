import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Otimiza Operacional",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PARA ACABAMENTO FINO ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* RESET GERAL */
        .stApp {
            background-color: #F4F7FE;
            font-family: 'Roboto', sans-serif;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 1rem; padding-bottom: 3rem;}

        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {color: #2B3674 !important;}
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {color: #A3AED0 !important;}

        /* TAGS DA SIDEBAR (Correção de Cor) */
        span[data-baseweb="tag"] {
            background-color: rgba(23, 162, 184, 0.15) !important;
            border: 1px solid rgba(23, 162, 184, 0.5);
        }
        span[data-baseweb="tag"] span {
            color: #17A2B8 !important;
            font-weight: 600;
        }

        /* INPUTS */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #F4F7FE !important;
            color: #2B3674 !important;
            border: none;
            border-radius: 8px;
        }

        /* CARDS UNIFICADOS */
        .css-card {
            background-color: #FFFFFF;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03);
            margin-bottom: 0px; /* Removido margem extra */
            height: 100%; /* Força altura igual em colunas */
            border: 1px solid #F0F0F0;
        }

        /* CARD DESTAQUE (Teal) */
        .css-highlight-card {
            background: linear-gradient(135deg, #17A2B8 0%, #008080 100%);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 6px 15px rgba(23, 162, 184, 0.25);
            color: white;
            height: 100%;
        }
        
        /* Títulos dentro dos cards */
        .card-title {
            font-size: 14px;
            font-weight: 500;
            color: #2B3674;
            margin-bottom: 10px;
        }
        
        .card-subtitle {
            font-size: 11px;
            color: #A3AED0;
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
    
    for _ in range(600):
        dt = np.random.choice(dates)
        hora = np.random.randint(8, 18) 
        dt_full = dt.replace(hour=hora, minute=np.random.randint(0, 59))
        
        t_vistoria = np.random.normal(15, 3) 
        t_upload = np.random.normal(5, 2)    
        t_validacao = np.random.normal(8, 4) 
        
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'data_hora': dt_full,
            'dia_semana': dt_full.strftime('%A'),
            'hora': hora,
            'vistoriador': np.random.choice(vistoriadores),
            'tempo_vistoria': t_vistoria,
            'tempo_upload': t_upload,
            'tempo_validacao': t_validacao,
            'tempo_total': t_vistoria + t_upload + t_validacao,
            'status': np.random.choice(['Concluído', 'Pendente', 'Refazer'], p=[0.75, 0.15, 0.1])
        })
    df = pd.DataFrame(data)
    dias_map = {'Monday': 'Seg', 'Tuesday': 'Ter', 'Wednesday': 'Qua', 'Thursday': 'Qui', 'Friday': 'Sex', 'Saturday': 'Sab', 'Sunday': 'Dom'}
    df['dia_semana_curto'] = df['dia_semana'].map(dias_map)
    return df

df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/9630/9630386.png", width=50)
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:15px;'>Módulo Operacional</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px; color:#A3AED0;'>Chão de Fábrica</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("FILTROS GERAIS")
    periodo = st.selectbox("Turno de Trabalho", ["Todos", "Manhã", "Tarde"])
    equipe = st.multiselect("Vistoriadores", df['vistoriador'].unique(), default=df['vistoriador'].unique())

if equipe:
    df = df[df['vistoriador'].isin(equipe)]

# --- 5. DASHBOARD LAYOUT (GRID) ---

# LINHA 1: RESUMO OPERACIONAL (3 COLUNAS)
# Aqui juntamos o TMA, o Status e as Etapas. Ao colocar lado a lado, removemos espaços vazios.
c1, c2, c3 = st.columns([1, 1, 1], gap="medium")

with c1:
    # 1. KPI TMA (DESTAQUE)
    avg_total = df['tempo_total'].mean()
    st.markdown(f"""
        <div class="css-highlight-card">
            <div style="font-size:14px; opacity:0.9; margin-bottom:5px;">Tempo Médio Total (TMA)</div>
            <div style="font-size:36px; font-weight:700; margin-bottom:10px;">{avg_total:.1f} min</div>
            <div style="background-color:rgba(255,255,255,0.2); display:inline-block; padding:4px 10px; border-radius:10px; font-size:12px;">
                Meta: 25.0 min (⚠ +{avg_total-25:.1f})
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    # 2. STATUS (PIE CHART) - Legibilidade aumentada
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Status dos Laudos</div>', unsafe_allow_html=True)
    
    df_status = df['status'].value_counts().reset_index()
    df_status.columns = ['Status', 'Count']
    color_map = {'Concluído': '#17A2B8', 'Pendente': '#F1C40F', 'Refazer': '#FF5252'}
    
    fig_pie = px.pie(df_status, names='Status', values='Count', hole=0.6, color='Status', color_discrete_map=color_map)
    fig_pie.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        height=140, # Altura controlada para alinhar
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="right", x=1.1)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    # 3. GARGALOS (BARRA HORIZONTAL) - Agora tem espaço lateral
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Tempos por Etapa (Médias)</div>', unsafe_allow_html=True)
    
    etapas_df = pd.DataFrame({
        'Etapa': ['Vistoria', 'Upload', 'Validação'],
        'Tempo': [df['tempo_vistoria'].mean(), df['tempo_upload'].mean(), df['tempo_validacao'].mean()],
        'Cor': ['#17A2B8', '#A3AED0', '#2B3674']
    })
    
    fig_bar = px.bar(etapas_df, x='Tempo', y='Etapa', orientation='h', text='Tempo')
    # Aumentei o tamanho da fonte (size=14) para ficar legível
    fig_bar.update_traces(marker_color=etapas_df['Cor'], texttemplate='%{text:.1f} min', textposition='inside', textfont_size=14)
    fig_bar.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(showgrid=False, showticklabels=False, title=None),
        yaxis=dict(showgrid=False, title=None, tickfont=dict(color='#2B3674', size=12)),
        height=140, 
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# LINHA 2: HEATMAP (FULL WIDTH)
st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
st.markdown('<div class="css-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">Mapa de Calor: Ocupação dos Boxes</div>', unsafe_allow_html=True)
st.markdown('<div class="card-subtitle" style="margin-bottom:15px;">Intensidade de vistorias por Dia e Hora (Identificação de Picos)</div>', unsafe_allow_html=True)

heatmap_data = df.groupby(['dia_semana_curto', 'hora']).size().reset_index(name='qtd')
dias_ordem = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']

fig_heat = px.density_heatmap(
    heatmap_data, x='hora', y='dia_semana_curto', z='qtd', 
    category_orders={"dia_semana_curto": dias_ordem},
    color_continuous_scale=['#F4F7FE', '#17A2B8', '#004D40']
)
fig_heat.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=0, b=0, l=0, r=0),
    xaxis=dict(title="Horário", dtick=1, tickfont=dict(color='#A3AED0')),
    yaxis=dict(title=None, tickfont=dict(color='#2B3674', size=12)),
    height=300, # Altura boa para ver os detalhes
    coloraxis_showscale=False
)
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# LINHA 3: EQUIPE (4 COLUNAS)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h5 style="color:#2B3674; margin-bottom:15px;">Produtividade da Equipe</h5>', unsafe_allow_html=True)

team_stats = df.groupby('vistoriador').agg(
    total=('id_laudo', 'count'),
    tempo_medio=('tempo_total', 'mean')
).sort_values('tempo_medio', ascending=True)

cols = st.columns(4, gap="medium")
i = 0
for vistoriador, row in team_stats.iterrows():
    if i < 4:
        with cols[i]:
            cor_tempo = "#00C853" if row['tempo_medio'] < 28 else "#FF5252"
            
            # Card compactado e limpo
            html_card = f"""
            <div class="css-card" style="padding: 20px; text-align: center; border-bottom: 4px solid {cor_tempo};">
                <div style="font-weight:bold; color:#2B3674; font-size:14px; margin-bottom:5px;">{vistoriador}</div>
                <div style="display:flex; justify-content:center; align-items:baseline;">
                    <span style="font-size:26px; font-weight:800; color:{cor_tempo};">{row['tempo_medio']:.0f}</span>
                    <span style="font-size:12px; color:#A3AED0; margin-left:5px;">min/laudo</span>
                </div>
                <div style="font-size:11px; color:#A3AED0; margin-top:5px;">Total: {row['total']}</div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        i += 1
