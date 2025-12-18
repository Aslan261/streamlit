import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Otimiza Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILIZAÇÃO CSS (A MÁGICA ACONTECE AQUI) ---
# Aqui definimos as cores da imagem de referência:
# Teal Principal: #17A2B8 (ou variante mais suave)
# Fundo: #F4F6F9
# Cards: #FFFFFF com sombra suave
st.markdown("""
    <style>
        /* Importando fonte Google (opcional, deixa mais moderno) */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        /* Fundo Geral */
        .stApp {
            background-color: #F4F6F9;
            font-family: 'Roboto', sans-serif;
        }

        /* Remover padding excessivo do topo */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        /* Estilo dos Cards (Caixas Brancas) */
        .css-card {
            border-radius: 15px;
            padding: 20px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }

        /* Card de Destaque (Teal - Total Balance style) */
        .css-highlight-card {
            border-radius: 15px;
            padding: 20px;
            background: linear-gradient(135deg, #20B2AA 0%, #008080 100%);
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        
        .css-highlight-card h3 {
            color: white !important;
            font-size: 1rem;
            font-weight: 300;
            margin: 0;
        }
        
        .css-highlight-card h1 {
            color: white !important;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
        }

        /* Métricas pequenas */
        .metric-label {
            font-size: 0.8rem;
            color: #6c757d;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2c3e50;
        }

        /* Ajuste da Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. DADOS (Mantidos do anterior) ---
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

# --- 4. SIDEBAR (Perfil do Usuário) ---
with st.sidebar:
    # Simulando o perfil "Hue Brew" da imagem
    col_perfil_1, col_perfil_2 = st.columns([1, 3])
    with col_perfil_1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    with col_perfil_2:
        st.markdown("**Gestor Otimiza**<br><span style='color:grey; font-size:0.8em'>Admin</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Menu")
    st.button("📊 Dashboard Geral", use_container_width=True)
    st.button("💰 Financeiro", use_container_width=True)
    st.button("👥 Equipe", use_container_width=True)
    st.button("⚙️ Configurações", use_container_width=True)

    # Filtro Rápido
    st.markdown("---")
    st.markdown("### Filtros")
    vistoriador_sel = st.multiselect("Vistoriador", df['vistoriador'].unique())

# Filtragem
if vistoriador_sel:
    df = df[df['vistoriador'].isin(vistoriador_sel)]

# --- 5. LAYOUT PRINCIPAL (GRID) ---

# Título discreto
st.markdown("## Visão Geral da Operação")

# --- LINHA SUPERIOR (BIG NUMBERS + GRÁFICO PRINCIPAL) ---
col_left, col_right = st.columns([1, 2])

with col_left:
    # CARTÃO DE DESTAQUE (Imitando o cartão Verde/Teal da imagem)
    faturamento_total = df['valor'].sum()
    st.markdown(f"""
        <div class="css-highlight-card">
            <h3>Faturamento Acumulado</h3>
            <h1>R$ {faturamento_total:,.2f}</h1>
            <p style="margin-top:10px; font-size:0.9rem">
                <span style="background-color:rgba(255,255,255,0.2); padding:2px 8px; border-radius:10px">
                +12% vs mês anterior
                </span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # LISTA DE "ÚLTIMAS TRANSAÇÕES" (Imitando a lista "Income" da imagem)
    st.markdown('<div class="css-card"><h5>Últimas Vistorias</h5>', unsafe_allow_html=True)
    
    recentes = df.tail(4).sort_values('data', ascending=False)
    for index, row in recentes.iterrows():
        # Ícone condicional
        icon = "✅" if row['resultado'] == 'Aprovado' else "⚠️"
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; margin-bottom:10px; border-bottom:1px solid #eee; padding-bottom:5px">
                <div>
                    <span style="font-size:1.2rem; margin-right:10px">{icon}</span>
                    <b>{row['vistoriador']}</b><br>
                    <span style="color:grey; font-size:0.8rem">Laudo #{row['id_laudo']} • {row['dia_str']}</span>
                </div>
                <div style="text-align:right">
                    <span style="color:#20B2AA; font-weight:bold">+ R$ {row['valor']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # GRÁFICO PRINCIPAL (Imitando o gráfico de área da imagem)
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("Volume Diário de Laudos")
    
    df_day = df.groupby('dia_str')['id_laudo'].count().reset_index()
    
    # Gráfico de Área com gradiente (estilo moderno)
    fig = px.area(df_day, x='dia_str', y='id_laudo', 
                  color_discrete_sequence=['#20B2AA']) # Cor Teal
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None),
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # LINHA INTERMEDIÁRIA (Pequenos Cards de Métricas)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="css-card" style="text-align:center">
                <span class="metric-label">Ticket Médio</span><br>
                <span class="metric-value">R$ {df['valor'].mean():.2f}</span>
                <span style="color:green; font-size:0.8rem">↗</span>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        reprovados = len(df[df['resultado'] == 'Reprovado'])
        st.markdown(f"""
            <div class="css-card" style="text-align:center">
                <span class="metric-label">Reprovações</span><br>
                <span class="metric-value">{reprovados}</span>
                <span style="color:red; font-size:0.8rem">↘ Atenção</span>
            </div>
        """, unsafe_allow_html=True)

# --- LINHA INFERIOR (CARDS HORIZONTAIS - Imitando "Investments") ---
st.markdown("### Performance por Vistoriador")

cols = st.columns(4)
stats_vistoriador = df.groupby('vistoriador')['id_laudo'].count().sort_values(ascending=False)

# Criando cards dinâmicos para cada vistoriador
i = 0
for vistoriador, qtd in stats_vistoriador.items():
    if i < 4: # Limite de 4 cards
        with cols[i]:
            st.markdown(f"""
                <div class="css-card" style="text-align:center; border-top: 5px solid #20B2AA">
                    <h4>{vistoriador}</h4>
                    <h2 style="color:#20B2AA">{qtd}</h2>
                    <p style="color:grey; font-size:0.8rem">Laudos realizados</p>
                    <button style="background-color:#E0F7FA; border:none; color:#006064; padding:5px 10px; border-radius:5px; cursor:pointer">Ver Detalhes</button>
                </div>
            """, unsafe_allow_html=True)
        i += 1
