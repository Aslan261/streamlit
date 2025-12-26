import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Painel",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURAÇÃO DE ESTILO E CORES (PADRONIZAÇÃO) ---
CORES = {
    "teal": "#17A2B8",
    "teal_dark": "#008080",
    "navy": "#2B3674",
    "grey_light": "#A3AED0",
    "grey_text": "#64748B",
    "bg_light": "#F4F7FE",
    "white": "#FFFFFF",
    "red": "#FF5252",
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
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {{
            color: {CORES['navy']} !important;
        }}
        
        /* CORREÇÃO DOS INPUTS */
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div,
        .stRadio div[role="radiogroup"] {{
            background-color: {CORES['white']} !important;
            color: {CORES['navy']} !important;
            border-color: #E0E0E0 !important;
        }}
        .stSelectbox div[data-baseweb="select"] span,
        .stMultiSelect div[data-baseweb="select"] span {{
            color: {CORES['navy']} !important;
        }}
        .stSelectbox svg, .stMultiSelect svg {{
            fill: {CORES['grey_light']} !important;
        }}

        /* TAGS DO MULTISELECT */
        span[data-baseweb="tag"] {{
            background-color: rgba(23, 162, 184, 0.15) !important;
            border: 1px solid rgba(23, 162, 184, 0.5);
        }}
        span[data-baseweb="tag"] span {{
            color: {CORES['teal']} !important;
        }}

        /* CARDS HTML (Texto) - Altura fixa 200px */
        .css-card {{
            background-color: {CORES['white']};
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.04);
            height: 200px; 
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
            height: 200px;
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
            overflow: hidden; 
        }}

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

# --- 3. DADOS (ATUALIZADO PARA SUPORTAR OPERACIONAL) ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    data = []
    vistoriadores = ['Carlos Silva', 'Ana Souza', 'Roberto Dias', 'Fernanda Lima']
    tipos_veiculo = {'Passeio': 150, 'Moto': 100, 'SUV/Van': 200, 'Caminhão': 300}
    
    for _ in range(600):
        dt = np.random.choice(dates)
        # Adicionando hora para operacional
        hora = np.random.randint(8, 18)
        dt_full = dt.replace(hour=hora, minute=np.random.randint(0, 59))
        
        tipo = np.random.choice(list(tipos_veiculo.keys()), p=[0.5, 0.2, 0.2, 0.1])
        preco = tipos_veiculo[tipo]
        
        # Simulando tempos operacionais (em minutos)
        t_vistoria = np.random.normal(20, 5)
        t_upload = np.random.normal(5, 2)
        t_validacao = np.random.normal(10, 3)
        
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'data': dt_full,
            'dia_semana': dt_full.strftime('%a'), # Seg, Ter...
            'hora': hora,
            'vistoriador': np.random.choice(vistoriadores),
            'tipo_veiculo': tipo,
            'valor': preco,
            'status': np.random.choice(['Pago', 'Pendente'], p=[0.85, 0.15]),
            # Novos campos operacionais
            'tempo_total': t_vistoria + t_upload + t_validacao,
            'etapa_gargalo': np.random.choice(['Vistoria', 'Upload', 'Validação'], p=[0.2, 0.3, 0.5])
        })
    return pd.DataFrame(data)

df = load_data()

