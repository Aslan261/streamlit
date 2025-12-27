import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import re

# Configuração da Página
st.set_page_config(page_title="Bíblia Analytics", layout="wide")

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
    'eis', 'quis'
])

# Lista de principais figuras bíblicas para priorizar na busca
BIG_ENTITIES = [
    'Deus', 'Jesus', 'Senhor', 'Espírito', 'Moisés', 'Arão', 'Faraó', 'Josué', 
    'Davi', 'Saul', 'Salomão', 'Elias', 'Eliseu', 'Isaías', 'Jeremias', 'Ezequiel', 
    'Daniel', 'Pedro', 'Paulo', 'João', 'Tiago', 'Maria', 'José', 'Abraão', 
    'Isaque', 'Jacó', 'José', 'Judá', 'Pilatos', 'Herodes', 'Judas', 'Timóteo',
    'Barnabé', 'Silas', 'Tito', 'Noé', 'Adão', 'Eva', 'Caim', 'Abel', 'Golias',
    'Jonas', 'Jó', 'Samuel', 'Absalão', 'Nabucodonosor'
]

def simple_entity_extractor(text):
    """
    Extrai palavras com inicial maiúscula que não estão no início da frase
    e filtra por uma lista de nomes comuns bíblicos.
    """
    if not isinstance(text, str):
        return []
    
    # Limpeza básica
    clean_text = re.sub(r'[^\w\s]', '', text)
    words = clean_text.split()
    
    entities = []
    
    for i, word in enumerate(words):
        # Verifica se é um dos grandes nomes (independente de posição)
        if word in BIG_ENTITIES:
            entities.append(word)
            continue
            
        # Heurística: Palavra com maiúscula no meio da frase
        if i > 0 and word[0].isupper() and word.lower() not in STOPWORDS_PT:
            if len(word) > 2: # Evita siglas curtas ou erros
                entities.append(word)
                
    return list(set(entities)) # Remove duplicatas no mesmo versículo

@st.cache_data
def process_entities(df):
    # Aplica a extração
    df['Entidades'] = df['Texto'].apply(simple_entity_extractor)
    return df

# =========================================================
# 2. INTERFACE E NAVEGAÇÃO
# =========================================================

st.title("📖 Bíblia Analytics & Network")
st.markdown("Uma ferramenta para análise exploratória e visualização de redes no texto sagrado.")

# Sidebar para Upload
st.sidebar.header("Dados")
uploaded_file = st.sidebar.file_uploader("Carregar arquivo da Bíblia (CSV/Excel)", type=['csv', 'xlsx'])

