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

# --- 2. CSS AJUSTADO (Correção da Sidebar + Estética) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* RESET GERAL */
        .stApp {
            background-color: #F4F7FE;
            font-family: 'Roboto', sans-serif;
        }
        
        /* CORREÇÃO DA SIDEBAR:
           Removemos 'header {visibility: hidden;}' para que o botão de expandir a sidebar apareça.
           Em vez disso, escondemos apenas o rodapé e o menu hambúrguer do canto direito se quiser limpar.
        */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Ajuste do topo para não ficar com espaço branco excessivo */
        .block-container {padding-top: 2rem; padding-bottom: 5rem;}

        /* SIDEBAR (MANTENDO O VISUAL CLEAN) */
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
            # Adicionando STATUS para o gráfico de Pizza/Rosca
            'status': np.random.choice(['Concluído', 'Pendente', 'Refazer'], p=[0.75, 0.15, 0.1])
        })
    
    df = pd.DataFrame(data)
    dias_map = {'Monday': 'Seg', 'Tuesday': 'Ter', 'Wednesday': 'Qua', 'Thursday': 'Qui', 'Friday': 'Sex', 'Saturday': 'Sab', 'Sunday': 'Dom'}
    df['dia_semana_curto'] = df['dia_semana'].map(dias_map)
    return df

df = load_operational_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/9630/9630386.png", width=55)
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:16px;'>Módulo Operacional</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#A3AED0;'>Chão de Fábrica</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("FILTROS")
    periodo = st.selectbox("Turno", ["Todos", "Manhã", "Tarde"])
    equipe = st.multiselect("Vistoriadores", df['vistoriador'].unique(), default=df['vistoriador'].unique())

if equipe:
    df = df[df['vistoriador'].isin(equipe)]

# --- 5. DASHBOARD OPERACIONAL ---

col_left, col_right = st.columns([1, 2], gap="medium")

# --- COLUNA ESQUERDA ---
with col_left:
    
    # 1. CARD PRINCIPAL (TMA)
    avg_total = df['tempo_total'].mean()
    st.markdown(f"""
        <div class="css-highlight-card">
            <h3 style="font-size:14px; opacity:0.9; margin-bottom:5px; font-weight:400;">Tempo Médio Total (TMA)</h3>
            <h1 style="font-size:42px; margin:0; font-weight:700;">{avg_total:.1f} min</h1>
            <div style="margin-top:15px;">
                <span style="font-size:12px; opacity:0.8;">Meta: 25.0 min</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. NOVO: GRÁFICO DE ROSCA (PIE CHART) - STATUS
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h5 style="margin-bottom:5px;">Status das Vistorias</h5>', unsafe_allow_html=True)
    
    # Agrupando dados
    df_status = df['status'].value_counts().reset_index()
    df_status.columns = ['Status', 'Count']
    
    # Cores personalizadas para combinar com o tema
    color_map = {
        'Concluído': '#17A2B8',  # Teal (Sucesso)
        'Pendente': '#F1C40F',   # Amarelo (Atenção)
        'Refazer': '#FF5252'     # Vermelho (Erro)
    }
    
    fig_pie = px.pie(
        df_status, 
        names='Status', 
        values='Count', 
        hole=0.6, # Transforma Pizza em Rosca (Donut)
        color='Status',
        color_discrete_map=color_map
    )
    
    fig_pie.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=10, b=10, l=10, r=10),
        height=220,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. GARGALOS (Barras)
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h5 style="margin-bottom:15px;">Tempo por Etapa (Gargalos)</h5>', unsafe_allow_html=True)
    
    etapas_df = pd.DataFrame({
        'Etapa': ['Vistoria Física', 'Upload Fotos', 'Validação'],
        'Tempo': [df['tempo_vistoria'].mean(), df['tempo_upload'].mean(), df['tempo_validacao'].mean()],
        'Cor': ['#17A2B8', '#A3AED0', '#2B3674']
    })
    
    fig_bar = px.bar(etapas_df, x='Tempo', y='Etapa', orientation='h', text='Tempo')
    fig_bar.update_traces(marker_color=etapas_df['Cor'], texttemplate='%{text:.1f} m', textposition='inside')
    fig_bar.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=0, b=0, l=0, r=0),
        xaxis=dict(showgrid=False, showticklabels=False, title=None),
        yaxis=dict(showgrid=False, title=None, tickfont=dict(color='#2B3674', size=12)),
        height=180, showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- COLUNA DIREITA ---
with col_right:
    
    # 4. MAPA DE CALOR
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-bottom:5px;">Ocupação dos Boxes (Heatmap)</h4>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px; color:#A3AED0; margin-bottom:15px;">Intensidade por Dia e Hora</p>', unsafe_allow_html=True)
    
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
        height=350, coloraxis_showscale=False
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. RANKING DE EFICIÊNCIA
    st.markdown('<h5 style="margin-top:10px;">Produtividade da Equipe</h5>', unsafe_allow_html=True)
    
    team_stats = df.groupby('vistoriador').agg(
        total=('id_laudo', 'count'),
        tempo_medio=('tempo_total', 'mean')
    ).sort_values('tempo_medio', ascending=True)

    cols = st.columns(4)
    i = 0
    for vistoriador, row in team_stats.iterrows():
        if i < 4:
            with cols[i]:
                cor_tempo = "#00C853" if row['tempo_medio'] < 28 else "#FF5252"
                html_card = f"""
                <div class="css-card" style="padding: 15px; text-align: center;">
                    <div style="font-weight:bold; color:#2B3674; font-size:13px; margin-bottom:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{vistoriador}</div>
                    <div style="display:flex; justify-content:center; align-items:baseline; margin-bottom:5px;">
                        <span style="font-size:22px; font-weight:800; color:{cor_tempo};">{row['tempo_medio']:.0f}</span>
                        <span style="font-size:11px; color:#A3AED0; margin-left:3px;">min</span>
                    </div>
                    <div style="font-size:10px; color:#A3AED0; background-color:#F4F7FE; padding:4px; border-radius:8px;">
                        {row['total']} laudos
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
            i += 1