# --- 4. FUNÇÃO AUXILIAR DE LAYOUT DE GRÁFICO ---
def aplicar_estilo_padrao(fig, titulo, height=None):
    fig.update_layout(
        title=dict(
            text=titulo.upper(),
            font=dict(size=13, color=CORES['grey_light'], family="Roboto"),
            x=0, 
            y=0.98 if height and height < 200 else 0.96
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto"),
        margin=dict(t=40, b=40, l=10, r=10),
    )
    if height:
        fig.update_layout(height=height)
        
    fig.update_xaxes(
        showgrid=False, 
        tickfont=dict(size=12, color=CORES['grey_text'])
    )
    fig.update_yaxes(
        showgrid=True, 
        gridcolor='#F0F2F6', 
        tickfont=dict(size=12, color=CORES['grey_text'])
    )
    return fig

# --- 5. SIDEBAR ---
with st.sidebar:
    c_img, c_txt = st.columns([1, 2])
    with c_img:
        st.image("https://cdn-icons-png.flaticon.com/512/2953/2953363.png", width=50)
    with c_txt:
        st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:15px;'>Painel Otimiza</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:11px; color:{CORES['grey_light']};'>Gestão Integrada</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- NOVO: NAVEGAÇÃO ---
    pagina = st.radio("Selecione o Módulo", ["Financeiro", "Operacional"], label_visibility="visible")
    
    st.markdown("---")
    st.caption("FILTROS")
    periodo = st.selectbox("Período", ["Últimos 30 Dias", "Este Mês", "Ano Atual"])
    equipe = st.multiselect("Filtrar Vistoriador", df['vistoriador'].unique(), default=df['vistoriador'].unique())

if equipe:
    df = df[df['vistoriador'].isin(equipe)]

# --- 6. RENDERIZAÇÃO CONDICIONAL DAS PÁGINAS ---

# ==============================================================================
# PÁGINA 1: FINANCEIRO (CÓDIGO ORIGINAL PRESERVADO)
# ==============================================================================
if pagina == "Financeiro":
    
    st.markdown(f"<h3 style='color:{CORES['navy']}; margin-bottom: 20px;'>Visão Financeira</h3>", unsafe_allow_html=True)

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
        # GRÁFICO DE BARRAS HORIZONTAL (STATUS)
        df_status = df['status'].value_counts().reset_index()
        df_status.columns = ['Status', 'Count']
        
        fig_status = px.bar(
            df_status, x='Count', y='Status', orientation='h', color='Status', 
            color_discrete_map={'Pago': CORES['teal'], 'Pendente': CORES['red']}, text='Count'
        )
        
        fig_status = aplicar_estilo_padrao(fig_status, "Status de Pagamento", height=200)
        fig_status.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, title=None), 
            yaxis=dict(showgrid=False, showline=False, title=None, tickfont=dict(size=12, color=CORES['grey_text'])), 
            showlegend=False,
        )
        fig_status.update_traces(textposition='inside', marker_line_width=0)
        st.plotly_chart(fig_status, use_container_width=True, config={'displayModeBar': False})


    # LINHA 2: GRÁFICO DE BARRAS CENTRAL
    st.markdown("<br>", unsafe_allow_html=True)

    df_veiculo = df.groupby('tipo_veiculo')['id_laudo'].count().reset_index().sort_values('id_laudo', ascending=False)
    fig_bar = px.bar(
        df_veiculo, x='tipo_veiculo', y='id_laudo', color='tipo_veiculo',
        color_discrete_sequence=[CORES['teal'], '#20B2AA', '#008080', '#5F9EA0']
    )

    fig_bar = aplicar_estilo_padrao(fig_bar, "Quantidade de Vistorias por Tipo de Veículo", height=320)
    fig_bar.update_layout(
        xaxis=dict(title=None, tickfont=dict(color=CORES['grey_light'], size=12)), 
        yaxis=dict(title=None, showgrid=False, gridcolor=CORES['grey_light']),
        showlegend=False,
        margin=dict(t=40, b=60, l=10, r=10)
    )
    fig_bar.update_traces(marker_line_width=0, texttemplate='%{y}', textposition='inside', cliponaxis=False)

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