# Se não tiver arquivo, usar dados de exemplo (mock) ou pedir arquivo
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = load_data(uploaded_file)
    else:
        # Se for excel, converte
        df = pd.read_excel(uploaded_file)
        cols_map = {'Book Name': 'Livro', 'Book Number': 'Livro_ID', 'Chapter': 'Capitulo', 'Verse': 'Versiculo', 'Text': 'Texto', 'Verse ID': 'ID_Global'}
        df.rename(columns=cols_map, inplace=True, errors='ignore')

    if df is not None:
        with st.spinner('Processando entidades e textos...'):
            df = process_entities(df)
            
        st.sidebar.success(f"Dados carregados! {len(df)} versículos.")
        
        # Menu Principal
        menu = st.sidebar.radio("Navegação", ["Dashboard Geral", "Análise de Entidades", "Redes de Conexão (SNA)", "Explorador de Texto"])
        
        # ---------------------------------------------------------
        # ABA: DASHBOARD GERAL
        # ---------------------------------------------------------
        if menu == "Dashboard Geral":
            st.header("Visão Macro")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total de Livros", df['Livro'].nunique())
            c2.metric("Total de Capítulos", df.groupby(['Livro', 'Capitulo']).ngroups)
            c3.metric("Total de Versículos", len(df))
            
            # Contagem de palavras aproximada
            total_words = df['Texto'].astype(str).apply(lambda x: len(x.split())).sum()
            c4.metric("Total de Palavras", f"{total_words:,.0f}".replace(",", "."))
            
            st.subheader("Distribuição de Versículos por Livro")
            verse_counts = df['Livro'].value_counts().reset_index()
            verse_counts.columns = ['Livro', 'Contagem']
            
            # Ordenar pela ordem original bíblica (usando ID se disponível)
            if 'Livro_ID' in df.columns:
                order_map = df[['Livro', 'Livro_ID']].drop_duplicates().set_index('Livro')['Livro_ID']
                verse_counts['ID'] = verse_counts['Livro'].map(order_map)
                verse_counts = verse_counts.sort_values('ID')
            
            fig = px.bar(verse_counts, x='Livro', y='Contagem', title="Versículos por Livro")
            st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------------------------
        # ABA: ANÁLISE DE ENTIDADES
        # ---------------------------------------------------------
        elif menu == "Análise de Entidades":
            st.header("Análise de Personagens e Entidades")
            
            # Flattening the list of entities
            all_entities = [ent for sublist in df['Entidades'] for ent in sublist]
            entity_counts = Counter(all_entities).most_common(50)
            df_ent = pd.DataFrame(entity_counts, columns=['Entidade', 'Frequência'])
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.subheader("Top Mencionado")
                st.dataframe(df_ent, height=500)
                
            with c2:
                st.subheader("Frequência Visual")
                fig = px.bar(df_ent.head(20), x='Frequência', y='Entidade', orientation='h', title="Top 20 Entidades")
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
            st.divider()
            
            # Análise Temporal/Posicional
            st.subheader("Onde a Entidade Aparece?")
            selected_entity = st.selectbox("Selecione uma entidade para rastrear:", df_ent['Entidade'].tolist())
            
            if selected_entity:
                # Filtrar dataframe
                mask = df['Entidades'].apply(lambda x: selected_entity in x)
                df_filtered = df[mask].copy()
                
                # Criar um índice sequencial global para o eixo X
                df_filtered['Posicao_Global'] = df_filtered.index
                
                fig_timeline = px.scatter(
                    df_filtered, 
                    x='ID_Global' if 'ID_Global' in df.columns else df_filtered.index, 
                    y='Livro', 
                    hover_data=['Capitulo', 'Versiculo', 'Texto'],
                    title=f"Dispersão de '{selected_entity}' ao longo da Bíblia",
                    color='Livro'
                )
                fig_timeline.update_layout(showlegend=False)
                st.plotly_chart(fig_timeline, use_container_width=True)
                
                with st.expander(f"Ver versículos com '{selected_entity}'"):
                    st.dataframe(df_filtered[['Livro', 'Capitulo', 'Versiculo', 'Texto']])

        # ---------------------------------------------------------
        # ABA: REDES (SNA)
        # ---------------------------------------------------------
        elif menu == "Redes de Conexão (SNA)":
            st.header("Análise de Redes Sociais Bíblica")
            st.markdown("Conexões baseadas em co-ocorrência: **Personagens que aparecem no mesmo versículo**.")
            
            # --- PREPARAÇÃO DOS DADOS ---
            edge_counter = Counter()
            node_counter = Counter()
            
            # Iterar sobre versículos e criar arestas (feito antes dos filtros para ter o universo completo)
            for entities in df['Entidades']:
                if len(entities) > 1:
                    sorted_ents = sorted(entities)
                    for i in range(len(sorted_ents)):
                        node_counter[sorted_ents[i]] += 1
                        for j in range(i + 1, len(sorted_ents)):
                            edge = (sorted_ents[i], sorted_ents[j])
                            edge_counter[edge] += 1
            
            # --- FILTROS DE INTERFACE ---
            col_filters_1, col_filters_2 = st.columns(2)
            
            with col_filters_1:
                min_weight = st.slider("Mínimo de Co-ocorrências (Peso)", 1, 50, 5)
            
            # Lista de entidades ordenada alfabeticamente para o dropdown
            all_available_nodes = sorted([k for k, v in node_counter.items() if v > 1])
            
            with col_filters_2:
                # Seletor de modo: Visão Geral ou Entidade Específica
                focus_option = st.selectbox(
                    "Focar em Entidade Específica", 
                    ["Visão Geral (Top Conectados)"] + all_available_nodes
                )

            # Filtro condicional de 'Máximo de Nós' (só mostra se for Visão Geral)
            max_nodes = 50
            if focus_option == "Visão Geral (Top Conectados)":
                max_nodes = st.slider("Máximo de Nós no Grafo", 10, 200, 50)

            # --- CONSTRUÇÃO DO GRAFO (G) ---
            G = nx.Graph()
            
            if focus_option == "Visão Geral (Top Conectados)":
                # LÓGICA ORIGINAL: Filtra pelos TOP N mais frequentes
                top_nodes = [n for n, c in node_counter.most_common(max_nodes)]
                
                for edge, weight in edge_counter.items():
                    if weight >= min_weight:
                        source, target = edge
                        if source in top_nodes and target in top_nodes:
                            G.add_edge(source, target, weight=weight)
                            G.add_node(source, size=node_counter[source])
                            G.add_node(target, size=node_counter[target])
                            
            else:
                # NOVA LÓGICA: Rede Egocêntrica (Foco na entidade selecionada)
                target_entity = focus_option
                
                # Adiciona o nó central
                G.add_node(target_entity, size=node_counter[target_entity])
                
                # Busca vizinhos conectados a esta entidade
                found_connections = False
                for edge, weight in edge_counter.items():
                    if weight >= min_weight:
                        if target_entity in edge:
                            found_connections = True
                            # Identifica quem é o vizinho
                            neighbor = edge[1] if edge[0] == target_entity else edge[0]
                            
                            G.add_edge(target_entity, neighbor, weight=weight)
                            G.add_node(neighbor, size=node_counter[neighbor])
                
                if not found_connections:
                    st.warning(f"A entidade '{target_entity}' não tem conexões com peso >= {min_weight}.")

            # --- VISUALIZAÇÃO ---
            if len(G.nodes) > 0:
                c1, c2, c3 = st.columns(3)
                c1.metric("Nós (Entidades)", len(G.nodes))
                c2.metric("Arestas (Conexões)", len(G.edges))
                density = nx.density(G)
                c3.metric("Densidade", f"{density:.4f}")
                
                # Layout do Grafo
                pos = nx.spring_layout(G, k=0.5, seed=42)
                
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
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    mode='lines')

                node_x = []
                node_y = []
                node_text = []
                node_size = []
                node_colors = [] # Para colorir diferente o nó central se houver foco
                
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_text.append(f"{node} (Menções: {G.nodes[node].get('size', 0)})")
                    
                    # Tamanho
                    sz = G.nodes[node].get('size', 10)
                    node_size.append(min(50, max(10, sz / 5)))
                    
                    # Cor (Lógica para destacar o selecionado)
                    if focus_option != "Visão Geral (Top Conectados)" and node == focus_option:
                        node_colors.append(1000) # Valor alto para cor diferente
                    else:
                        # Cor baseada no grau (conectividade)
                        node_colors.append(len(list(G.neighbors(node))))

                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    hoverinfo='text',
                    text=[node for node in G.nodes()],
                    textposition="top center",
                    marker=dict(
                        showscale=True,
                        colorscale='YlGnBu',
                        reversescale=True,
                        color=node_colors,
                        size=node_size,
                        colorbar=dict(
                            thickness=15,
                            title='Conectividade',
                            xanchor='left',
                        ),
                        line_width=2))
                
                fig_net = go.Figure(data=[edge_trace, node_trace],
                             layout=go.Layout(
                                title=dict(
                                    text=f'Rede: {focus_option}',
                                    font=dict(size=16)
                                ),
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20,l=5,r=5,t=40),
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                                )
                st.plotly_chart(fig_net, use_container_width=True)
                
                st.info("Dica: Use zoom no gráfico para explorar clusters específicos.")

            else:
                st.warning("Nenhuma conexão encontrada com os filtros atuais.")

        # ---------------------------------------------------------
        # ABA: EXPLORADOR
        # ---------------------------------------------------------
        elif menu == "Explorador de Texto":
            st.header("Leitura e Pesquisa")
            
            search_term = st.text_input("Pesquisar no texto (ex: 'amor', 'luz', 'espada')")
            
            if search_term:
                results = df[df['Texto'].str.contains(search_term, case=False, na=False)]
                st.write(f"Encontrados **{len(results)}** versículos contendo '{search_term}'.")
                st.dataframe(results[['Livro', 'Capitulo', 'Versiculo', 'Texto']], height=400)
            
            st.divider()
            
            c_livro, c_cap = st.columns(2)
            livro_sel = c_livro.selectbox("Livro", df['Livro'].unique())
            
            caps_disponiveis = df[df['Livro'] == livro_sel]['Capitulo'].unique()
            cap_sel = c_cap.selectbox("Capítulo", sorted(caps_disponiveis))
            
            texto_capitulo = df[(df['Livro'] == livro_sel) & (df['Capitulo'] == cap_sel)]
            
            st.subheader(f"{livro_sel} {cap_sel}")
            for _, row in texto_capitulo.iterrows():
                # Destacar entidades no texto se houver
                texto_fmt = row['Texto']
                for ent in row['Entidades']:
                    texto_fmt = texto_fmt.replace(ent, f"**{ent}**")
                    
                st.markdown(f"**{row['Versiculo']}.** {texto_fmt}")

else:
    st.info("Por favor, faça o upload do arquivo 'blivre.xlsx' ou CSV na barra lateral para começar.")
    st.markdown("""
    ### Instruções:
    1. Arraste o arquivo `blivre.xlsx` para a área de upload à esquerda.
    2. Aguarde o processamento inicial.
    3. Navegue pelas abas para explorar as visões analíticas.
    """)
