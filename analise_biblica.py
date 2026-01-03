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

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background-color: var(--primary-100); /* Azul Profundo Original */
    }
    
    /* FORÇAR TEXTO CLARO NA SIDEBAR PARA CONTRASTE */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div {
        color: var(--bg-100) !important; /* Texto Creme Claro */
    }

    /* EXCEÇÃO: Inputs na sidebar (Fundo Branco -> Texto Escuro) */
    [data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: white !important;
        border: 1px solid var(--primary-200) !important;
    }
    [data-testid="stSidebar"] input {
        color: var(--text-100) !important; /* Texto escuro dentro do input */
        -webkit-text-fill-color: var(--text-100) !important;
    }
    
    /* Separador */
    [data-testid="stSidebar"] hr {
        border-color: var(--primary-200) !important;
        opacity: 0.5;
    }
    
    /* RADIO BUTTONS (MENU) NA SIDEBAR */
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        background-color: transparent;
        color: var(--bg-100) !important; /* Texto claro */
        border: 1px solid transparent;
        padding: 10px;
        border-radius: 5px;
        transition: all 0.3s;
    }
    div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
        background-color: var(--primary-200); /* Azul médio no hover */
        color: white !important;
    }
    /* Item selecionado do menu */
    div.row-widget.stRadio > div[role="radiogroup"] [data-testid="stMarkdownContainer"] > p {
        color: inherit !important;
    }

    /* HEADER SUPERIOR */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    /* Ícones do menu superior */
    header[data-testid="stHeader"] .st-emotion-cache-15zrgzn, 
    header[data-testid="stHeader"] button {
        color: var(--primary-100) !important;
    }

    /* CABEÇALHOS GERAIS (ÁREA PRINCIPAL) */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-100) !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    h1 {
        border-bottom: 2px solid var(--accent-100);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* LABELS DE INPUTS (Área Principal) */
    .main .stDateInput label, .main .stTextInput label, .main .stSelectbox label, .main .stSlider label, .main .stNumberInput label, .main .stMultiSelect label {
        color: var(--primary-100) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* DATA INPUT & CAMPOS DE TEXTO - FUNDO CLARO (Área Principal) */
    .main div[data-baseweb="input"], .main div[data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid var(--bg-300);
        color: var(--text-100);
    }
    .main input {
        color: var(--text-100) !important;
    }

    /* BARRA DE PROGRESSO */
    .stProgress > div > div > div > div {
        background-color: var(--accent-100) !important;
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
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: var(--accent-200);
        color: white !important;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* TABELAS */
    [data-testid="stDataFrame"] {
        background-color: transparent !important; 
    }
    [data-testid="stDataFrame"] > div {
        background-color: white; 
        border-radius: 10px;
        padding: 5px;
    }

    /* EXPANSORES */
    .stExpander {
        background-color: white;
        border-radius: 10px;
        border: 1px solid var(--bg-300);
    }
    .streamlit-expanderHeader p {
        color: var(--accent-100) !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* ABAS (TABS) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-200);
        border-radius: 8px 8px 0 0;
        color: var(--text-200);
        font-size: 1.1rem !important;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-100) !important;
        color: white !important;
    }

    /* TAG PERSONALIZADA */
    selection-tag {
        color: var(--primary-100);
        font-weight: bold;
    }

    /* ALERTAS PERSONALIZADOS */
    .custom-info {
        padding: 1rem;
        background-color: #dbeafe; 
        color: #1e40af; 
        border-radius: 0.5rem;
        border-left: 5px solid #3b82f6;
        margin-bottom: 1rem;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# 1. FUNÇÕES DE CARREGAMENTO E PROCESSAMENTO
# =========================================================

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        cols_map = {
            'Book Name': 'Livro', 'Book Number': 'Livro_ID', 
            'Chapter': 'Capitulo', 'Verse': 'Versiculo', 
            'Text': 'Texto', 'Verse ID': 'ID_Global'
        }
        df.rename(columns=cols_map, inplace=True, errors='ignore')
        required_cols = ['Livro', 'Capitulo', 'Versiculo', 'Texto']
        if not all(col in df.columns for col in required_cols):
            st.error(f"O arquivo deve conter as colunas: {required_cols}")
            return None
        return df
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

STOPWORDS_PT = set(['a', 'o', 'as', 'os', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas', 'por', 'pelo', 'pela', 'para', 'que', 'e', 'é', 'era', 'foi', 'com', 'sem', 'seu', 'sua', 'seus', 'suas', 'ele', 'ela', 'eles', 'elas', 'mas', 'ou', 'quando', 'como', 'onde', 'quem', 'porque', 'se', 'eu', 'tu', 'nós', 'vós', 'me', 'te', 'lhe', 'nos', 'vos', 'lhes', 'mim', 'ti', 'si', 'este', 'esta', 'isto', 'esse', 'essa', 'isso', 'aquele', 'aquela', 'aquilo', 'meu', 'teu', 'nosso', 'vosso', 'tua', 'minha', 'nossa', 'vossa', 'senhor', 'deus', 'jesus', 'cristo', 'não', 'eis', 'quis', 'então', 'amém', 'segunda', 'Assim'])

BIG_ENTITIES = ['Deus', 'Jesus', 'Senhor', 'Espírito', 'Moisés', 'Arão', 'Faraó', 'Josué', 'Davi', 'Saul', 'Salomão', 'Elias', 'Eliseu', 'Isaías', 'Jeremias', 'Ezequiel', 'Daniel', 'Pedro', 'Paulo', 'João', 'Tiago', 'Maria', 'José', 'Abraão', 'Isaque', 'Jacó', 'José', 'Judá', 'Pilatos', 'Herodes', 'Judas', 'Timóteo', 'Barnabé', 'Silas', 'Tito', 'Noé', 'Adão', 'Eva', 'Caim', 'Abel', 'Golias', 'Jonas', 'Jó', 'Samuel', 'Absalão', 'Nabucodonosor', 'Calebe']

def simple_entity_extractor(text):
    if not isinstance(text, str): return []
    clean_text = re.sub(r'[^\w\s]', '', text)
    words = clean_text.split()
    entities = []
    for i, word in enumerate(words):
        if word in BIG_ENTITIES:
            entities.append(word)
            continue
        if i > 0 and word[0].isupper() and word.lower() not in STOPWORDS_PT:
            if len(word) > 2: entities.append(word)
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

def apply_theme_to_plot(fig, transparent=True, dark_text=False):
    paper_color = 'rgba(0,0,0,0)' if transparent else 'white'
    plot_color = 'rgba(255,255,255,0.7)' if transparent else 'white'
    text_color = '#353535' if dark_text else '#353535'
    
    fig.update_layout(
        paper_bgcolor=paper_color,
        plot_bgcolor=plot_color,
        font_color=text_color,
        title_font_color='#1e295a',
        colorway=['#1e295a', '#F18F01', '#4c5187', '#abacea', '#833500'],
    )
    return fig

def fmt_num(num):
    return f"{num:,.0f}".replace(",", ".")

# =========================================================
# 2. INTERFACE E NAVEGAÇÃO
# =========================================================

st.sidebar.markdown("# ✝️ Seu Guia Bíblico")
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
            
        st.sidebar.success(f"Carregado: {fmt_num(len(df))} versículos")
        st.sidebar.markdown("---")
        
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

        # ---------------------------------------------------------
        # DEVOCIONAL
        # ---------------------------------------------------------
        if menu == "🙏 Devocional Diário":
            st.title("Devocional Anual")
            st.markdown("*Uma jornada aleatória e inspiradora através das escrituras.*")
            
            plan, total_chapters = generate_reading_plan(df)
            
            # Inicializar estado de leitura se não existir
            if 'read_days' not in st.session_state:
                st.session_state['read_days'] = []

            col_date, col_nav = st.columns([1, 2])
            with col_date:
                today = datetime.now()
                selected_date = st.date_input("Selecione a Data", today, format="DD/MM/YYYY")
                day_of_year = selected_date.timetuple().tm_yday
                if day_of_year > 365: day_of_year = 365
            
            with col_nav:
                st.markdown(f"<p style='color:#1e295a; font-weight:bold; margin-bottom:0px;'>Progresso do Ano (Dia {day_of_year}/365)</p>", unsafe_allow_html=True)
                progress = day_of_year / 365
                st.progress(progress)

            todays_chapters = plan.get(day_of_year, [])

            if not todays_chapters:
                st.info("Nenhuma leitura programada.")
            else:
                reading_refs = []
                for book, chap in todays_chapters:
                    reading_refs.append(f"{book} {chap}")
                
                reading_title = ", ".join(reading_refs[:3]) + f" e mais {len(reading_refs)-3}" if len(reading_refs) > 3 else ", ".join(reading_refs)
                
                st.subheader(f"📖 Leitura de Hoje: {reading_title}")
                
                # --- SISTEMA DE ABAS (INCLUINDO NOVA ABA DE PROGRESSO) ---
                tab_texto, tab_reflexao, tab_progresso = st.tabs(["Texto Bíblico", "Reflexão com IA", "📈 Meu Progresso"])
                
                full_text_devocional = ""
                
                with tab_texto:
                    for book, chap in todays_chapters:
                        st.markdown(f"#### {book} {chap}")
                        subset = df[(df['Livro'] == book) & (df['Capitulo'] == chap)]
                        text_content = ""
                        
                        html_text = ""
                        for _, row in subset.iterrows():
                            vers = row['Versiculo']
                            txt = row['Texto']
                            text_content += f"{vers}. {txt} "
                            html_text += f"<div style='margin-bottom: 8px;'><span style='color:#833500; font-weight:bold;'>{vers}.</span> <span style='color:#353535;'>{txt}</span></div>"
                        
                        st.markdown(html_text, unsafe_allow_html=True)
                        full_text_devocional += f"\n\nTexto de {book} {chap}:\n{text_content}"
                        st.markdown("<hr style='border-color: #c2baa6; opacity: 0.5;'>", unsafe_allow_html=True)
                
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
                                        response = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt_devocional)
                                        st.session_state['devocional_result'] = response.text
                                except Exception as e:
                                    st.error(f"Erro: {e}")
                    
                    with col_ia_2:
                        if 'devocional_result' in st.session_state:
                            st.markdown(f"""<div style="background-color: white; padding: 30px; border-radius: 10px; border-left: 5px solid #F18F01; box-shadow: 2px 2px 15px rgba(0,0,0,0.05);">{st.session_state['devocional_result']}</div>""", unsafe_allow_html=True)
                        else:
                            st.info("Clique no botão ao lado para gerar uma reflexão exclusiva para hoje.")

                # ABA 3: MEU PROGRESSO
                with tab_progresso:
                    st.markdown("### 🗓️ Controle de Leitura")
                    st.markdown("Marque os dias que você já concluiu para atualizar seu progresso nos livros.")
                    
                    # Layout para seleção de dias
                    c_sel, c_btn = st.columns([3, 1])
                    with c_sel:
                        days_selected = st.multiselect(
                            "Dias Concluídos (1 a 365)", 
                            options=range(1, 366),
                            default=st.session_state['read_days']
                        )
                    
                    with c_btn:
                        st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
                        if st.button("Marcar até Hoje", use_container_width=True):
                            st.session_state['read_days'] = list(range(1, day_of_year + 1))
                            st.rerun()
                        if st.button("Limpar Tudo", use_container_width=True):
                            st.session_state['read_days'] = []
                            st.rerun()

                    # Atualiza estado
                    if days_selected != st.session_state['read_days']:
                        st.session_state['read_days'] = days_selected
                        st.rerun()

                    st.divider()

                    if not st.session_state['read_days']:
                        st.info("Nenhum dia marcado ainda.")
                    else:
                        # CALCULO DE PROGRESSO
                        read_chapters_set = set()
                        for d in st.session_state['read_days']:
                            chapters_in_day = plan.get(d, [])
                            for book, chap in chapters_in_day:
                                read_chapters_set.add((book, chap))
                        
                        if 'Livro_ID' in df.columns:
                            all_chapters = df[['Livro_ID', 'Livro', 'Capitulo']].drop_duplicates()
                            book_order = df[['Livro', 'Livro_ID']].drop_duplicates().sort_values('Livro_ID')['Livro'].tolist()
                        else:
                            all_chapters = df[['Livro', 'Capitulo']].drop_duplicates()
                            book_order = sorted(df['Livro'].unique())
                        
                        total_counts = all_chapters.groupby('Livro').size()
                        
                        if read_chapters_set:
                            read_df = pd.DataFrame(list(read_chapters_set), columns=['Livro', 'Capitulo'])
                            read_counts = read_df.groupby('Livro').size()
                        else:
                            read_counts = pd.Series()

                        st.markdown("#### Progresso por Livro")
                        
                        cols = st.columns(3)
                        count_displayed = 0
                        
                        for i, book in enumerate(book_order):
                            total = total_counts.get(book, 0)
                            read = read_counts.get(book, 0)
                            
                            if total > 0 and read > 0:
                                pct = read / total
                                if pct > 1.0: pct = 1.0
                                
                                with cols[count_displayed % 3]:
                                    st.markdown(f"**{book}**")
                                    st.progress(pct)
                                    st.caption(f"{read}/{total} caps ({int(pct*100)}%)")
                                count_displayed += 1
                        
                        if count_displayed == 0:
                            st.info("Os dias marcados não contêm capítulos processados no plano atual.")

        # ---------------------------------------------------------
        # DASHBOARD
        # ---------------------------------------------------------
        elif menu == "📊 Visão Geral":
            st.title("Visão Macro")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Livros", fmt_num(df['Livro'].nunique()))
            c2.metric("Capítulos", fmt_num(df.groupby(['Livro', 'Capitulo']).ngroups))
            c3.metric("Versículos", fmt_num(len(df)))
            total_words = df['Texto'].astype(str).apply(lambda x: len(x.split())).sum()
            c4.metric("Palavras (aprox.)", fmt_num(total_words))
            
            st.markdown("### Distribuição de Conteúdo")
            verse_counts = df['Livro'].value_counts().reset_index()
            verse_counts.columns = ['Livro', 'Contagem']
            if 'Livro_ID' in df.columns:
                order_map = df[['Livro', 'Livro_ID']].drop_duplicates().set_index('Livro')['Livro_ID']
                verse_counts['ID'] = verse_counts['Livro'].map(order_map)
                verse_counts = verse_counts.sort_values('ID')
            
            fig = px.bar(
                verse_counts, x='Livro', y='Contagem', 
                color='Contagem', color_continuous_scale=['#1e295a', '#F18F01']
            )
            
            fig.update_traces(marker_line_width=0)
            fig.update_layout(
                paper_bgcolor='rgba(255,255,255,0.9)', 
                plot_bgcolor='rgba(255,255,255,0.9)',
                font=dict(color='black'),
                xaxis=dict(title=None, tickfont=dict(color='black'), showgrid=False),
                yaxis=dict(title=None, showticklabels=False, showgrid=False, visible=False),
                coloraxis_showscale=False,
                margin=dict(l=20, r=20, t=20, b=60),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------------------------
        # ENTIDADES
        # ---------------------------------------------------------
        elif menu == "👥 Análise de Entidades":
            st.title("Personagens e Entidades")
            
            all_entities = [ent for sublist in df['Entidades'] for ent in sublist]
            entity_counts = Counter(all_entities).most_common(50)
            df_ent = pd.DataFrame(entity_counts, columns=['Entidade', 'Frequência'])
            
            # Tabela de Frequência - largura total, sem colunas
            st.markdown("### Tabela de Frequência (Top 50)")
            # Fundo transparente aplicado via CSS, aqui apenas chamamos o df
            st.dataframe(df_ent, height=600, use_container_width=True)
            
            st.divider()
            st.subheader("Rastreamento de Entidade (Modo Escuro)")
            
            unique_entities_list = sorted(list(set(all_entities)))
            selected_entity = st.selectbox("Selecione uma entidade:", unique_entities_list)
            
            if selected_entity:
                mask = df['Entidades'].apply(lambda x: selected_entity in x)
                df_filtered = df[mask].copy()
                
                if 'ID_Global' in df_filtered.columns:
                    df_filtered = df_filtered.sort_values('ID_Global')
                else:
                    df_filtered = df_filtered.sort_index()
                
                book_order = []
                if 'Livro_ID' in df.columns:
                    book_order = df[['Livro', 'Livro_ID']].drop_duplicates().sort_values('Livro_ID')['Livro'].tolist()
                else:
                    book_order = df['Livro'].unique().tolist()

                fig_timeline = px.scatter(
                    df_filtered, 
                    x='ID_Global' if 'ID_Global' in df.columns else df_filtered.index, 
                    y='Livro', 
                    color='Livro',
                    hover_data=['Capitulo', 'Versiculo', 'Texto'],
                    title=f"Dispersão de '{selected_entity}' nas Escrituras",
                    category_orders={"Livro": book_order}
                )
                
                fig_timeline.update_traces(
                    marker=dict(size=8, opacity=0.9, symbol='circle'),
                    mode='markers'
                )
                
                fig_timeline.update_layout(
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    font_color='white',
                    title_font_color='white',
                    xaxis=dict(showgrid=False, title="Progresso na Bíblia", color='white', showticklabels=False),
                    yaxis=dict(showgrid=True, gridcolor='#333', color='white'),
                    legend=dict(
                        bgcolor='rgba(0,0,0,0.5)',
                        font=dict(color='white')
                    ),
                    height=600
                )
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
                c_filter_1, c_filter_2, c_filter_3 = st.columns(3)
                with c_filter_1:
                    min_weight = st.slider("Força da Conexão (Peso Mínimo)", 1, 50, 5)
                
                all_available_nodes = sorted([k for k, v in node_counter.items() if v > 1])
                with c_filter_2:
                    focus_option = st.selectbox("Focar em:", ["Visão Geral (Top Conectados)"] + all_available_nodes)
                
                # Nova Funcionalidade: Layout do Grafo
                with c_filter_3:
                    layout_opt = st.selectbox("Layout do Grafo", ["Spring (Padrão)", "Circular", "Aleatório", "Shell"])

            max_nodes = 50
            if focus_option == "Visão Geral (Top Conectados)":
                max_nodes = st.slider("Máximo de Nós", 10, 200, 50)

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
                # Aplicação da escolha de Layout
                if layout_opt == "Spring (Padrão)":
                    pos = nx.spring_layout(G, k=0.6, seed=42)
                elif layout_opt == "Circular":
                    pos = nx.circular_layout(G)
                elif layout_opt == "Aleatório":
                    pos = nx.random_layout(G, seed=42)
                elif layout_opt == "Shell":
                    pos = nx.shell_layout(G)
                else:
                    pos = nx.spring_layout(G, k=0.6, seed=42)

                edge_x = []
                edge_y = []
                for edge in G.edges():
                    if edge[0] in pos and edge[1] in pos:
                        x0, y0 = pos[edge[0]]
                        x1, y1 = pos[edge[1]]
                        edge_x.append(x0); edge_x.append(x1); edge_x.append(None)
                        edge_y.append(y0); edge_y.append(y1); edge_y.append(None)

                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=0.5, color='#4c5187'),
                    hoverinfo='none', mode='lines')

                node_x = []
                node_y = []
                node_text = [] 
                node_size = []
                node_colors = []
                
                for node in G.nodes():
                    if node in pos:
                        x, y = pos[node]
                        node_x.append(x)
                        node_y.append(y)
                        node_text.append(f"{node} (Menções: {G.nodes[node].get('size', 0)})")
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
                    text=node_text,
                    textposition="top center",
                    textfont=dict(color='#1e295a', size=10),
                    marker=dict(
                        showscale=True, colorscale='Sunset', reversescale=False,
                        color=node_colors, size=node_size, line_width=2, line_color='white'
                    )
                )
                
                fig_net = go.Figure(data=[edge_trace, node_trace])
                apply_theme_to_plot(fig_net)
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
            
            texto_html = "<div style='background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #F18F01; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);'>"
            for _, row in texto_capitulo.iterrows():
                v = row['Versiculo']
                t = row['Texto']
                for ent in row['Entidades']:
                    t = t.replace(ent, f"<b style='color:#833500'>{ent}</b>")
                texto_html += f"<div style='margin-bottom: 5px;'><sup style='color:#1e295a; font-weight:bold; margin-right: 5px;'>{v}</sup> {t}</div>"
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
                st.markdown("""
                <div class="custom-info">
                    <strong>ℹ️ Atenção:</strong> Insira sua API Key do Google Gemini na barra lateral para ativar a inteligência artificial.
                </div>
                """, unsafe_allow_html=True)

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
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h1 style='color: #1e295a;'>Bem-vindo ao seu caminho com Deus</h1>
        <p style='font-size: 1.2rem; color: #5f5f5f;'>Sua central de inteligência e devoção bíblica diária.</p>
        <hr style='width: 50%; margin: 20px auto; border-color: #F18F01;'>
        <p>📂 Para começar, faça o upload da bíblia <b>blivre.xlsx</b> na barra lateral.</p>
    </div>
    """, unsafe_allow_html=True)