# ==============================================================================
# PÁGINA 2: OPERACIONAL (NOVA SEÇÃO)
# ==============================================================================
elif pagina == "Operacional":
    
    st.markdown(f"<h3 style='color:{CORES['navy']}; margin-bottom: 20px;'>Visão Operacional (Chão de Fábrica)</h3>", unsafe_allow_html=True)
    
    # LINHA 1: KPIs OPERACIONAIS
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    
    with c1:
        # KPI: Tempo Médio de Atendimento (TMA)
        tma_medio = df['tempo_total'].mean()
        st.markdown(f"""
            <div class="css-highlight-card">
                <div style="font-size:12px; opacity:0.9; margin-bottom:5px;">TEMPO MÉDIO (TMA)</div>
                <div style="font-size:28px; font-weight:700; margin-bottom:5px;">{tma_medio:.1f} min</div>
                <div style="font-size:11px; opacity:0.8;">
                    <span style="background-color:rgba(255,255,255,0.2); padding:3px 8px; border-radius:8px;">Meta: 30 min</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        # KPI: Volume Diário Médio (Simulado)
        vol_dia = len(df) // 30
        st.markdown(f"""
            <div class="css-card">
                <div class="card-title">Volume Médio Diário</div>
                <div class="card-value">{vol_dia} <span style="font-size:16px; color:{CORES['grey_light']}">laudos</span></div>
                <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">Capacidade Instalada: {vol_dia + 5}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        # KPI: Principais Gargalos (Etapas)
        df_gargalo = df['etapa_gargalo'].value_counts().reset_index()
        df_gargalo.columns = ['Etapa', 'Ocorrencias']
        
        fig_garg = px.bar(
            df_gargalo, x='Ocorrencias', y='Etapa', orientation='h', color='Etapa',
            color_discrete_sequence=[CORES['teal'], '#2B3674', '#64748B'], text='Ocorrencias'
        )
        fig_garg = aplicar_estilo_padrao(fig_garg, "Principais Gargalos", height=200)
        fig_garg.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, title=None), 
            yaxis=dict(showgrid=False, showline=False, title=None, tickfont=dict(size=12, color=CORES['grey_text'])), 
            showlegend=False,
        )
        fig_garg.update_traces(textposition='inside', marker_line_width=0)
        st.plotly_chart(fig_garg, use_container_width=True, config={'displayModeBar': False})
        
    # LINHA 2: HEATMAP DE OCUPAÇÃO (HORA x DIA)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Agrupamento para heatmap
    df_heat = df.groupby(['hora', 'dia_semana']).size().reset_index(name='Qtd')
    # Ordem dos dias
    dias_ordem = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    fig_heat = px.density_heatmap(
        df_heat, x='hora', y='dia_semana', z='Qtd',
        color_continuous_scale=[CORES['bg_light'], CORES['teal'], CORES['navy']],
        category_orders={"dia_semana": dias_ordem}
    )
    
    fig_heat = aplicar_estilo_padrao(fig_heat, "Mapa de Calor: Horários de Pico", height=320)
    fig_heat.update_layout(
        xaxis=dict(title="Horário do Dia", tickmode='linear', dtick=1),
        yaxis=dict(title=None),
        coloraxis_showscale=False, # Remove barra de cores lateral para limpar
        margin=dict(t=40, b=40, l=10, r=10)
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
    
    # LINHA 3: RANKING DE EFICIÊNCIA (TEMPO)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<h5 style="color:{CORES["navy"]}; margin-bottom:15px; font-family:Roboto;">Ranking de Agilidade (Tempo Médio)</h5>', unsafe_allow_html=True)

    team_ops = df.groupby('vistoriador').agg(
        tempo_medio=('tempo_total', 'mean'),
        qtd=('id_laudo', 'count')
    ).sort_values('tempo_medio', ascending=True) # Menor tempo é melhor

    cols = st.columns(4, gap="medium")
    i = 0
    for vistoriador, row in team_ops.iterrows():
        if i < 4:
            with cols[i]:
                border_color = CORES['teal'] if i == 0 else "#E0E0E0" 
                html_card = f"""
                <div class="css-card" style="height:auto; padding: 20px; text-align: center; border-bottom: 4px solid {border_color};">
                    <div style="font-weight:600; color:{CORES['navy']}; font-size:14px; margin-bottom:8px;">{vistoriador}</div>
                    <div style="font-size:24px; font-weight:800; color:{CORES['teal']};">{row['tempo_medio']:.1f} min</div>
                    <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">{row['qtd']} laudos realizados</div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
            i += 1

