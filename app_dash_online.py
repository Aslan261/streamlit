import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Painel Inteligência",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONFIGURAÇÃO DE ESTILO E CORES ---
CORES = {
    "teal": "#17A2B8",
    "teal_dark": "#008080",
    "navy": "#2B3674",
    "grey_light": "#A3AED0",
    "grey_text": "#64748B",
    "bg_light": "#F4F7FE",
    "white": "#FFFFFF",
    "red": "#FF5252",
    "orange": "#FFB74D",
    "green": "#00C853"
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
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
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

        /* TAGS */
        span[data-baseweb="tag"] {{
            background-color: rgba(23, 162, 184, 0.15) !important;
            border: 1px solid rgba(23, 162, 184, 0.5);
        }}
        span[data-baseweb="tag"] span {{
            color: {CORES['teal']} !important;
        }}

        /* CARDS */
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
        
        /* ESTILIZAÇÃO DOS GRÁFICOS */
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

# --- 3. DADOS (ENRIQUECIDOS COM INTELEGÊNCIA COMERCIAL) ---
@st.cache_data
def load_data():
    np.random.seed(42)
    # Gerando dados mais espalhados no tempo para simular vencimentos futuros
    dates = [datetime.now() - timedelta(days=x) for x in range(365)] 
    data = []
    vistoriadores = ['Carlos Silva', 'Ana Souza', 'Roberto Dias', 'Fernanda Lima']
    tipos_veiculo = {'Passeio': 150, 'Moto': 100, 'SUV/Van': 200, 'Caminhão': 300}
    bairros = ['Centro', 'Zona Industrial', 'Jd. América', 'Porto', 'Aeroporto', 'Vila Nova']
    
    # Clientes Fictícios para o CRM
    clientes = ['Transp. Express', 'Logística 2000', 'Frota Segura', 'Localiza Vans', 'Auto Center Silva', 'Particular']

    for _ in range(800):
        dt = np.random.choice(dates)
        hora = np.random.randint(8, 18)
        dt_full = dt.replace(hour=hora, minute=np.random.randint(0, 59))
        
        # Simula data de vencimento (1 ano após a vistoria)
        dt_vencimento = dt_full + timedelta(days=365)
        
        tipo = np.random.choice(list(tipos_veiculo.keys()), p=[0.5, 0.2, 0.2, 0.1])
        preco = tipos_veiculo[tipo]
        cliente = np.random.choice(clientes, p=[0.2, 0.2, 0.2, 0.1, 0.1, 0.2])
        
        t_vistoria = np.random.normal(20, 5)
        t_upload = np.random.normal(5, 2)
        t_validacao = np.random.normal(10, 3)
        
        data.append({
            'id_laudo': np.random.randint(10000, 99999),
            'cliente_nome': cliente,
            'data': dt_full, 
            'data_vencimento': dt_vencimento,
            'mes_vencimento': dt_vencimento.strftime('%m/%Y'),
            'dia_str': dt_full.strftime('%d/%m'),
            'dia_semana': dt_full.strftime('%a'),
            'hora': hora,
            'vistoriador': np.random.choice(vistoriadores),
            'tipo_veiculo': tipo,
            'valor': preco,
            'bairro': np.random.choice(bairros),
            'status': np.random.choice(['Pago', 'Pendente'], p=[0.85, 0.15]),
            'tempo_total': t_vistoria + t_upload + t_validacao,
            'etapa_gargalo': np.random.choice(['Vistoria', 'Upload', 'Validação'], p=[0.2, 0.3, 0.5]),
            'probabilidade_fechamento': np.random.uniform(0.4, 0.99) # Para o CRM
        })
    return pd.DataFrame(data).sort_values('data')

df = load_data()

# --- 4. FUNÇÃO AUXILIAR DE LAYOUT ---
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
        st.markdown(f"<div style='font-size:11px; color:{CORES['grey_light']};'>Gestão Inteligente</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # NAVEGAÇÃO
    pagina = st.radio("Selecione o Módulo", ["Financeiro", "Operacional", "Comercial"], label_visibility="visible")
    
    st.markdown("---")
    st.markdown(f"<div style='font-size:12px; font-weight:bold; color:{CORES['navy']}; margin-bottom:10px;'>FILTROS GERAIS</div>", unsafe_allow_html=True)
    
    periodo = st.selectbox("Período", ["Próximos 30 Dias (Previsão)", "Este Mês", "Ano Atual"])
    equipe = st.multiselect("Vistoriador", df['vistoriador'].unique(), default=[])
    f_veiculo = st.multiselect("Tipo de Veículo", df['tipo_veiculo'].unique(), default=[])

# Lógica de Filtro Básica
if equipe:
    df = df[df['vistoriador'].isin(equipe)]
if f_veiculo:
    df = df[df['tipo_veiculo'].isin(f_veiculo)]

# --- 6. RENDERIZAÇÃO DAS PÁGINAS ---

# ==============================================================================
# PÁGINA 1: FINANCEIRO
# ==============================================================================
if pagina == "Financeiro":
    st.markdown(f"<h3 style='color:{CORES['navy']}; margin-bottom: 20px;'>Visão Financeira</h3>", unsafe_allow_html=True)
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
        df_status = df['status'].value_counts().reset_index()
        df_status.columns = ['Status', 'Count']
        fig_status = px.bar(
            df_status, x='Count', y='Status', orientation='h', color='Status', 
            color_discrete_map={'Pago': CORES['teal'], 'Pendente': CORES['red']}, text='Count'
        )
        fig_status = aplicar_estilo_padrao(fig_status, "Status de Pagamento", height=200)
        fig_status.update_layout(xaxis=dict(showgrid=False, showticklabels=False, title=None), yaxis=dict(showgrid=False, showline=False, title=None, tickfont=dict(size=12, color=CORES['grey_text'])), showlegend=False)
        fig_status.update_traces(textposition='inside', marker_line_width=0)
        st.plotly_chart(fig_status, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    df_veiculo = df.groupby('tipo_veiculo')['id_laudo'].count().reset_index().sort_values('id_laudo', ascending=False)
    fig_bar = px.bar(df_veiculo, x='tipo_veiculo', y='id_laudo', color='tipo_veiculo', color_discrete_sequence=[CORES['teal'], '#20B2AA', '#008080', '#5F9EA0'])
    fig_bar = aplicar_estilo_padrao(fig_bar, "Quantidade de Vistorias por Tipo de Veículo", height=320)
    fig_bar.update_layout(xaxis=dict(title=None, tickfont=dict(color=CORES['grey_light'], size=12)), yaxis=dict(title=None, showgrid=False, gridcolor=CORES['grey_light']), showlegend=False, margin=dict(t=40, b=60, l=10, r=10))
    fig_bar.update_traces(marker_line_width=0, texttemplate='%{y}', textposition='outside', cliponaxis=False)
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<h5 style="color:{CORES["navy"]}; margin-bottom:15px; font-family:Roboto;">Receita Gerada por Vistoriador</h5>', unsafe_allow_html=True)
    team_finance = df.groupby('vistoriador').agg(total_receita=('valor', 'sum'), qtd=('id_laudo', 'count')).sort_values('total_receita', ascending=False)
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
# PÁGINA 2: OPERACIONAL
# ==============================================================================
elif pagina == "Operacional":
    st.markdown(f"<h3 style='color:{CORES['navy']}; margin-bottom: 20px;'>Visão Operacional</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    with c1:
        tma = df['tempo_total'].mean()
        st.markdown(f"""
            <div class="css-highlight-card">
                <div style="font-size:12px; opacity:0.9; margin-bottom:5px;">TEMPO MÉDIO (TMA)</div>
                <div style="font-size:28px; font-weight:700; margin-bottom:5px;">{tma:.1f} min</div>
                <div style="font-size:11px; opacity:0.8;">
                    <span style="background-color:rgba(255,255,255,0.2); padding:3px 8px; border-radius:8px;">Meta: 30 min</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        vol_dia = len(df) // 30
        st.markdown(f"""
            <div class="css-card">
                <div class="card-title">Volume Médio Diário</div>
                <div class="card-value">{vol_dia} <span style="font-size:16px; color:{CORES['grey_light']}">laudos</span></div>
                <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">Capacidade Instalada: {vol_dia + 5}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        df_gargalo = df['etapa_gargalo'].value_counts().reset_index()
        df_gargalo.columns = ['Etapa', 'Ocorrencias']
        fig_garg = px.bar(df_gargalo, x='Ocorrencias', y='Etapa', orientation='h', color='Etapa', color_discrete_sequence=[CORES['teal'], '#2B3674', '#64748B'], text='Ocorrencias')
        fig_garg = aplicar_estilo_padrao(fig_garg, "Principais Gargalos", height=200)
        fig_garg.update_layout(xaxis=dict(showgrid=False, showticklabels=False, title=None), yaxis=dict(showgrid=False, showline=False, title=None, tickfont=dict(size=12, color=CORES['grey_text'])), showlegend=False)
        fig_garg.update_traces(textposition='inside', marker_line_width=0)
        st.plotly_chart(fig_garg, use_container_width=True, config={'displayModeBar': False})
        
    st.markdown("<br>", unsafe_allow_html=True)
    df_heat = df.groupby(['hora', 'dia_semana']).size().reset_index(name='Qtd')
    dias_ordem = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    fig_heat = px.density_heatmap(df_heat, x='hora', y='dia_semana', z='Qtd', color_continuous_scale=[CORES['bg_light'], CORES['teal'], CORES['navy']], category_orders={"dia_semana": dias_ordem})
    fig_heat = aplicar_estilo_padrao(fig_heat, "Mapa de Calor: Horários de Pico", height=320)
    fig_heat.update_layout(xaxis=dict(title="Horário do Dia", tickmode='linear', dtick=1), yaxis=dict(title=None), coloraxis_showscale=False, margin=dict(t=40, b=40, l=10, r=10))
    st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<h5 style="color:{CORES["navy"]}; margin-bottom:15px; font-family:Roboto;">Ranking de Agilidade (Tempo Médio)</h5>', unsafe_allow_html=True)
    team_ops = df.groupby('vistoriador').agg(tempo_medio=('tempo_total', 'mean'), qtd=('id_laudo', 'count')).sort_values('tempo_medio', ascending=True)
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

# ==============================================================================
# PÁGINA 3: COMERCIAL (NOVA - INTELLIGENCE)
# ==============================================================================
elif pagina == "Comercial":
    
    st.markdown(f"<h3 style='color:{CORES['navy']}; margin-bottom: 20px;'>Inteligência Comercial & Oportunidades</h3>", unsafe_allow_html=True)
    
    # Filtrando dados para o futuro (Vencimentos)
    hoje = datetime.now()
    proximos_30_dias = hoje + timedelta(days=30)
    
    # DataFrame de Vencimentos Futuros
    df_vencimentos = df[(df['data_vencimento'] >= hoje) & (df['data_vencimento'] <= proximos_30_dias)]
    
    # KPIs DE INTELIGÊNCIA
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    
    with c1:
        # Potencial de Renovação (R$)
        potencial_renovacao = df_vencimentos['valor'].sum()
        st.markdown(f"""
            <div class="css-highlight-card">
                <div style="font-size:12px; opacity:0.9; margin-bottom:5px;">POTENCIAL DE RENOVAÇÃO (30 DIAS)</div>
                <div style="font-size:28px; font-weight:700; margin-bottom:5px;">R$ {potencial_renovacao:,.2f}</div>
                <div style="font-size:11px; opacity:0.8;">
                    <span style="background-color:rgba(255,255,255,0.2); padding:3px 8px; border-radius:8px;">🎯 {len(df_vencimentos)} clientes a vencer</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        # Leads Qualificados (Simulado: Probabilidade > 70%)
        leads_quentes = len(df_vencimentos[df_vencimentos['probabilidade_fechamento'] > 0.7])
        st.markdown(f"""
            <div class="css-card">
                <div class="card-title">Leads Prioritários</div>
                <div class="card-value">{leads_quentes} <span style="font-size:16px; color:{CORES['grey_light']}">clientes</span></div>
                <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">Alta probabilidade de renovação</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        # Onde vender (Principal Bairro)
        top_bairro = df['bairro'].mode()[0]
        st.markdown(f"""
            <div class="css-card">
                <div class="card-title">Região Mais Aquecida</div>
                <div class="card-value" style="font-size:24px;">{top_bairro}</div>
                <div style="font-size:11px; color:{CORES['grey_light']}; margin-top:5px;">Maior concentração de vistorias</div>
            </div>
        """, unsafe_allow_html=True)

    # LINHA 2: INTELLIGENCE CHARTS (CRONOGRAMA E MAPA)
    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_right = st.columns([2, 1], gap="medium")
    
    with c_left:
        # CRONOGRAMA DE VENCIMENTOS (QUEM/QUANDO)
        # Agrupando vencimentos futuros por mês
        df_futuro = df[df['data_vencimento'] > hoje].copy()
        df_futuro['mes_ano'] = df_futuro['data_vencimento'].dt.strftime('%Y-%m')
        df_timeline = df_futuro.groupby('mes_ano')['valor'].sum().reset_index().sort_values('mes_ano').head(6) # Próximos 6 meses
        
        fig_timeline = px.bar(
            df_timeline, x='mes_ano', y='valor', 
            text='valor', color='valor',
            color_continuous_scale=[CORES['teal'], CORES['navy']]
        )
        fig_timeline = aplicar_estilo_padrao(fig_timeline, "Cronograma de Receita Futura (Vencimentos)", height=320)
        fig_timeline.update_layout(
            xaxis=dict(title="Mês de Vencimento", tickfont=dict(size=11)),
            yaxis=dict(showgrid=True),
            coloraxis_showscale=False,
            margin=dict(t=40, b=40, l=10, r=10)
        )
        fig_timeline.update_traces(texttemplate='R$ %{y:.2s}', textposition='outside', cliponaxis=False)
        st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})
        
    with c_right:
        # ONDE VENDER (BAIRROS)
        df_geo = df.groupby('bairro')['id_laudo'].count().reset_index().sort_values('id_laudo', ascending=True)
        
        fig_geo = px.bar(
            df_geo, x='id_laudo', y='bairro', orientation='h',
            text='id_laudo',
            color_discrete_sequence=[CORES['teal']]
        )
        fig_geo = aplicar_estilo_padrao(fig_geo, "Oportunidades por Região", height=320)
        fig_geo.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, title=None),
            yaxis=dict(title=None, tickfont=dict(size=11)),
            margin=dict(t=40, b=20, l=10, r=10)
        )
        fig_geo.update_traces(textposition='inside')
        st.plotly_chart(fig_geo, use_container_width=True, config={'displayModeBar': False})

    # LINHA 3: LISTA DE AÇÃO (CRM - QUEM LIGAR HOJE)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<h5 style="color:{CORES["navy"]}; margin-bottom:15px; font-family:Roboto;">Lista de Ação Prioritária (Vencimentos Próximos)</h5>', unsafe_allow_html=True)
    
    # Tabela estilizada
    df_crm = df_vencimentos[['cliente_nome', 'data_vencimento', 'valor', 'tipo_veiculo', 'probabilidade_fechamento']].sort_values('data_vencimento').head(5)
    
    # Formatando para exibição
    df_crm['Vencimento'] = df_crm['data_vencimento'].dt.strftime('%d/%m/%Y')
    df_crm['Valor Estimado'] = df_crm['valor'].apply(lambda x: f"R$ {x:,.2f}")
    df_crm['Score'] = (df_crm['probabilidade_fechamento'] * 100).astype(int).astype(str) + "%"
    
    # Exibindo como cartões horizontais para manter o design system (em vez de tabela padrão)
    for index, row in df_crm.iterrows():
        # Cor da borda baseada no Score (Probabilidade)
        prob = row['probabilidade_fechamento']
        border = CORES['green'] if prob > 0.8 else (CORES['orange'] if prob > 0.5 else CORES['red'])
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 5px solid {border}; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
            <div style="width: 25%;">
                <div style="font-size: 11px; color: {CORES['grey_light']};">CLIENTE</div>
                <div style="font-weight: 600; color: {CORES['navy']};">{row['cliente_nome']}</div>
            </div>
            <div style="width: 20%;">
                <div style="font-size: 11px; color: {CORES['grey_light']};">VENCIMENTO</div>
                <div style="color: {CORES['red']}; font-weight: bold;">{row['Vencimento']}</div>
            </div>
            <div style="width: 20%;">
                <div style="font-size: 11px; color: {CORES['grey_light']};">VEÍCULO</div>
                <div style="color: {CORES['grey_text']};">{row['tipo_veiculo']}</div>
            </div>
            <div style="width: 20%;">
                <div style="font-size: 11px; color: {CORES['grey_light']};">VALOR</div>
                <div style="color: {CORES['teal']}; font-weight: bold;">{row['Valor Estimado']}</div>
            </div>
            <div style="width: 15%; text-align: right;">
                <span style="background-color: {CORES['bg_light']}; color: {CORES['navy']}; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold;">Score {row['Score']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
