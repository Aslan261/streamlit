import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import re
from datetime import datetime
import math
import random

# Tenta importar a nova biblioteca do Google Gen AI
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# Configuração da Página
st.set_page_config(page_title="A Bíblia é o seu caminho", layout="wide", page_icon="📖")

# =========================================================
# 0. ESTILIZAÇÃO (CSS PERSONALIZADO)
# =========================================================
# Aplicando a paleta de cores solicitada
st.markdown("""
<style>
    /* VARIÁVEIS DE COR */
    :root {
        --primary-100: #1e295a; /* Azul Profundo */
        --primary-200: #4c5187; /* Azul Médio */
        --primary-300: #abacea; /* Azul Claro */
        --accent-100: #F18F01;  /* Laranja Vivo */
        --accent-200: #833500;  /* Laranja Escuro/Marrom */
        --text-100: #353535;    /* Cinza Escuro (Texto Principal) */
        --text-200: #5f5f5f;    /* Cinza Médio */
        --bg-100: #F5ECD7;      /* Creme Claro (Fundo App) */
        --bg-200: #ebe2cd;      /* Creme Médio */
        --bg-300: #c2baa6;      /* Bege Escuro */
    }

    /* FUNDO GERAL */
    .stApp {
        background-color: var(--bg-100);
        color: var(--text-100);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: var(--primary-100);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: var(--bg-100) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: var(--primary-300) !important;
    }
    /* Separador na sidebar */
    [data-testid="stSidebar"] hr {
        border-color: var(--primary-200) !important;
    }
    
    /* RADIO BUTTONS (MENU) */
    /* Estilizando a seleção do menu para parecer 'ativo' */
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        background-color: transparent;
        color: var(--primary-300);
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 5px;
        transition: all 0.3s;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: var(--primary-200);
        color: white;
    }
    /* Quando selecionado (Infelizmente o Streamlit não expõe classe fácil para 'checked' no CSS puro, 
       mas o estilo padrão do Streamlit já destaca. Vamos focar em tipografia) */

    /* CABEÇALHOS */
    h1, h2, h3 {
        color: var(--primary-100) !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    h1 {
        border-bottom: 2px solid var(--accent-100);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* CARDS DE MÉTRICAS */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        border-left: 5px solid var(--accent-100);
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-200) !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--primary-100) !important;
        font-size: 1.8rem !important;
    }

    /* BOTÕES */
    .stButton > button {
        background-color: var(--accent-100);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: var(--accent-200);
        color: white;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stButton > button:focus {
        border-color: var(--accent-200);
        color: white;
    }

    /* INPUTS E SELECTBOXES */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: white;
        color: var(--text-100);
        border-radius: 5px;
        border: 1px solid var(--bg-300);
    }

    /* TABELAS (DATAFRAME) */
    [data-testid="stDataFrame"] {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
    }

    /* EXPANSORES E TABS */
    .stExpander {
        background-color: white;
        border-radius: 10px;
        border: 1px solid var(--bg-300);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-200);
        border-radius: 5px 5px 0 0;
        color: var(--text-100);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-100) !important;
        color: white !important;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 1. FUNÇÕES DE CARREGAMENTO E PROCESSAMENTO
# =========================================================

@st.cache_data
def load_data(file):
    try:
        # Tenta ler como CSV padrão ou com separadores diferentes caso o usuário mude o formato
        df = pd.read_csv(file)
        # Normalização de nomes de colunas para garantir compatibilidade
        cols_map = {
            'Book Name': 'Livro', 
            'Book Number': 'Livro_ID', 
            'Chapter': 'Capitulo', 
            'Verse': 'Versiculo', 
            'Text': 'Texto', 
            'Verse ID': 'ID_Global'
        }
        df.rename(columns=cols_map, inplace=True, errors='ignore')
        
        # Garante que colunas essenciais existam
        required_cols = ['Livro', 'Capitulo', 'Versiculo', 'Texto']
        if not all(col in df.columns for col in required_cols):
            st.error(f"O arquivo deve conter as colunas: {required_cols}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

# Lista básica de stopwords e personagens para ajudar na extração simples
STOPWORDS_PT = set([
    'a', 'o', 'as', 'os', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 
    'nos', 'nas', 'por', 'pelo', 'pela', 'para', 'que', 'e', 'é', 'era', 
    'foi', 'com', 'sem', 'seu', 'sua', 'seus', 'suas', 'ele', 'ela', 'eles', 
    'elas', 'mas', 'ou', 'quando', 'como', 'onde', 'quem', 'porque', 'se', 
    'eu', 'tu', 'nós', 'vós', 'me', 'te', 'lhe', 'nos', 'vos', 'lhes', 
    'mim', 'ti', 'si', 'este', 'esta', 'isto', 'esse', 'essa', 'isso', 
    'aquele', 'aquela', 'aquilo', 'meu', 'teu', 'nosso', 'vosso', 'tua', 
    'minha', 'nossa', 'vossa', 'senhor', 'deus', 'jesus', 'cristo', 'não',
    'eis', 'quis', 'então', 'amém', 'segunda'
])

# Lista de principais figuras bíblicas para priorizar na busca
BIG_ENTITIES = [
    'Deus', 'Jesus', 'Senhor', 'Espírito', 'Moisés', 'Arão', 'Faraó', 'Josué', 
    'Davi', 'Saul', 'Salomão', 'Elias', 'Eliseu', 'Isaías', 'Jeremias', 'Ezequiel', 
    'Daniel', 'Pedro', 'Paulo', 'João', 'Tiago', 'Maria', 'José', 'Abraão', 
    'Isaque', 'Jacó', 'José', 'Judá', 'Pilatos', 'Herodes', 'Judas', 'Timóteo',
    'Barnabé', 'Silas', 'Tito', 'Noé', 'Adão', 'Eva', 'Caim', 'Abel', 'Golias',
    'Jonas', 'Jó', 'Samuel', 'Absalão', 'Nabucodonosor', 'Calebe'
]

def simple_entity_extractor(text):
    if not isinstance(text, str):
        return []
    clean_text = re.sub(r'[^\w\s]', '', text)
    words = clean_text.split()
    entities = []
    for i, word in enumerate(words):
        if word in BIG_ENTITIES:
            entities.append(word)
            continue
        if i > 0 and word[0].isupper() and word.lower() not in STOPWORDS_PT:
            if len(word) > 2:
                entities.append(word)
    return list(set(entities))

@st.cache_data
def process_entities(df):
    df['Entidades'] = df['Texto'].apply(simple_entity_extractor)
    return df

@st.cache_data
def generate_reading_plan(df):
    if 'Livro_ID' in df.columns:
        chapters = df[['Livro_ID', 'Livro', 'Capitulo']].drop_duplicates().sort_values(['Livro_ID', 'Capitulo'])
    else:
        chapters = df[['Livro', 'Capitulo']].drop_duplicates()
        
    chapters_list = chapters[['Livro', 'Capitulo']].values.tolist()
    total_chapters = len(chapters_list)
    
    random.seed(42)
    random.shuffle(chapters_list)
    
    plan = {}
    chunk_size = total_chapters / 365
    
    current_idx = 0
    for day in range(1, 366):
        end_idx = int(day * chunk_size)
        daily_chapters = chapters_list[current_idx:end_idx]
        plan[day] = daily_chapters
        current_idx = end_idx
        
    return plan, total_chapters

# Função auxiliar para aplicar tema aos gráficos Plotly
def apply_theme_to_plot(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Transparente para usar o fundo do app
        plot_bgcolor='rgba(255,255,255,0.5)', # Fundo do gráfico semi-transparente
        font_color='#353535',
        title_font_color='#1e295a',
        colorway=['#1e295a', '#F18F01', '#4c5187', '#abacea', '#833500'], # Cores do tema nas séries
    )
    return fig

# =========================================================
# 2. INTERFACE E NAVEGAÇÃO
# =========================================================

# Sidebar customizada com emojis e estilo
st.sidebar.markdown("# ✝️ Seu Aplicativo Bíblico")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📥 Carregar Dados")
uploaded_file = st.sidebar.file_uploader("Arquivo CSV/Excel", type=['csv', 'xlsx'], label_visibility="collapsed")

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = load_data(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        cols_map = {'Book Name': 'Livro', 'Book Number': 'Livro_ID', 'Chapter': 'Capitulo', 'Verse': 'Versiculo', 'Text': 'Texto', 'Verse ID': 'ID_Global'}
        df.rename(columns=cols_map, inplace=True, errors='ignore')

    if df is not None:
        with st.spinner('Processando dados...'):
            if 'Entidades' not in df.columns:
                df = process_entities(df)
            
        st.sidebar.success(f"Carregado: {len(df)} versículos")
        st.sidebar.markdown("---")
        
        # Menu Principal com ícones para visual mais interessante
        menu = st.sidebar.radio("Navegação", [
            "🙏 Devocional Diário",
            "📊 Visão Geral", 
            "👥 Análise de Entidades", 
            "🕸️ Redes de Conexão (SNA)", 
            "🔍 Explorador de Texto",
            "🤖 Assistente de Estudo IA"
        ])
        
        api_key = ""
        if menu in ["🤖 Assistente de Estudo IA", "🙏 Devocional Diário"]:
            if HAS_GENAI:
                st.sidebar.markdown("---")
                st.sidebar.markdown("### 🔑 Configuração IA")
                api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Chave do Google AI Studio")

        # --- CONTEÚDO PRINCIPAL ---

        # ---------------------------------------------------------
        # DEVOCIONAL
        # ---------------------------------------------------------
        if menu == "🙏 Devocional Diário":
            st.title("Devocional Anual")
            st.markdown("*Uma jornada aleatória e inspiradora através das escrituras.*")
            
            plan, total_chapters = generate_reading_plan(df)
            
            # Card de controle com cor de fundo branca para destaque
            with st.container():
                col_date, col_nav = st.columns([1, 2])
                with col_date:
                    today = datetime.now()
                    selected_date = st.date_input("📅 Selecione a Data", today)
                    day_of_year = selected_date.timetuple().tm_yday
                    if day_of_year > 365: day_of_year = 365
                
                with col_nav:
                    st.markdown(f"**Progresso do Ano (Dia {day_of_year}/365)**")
                    progress = day_of_year / 365
                    st.progress(progress)
            
            st.divider()

            todays_chapters = plan.get(day_of_year, [])

            if not todays_chapters:
                st.info("Nenhuma leitura programada.")
            else:
                reading_refs = []
                for book, chap in todays_chapters:
                    reading_refs.append(f"{book} {chap}")
                
                if len(reading_refs) > 3:
                    reading_title = ", ".join(reading_refs[:3]) + f" e mais {len(reading_refs)-3}"
                else:
                    reading_title = ", ".join(reading_refs)
                
                st.subheader(f"📖 Leitura de Hoje: {reading_title}")
                
                tab_texto, tab_reflexao = st.tabs(["Texto Bíblico", "Reflexão IA"])
                
                full_text_devocional = ""
                
                with tab_texto:
                    for book, chap in todays_chapters:
                        st.markdown(f"#### {book} {chap}")
                        subset = df[(df['Livro'] == book) & (df['Capitulo'] == chap)]
                        text_content = ""
                        # Usando expander para não poluir se for muito longo
                        with st.expander(f"Ler {book} {chap}", expanded=True):
                            for _, row in subset.iterrows():
                                vers = row['Versiculo']
                                txt = row['Texto']
                                text_content += f"{vers}. {txt} "
                                st.markdown(f"<small><b>{vers}.</b> {txt}</small>", unsafe_allow_html=True)
                        full_text_devocional += f"\n\nTexto de {book} {chap}:\n{text_content}"
                
                with tab_reflexao:
                    col_ia_1, col_ia_2 = st.columns([1, 3])
                    with col_ia_1:
                        st.markdown("### ✨ Insights")
                        if st.button("Gerar Devocional", use_container_width=True):
                            if not HAS_GENAI:
                                st.error("Biblioteca indisponível.")
                            elif not api_key:
                                st.error("Insira a API Key na barra lateral.")
                            else:
                                try:
                                    with st.spinner("Meditando na palavra..."):
                                        client = genai.Client(api_key=api_key)
                                        prompt_devocional = f"""
                                        Crie um devocional curto e inspirador baseado em: {reading_title}.
                                        Trechos: {full_text_devocional[:20000]}
                                        Foque em um tema de união entre os textos ou no texto mais forte.
                                        Formate com Markdown bonito, usando negrito e itálico.
                                        Estrutura: Versículo Chave, Reflexão Profunda, Aplicação Prática, Oração.
                                        """
                                        response = client.models.generate_content(
                                            model='gemini-2.5-flash-lite',
                                            contents=prompt_devocional
                                        )
                                        st.session_state['devocional_result'] = response.text
                                except Exception as e:
                                    st.error(f"Erro: {e}")
                    
                    with col_ia_2:
                        if 'devocional_result' in st.session_state:
                            st.markdown(st.session_state['devocional_result'])
                        else:
                            st.info("Clique no botão ao lado para gerar uma reflexão exclusiva para hoje.")

        # ---------------------------------------------------------
        # DASHBOARD
        # ---------------------------------------------------------
        elif menu == "📊 Visão Geral":
            st.title("Visão Macro")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Livros", df['Livro'].nunique())
            c2.metric("Capítulos", df.groupby(['Livro', 'Capitulo']).ngroups)
            c3.metric("Versículos", len(df))
            
            total_words = df['Texto'].astype(str).apply(lambda x: len(x.split())).sum()
            c4.metric("Palavras (aprox.)", f"{total_words:,.0f}".replace(",", "."))
            
            st.markdown("### Distribuição de Conteúdo")
            verse_counts = df['Livro'].value_counts().reset_index()
            verse_counts.columns = ['Livro', 'Contagem']
            
            if 'Livro_ID' in df.columns:
                order_map = df[['Livro', 'Livro_ID']].drop_duplicates().set_index('Livro')['Livro_ID']
                verse_counts['ID'] = verse_counts['Livro'].map(order_map)
                verse_counts = verse_counts.sort_values('ID')
            
            fig = px.bar(verse_counts, x='Livro', y='Contagem', color='Contagem', 
                         color_continuous_scale=['#1e295a', '#F18F01'])
            apply_theme_to_plot(fig)
            st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------------------------
        # ENTIDADES
        # ---------------------------------------------------------
        elif menu == "👥 Análise de Entidades":
            st.title("Personagens e Entidades")
            
            all_entities = [ent for sublist in df['Entidades'] for ent in sublist]
            entity_counts = Counter(all_entities).most_common(50)
            df_ent = pd.DataFrame(entity_counts, columns=['Entidade', 'Frequência'])
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.markdown("#### Top Mencionado")
                st.dataframe(df_ent, height=500, use_container_width=True)
                
            with c2:
                st.markdown("#### Frequência Visual")
                fig = px.bar(df_ent.head(20), x='Frequência', y='Entidade', orientation='h', 
                             color='Frequência', color_continuous_scale='Blues')
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                apply_theme_to_plot(fig)
                st.plotly_chart(fig, use_container_width=True)
                
            st.divider()
            st.subheader("Rastreamento de Entidade")
            
            unique_entities_list = sorted(list(set(all_entities)))
            selected_entity = st.selectbox("Selecione uma entidade:", unique_entities_list)
            
            if selected_entity:
                mask = df['Entidades'].apply(lambda x: selected_entity in x)
                df_filtered = df[mask].copy()
                df_filtered['Posicao_Global'] = df_filtered.index
                
                fig_timeline = px.scatter(
                    df_filtered, 
                    x='ID_Global' if 'ID_Global' in df.columns else df_filtered.index, 
                    y='Livro', 
                    hover_data=['Capitulo', 'Versiculo', 'Texto'],
                    title=f"Ocorrências de '{selected_entity}'",
                    color='Livro'
                )
                fig_timeline.update_layout(showlegend=False)
                apply_theme_to_plot(fig_timeline)
                # Customizar marcadores para laranja
                fig_timeline.update_traces(marker=dict(color='#F18F01', size=8, opacity=0.7))
                
                st.plotly_chart(fig_timeline, use_container_width=True)
                
                with st.expander(f"Ver versículos citados ({len(df_filtered)})"):
                    st.dataframe(df_filtered[['Livro', 'Capitulo', 'Versiculo', 'Texto']], use_container_width=True)

        # ---------------------------------------------------------
        # REDES (SNA)
        # ---------------------------------------------------------
        elif menu == "🕸️ Redes de Conexão (SNA)":
            st.title("Redes Sociais Bíblicas")
            st.info("Visualização de quem aparece junto com quem no mesmo versículo.")
            
            edge_counter = Counter()
            node_counter = Counter()
            for entities in df['Entidades']:
                if len(entities) > 1:
                    sorted_ents = sorted(entities)
                    for i in range(len(sorted_ents)):
                        node_counter[sorted_ents[i]] += 1
                        for j in range(i + 1, len(sorted_ents)):
                            edge = (sorted_ents[i], sorted_ents[j])
                            edge_counter[edge] += 1
            
            with st.container():
                c_filter_1, c_filter_2 = st.columns(2)
                with c_filter_1:
                    min_weight = st.slider("Força da Conexão (Peso Mínimo)", 1, 50, 5)
                
                all_available_nodes = sorted([k for k, v in node_counter.items() if v > 1])
                with c_filter_2:
                    focus_option = st.selectbox("Focar em:", ["Visão Geral (Top Conectados)"] + all_available_nodes)

            max_nodes = 50
            if focus_option == "Visão Geral (Top Conectados)":
                max_nodes = st.slider("Máximo de Nós", 10, 200, 50)

            # Grafo
            G = nx.Graph()
            if focus_option == "Visão Geral (Top Conectados)":
                top_nodes = [n for n, c in node_counter.most_common(max_nodes)]
                for edge, weight in edge_counter.items():
                    if weight >= min_weight:
                        source, target = edge
                        if source in top_nodes and target in top_nodes:
                            G.add_edge(source, target, weight=weight)
                            G.add_node(source, size=node_counter[source])
                            G.add_node(target, size=node_counter[target])
            else:
                target_entity = focus_option
                G.add_node(target_entity, size=node_counter[target_entity])
                found = False
                for edge, weight in edge_counter.items():
                    if weight >= min_weight:
                        if target_entity in edge:
                            found = True
                            neighbor = edge[1] if edge[0] == target_entity else edge[0]
                            G.add_edge(target_entity, neighbor, weight=weight)
                            G.add_node(neighbor, size=node_counter[neighbor])
                if not found:
                    st.warning(f"Sem conexões fortes para {target_entity} com peso >= {min_weight}.")

            if len(G.nodes) > 0:
                pos = nx.spring_layout(G, k=0.6, seed=42)
                
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.append(x0)
                    edge_x.append(x1)
                    edge_x.append(None)
                    edge_y.append(y0)
                    edge_y.append(y1)
                    edge_y.append(None)

                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=0.5, color='#4c5187'), # Azul médio para linhas
                    hoverinfo='none',
                    mode='lines')

                node_x = []
                node_y = []
                node_text = []
                node_size = []
                node_colors = []
                
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_text.append(f"{node} ({G.nodes[node].get('size', 0)})")
                    sz = G.nodes[node].get('size', 10)
                    node_size.append(min(60, max(15, sz / 4)))
                    if focus_option != "Visão Geral (Top Conectados)" and node == focus_option:
                        node_colors.append(1000)
                    else:
                        node_colors.append(len(list(G.neighbors(node))))

                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    hoverinfo='text',
                    text=[node for node in G.nodes()],
                    textposition="top center",
                    textfont=dict(color='#1e295a', size=10), # Texto escuro
                    marker=dict(
                        showscale=True,
                        colorscale='Sunset', # Cores quentes (laranja/roxo)
                        reversescale=False,
                        color=node_colors,
                        size=node_size,
                        line_width=2,
                        line_color='white'))
                
                fig_net = go.Figure(data=[edge_trace, node_trace])
                apply_theme_to_plot(fig_net)
                # Remover eixos para grafo limpo
                fig_net.update_layout(
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(b=0,l=0,r=0,t=20)
                )
                
                st.plotly_chart(fig_net, use_container_width=True)
            else:
                st.warning("Nenhum dado para exibir no grafo.")

        # ---------------------------------------------------------
        # EXPLORADOR
        # ---------------------------------------------------------
        elif menu == "🔍 Explorador de Texto":
            st.title("Pesquisa Avançada")
            
            col_search, col_stats = st.columns([3, 1])
            with col_search:
                search_term = st.text_input("Buscar termo", placeholder="Ex: amor, espada, luz...")
            
            if search_term:
                results = df[df['Texto'].str.contains(search_term, case=False, na=False)]
                with col_stats:
                    st.metric("Encontrados", len(results))
                
                st.dataframe(results[['Livro', 'Capitulo', 'Versiculo', 'Texto']], use_container_width=True)
            
            st.divider()
            
            c_livro, c_cap = st.columns(2)
            livro_sel = c_livro.selectbox("Livro", df['Livro'].unique())
            caps_disponiveis = df[df['Livro'] == livro_sel]['Capitulo'].unique()
            cap_sel = c_cap.selectbox("Capítulo", sorted(caps_disponiveis))
            
            texto_capitulo = df[(df['Livro'] == livro_sel) & (df['Capitulo'] == cap_sel)]
            
            st.markdown(f"### {livro_sel} {cap_sel}")
            
            # Formatação bonita do texto corrido
            texto_html = "<div style='background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #F18F01;'>"
            for _, row in texto_capitulo.iterrows():
                v = row['Versiculo']
                t = row['Texto']
                for ent in row['Entidades']:
                    t = t.replace(ent, f"<b style='color:#833500'>{ent}</b>")
                texto_html += f"<sup><b>{v}</b></sup> {t} "
            texto_html += "</div>"
            
            st.markdown(texto_html, unsafe_allow_html=True)

        # ---------------------------------------------------------
        # ASSISTENTE IA
        # ---------------------------------------------------------
        elif menu == "🤖 Assistente de Estudo IA":
            st.title("Assistente Teológico (IA)")
            
            if not HAS_GENAI:
                st.error("Biblioteca Google GenAI ausente.")
                st.stop()
            
            if not api_key:
                st.warning("Insira a API Key na barra lateral.")

            c1, c2, c3 = st.columns(3)
            livro_sel = c1.selectbox("Livro", df['Livro'].unique(), key='ia_livro')
            caps_disponiveis = df[df['Livro'] == livro_sel]['Capitulo'].unique()
            cap_sel = c2.selectbox("Capítulo", sorted(caps_disponiveis), key='ia_cap')
            versiculos_disponiveis = df[(df['Livro'] == livro_sel) & (df['Capitulo'] == cap_sel)]['Versiculo'].unique()
            versiculos_com_todos = ["Todos"] + list(sorted(versiculos_disponiveis))
            vers_sel = c3.selectbox("Versículo", versiculos_com_todos, key='ia_vers')
            
            if vers_sel == "Todos":
                texto_df = df[(df['Livro'] == livro_sel) & (df['Capitulo'] == cap_sel)]
                texto_completo = " ".join(texto_df['Texto'].astype(str).tolist())
                referencia = f"{livro_sel} {cap_sel}"
            else:
                texto_df = df[(df['Livro'] == livro_sel) & (df['Capitulo'] == cap_sel) & (df['Versiculo'] == vers_sel)]
                if not texto_df.empty:
                    texto_completo = texto_df.iloc[0]['Texto']
                    referencia = f"{livro_sel} {cap_sel}:{vers_sel}"
                else:
                    texto_completo = ""
                    referencia = ""

            st.info(f"**Analisando:** {referencia}")
            with st.expander("Ver texto completo"):
                st.write(texto_completo)

            if st.button("🔍 Analisar Profundamente"):
                if not api_key:
                    st.error("Falta API Key")
                elif not texto_completo:
                    st.error("Sem texto")
                else:
                    try:
                        with st.spinner("Consultando especialistas digitais..."):
                            client = genai.Client(api_key=api_key)
                            prompt = f"""
                            Especialista em teologia: analise {referencia}: "{texto_completo}".
                            1. Contexto Histórico/Literário.
                            2. Exegese e Teologia.
                            3. Aplicação Prática Moderna.
                            Use Markdown estruturado.
                            """
                            response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
                            st.markdown("---")
                            st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Erro: {e}")

else:
    # Tela de Boas Vindas (Placeholder quando não tem arquivo)
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h1 style='color: #1e295a;'>Bem-vindo ao seu caminho com Deus</h1>
        <p style='font-size: 1.2rem; color: #5f5f5f;'>Sua central de inteligência e devoção bíblica diária.</p>
        <hr style='width: 50%; margin: 20px auto; border-color: #F18F01;'>
        <p>📂 Para começar, faça o upload da bíblia <b>blivre.xlsx</b> na barra lateral.</p>
    </div>
    """, unsafe_allow_html=True)
