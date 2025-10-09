# Importando as bibliotecas necessárias
import streamlit as st
import unicodedata
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="DocentES | Censo Escolar",
    page_icon="👩🏻‍🏫",
    layout="wide"
)

# --- FUNÇÃO PARA CARREGAR TODOS OS DADOS ---
@st.cache_data
def carregar_dados():
    """
    Esta função carrega todos os 5 arquivos CSV em DataFrames separados
    e os retorna em um dicionário para fácil acesso.
    """
    # Nomes dos arquivos
    nomes_arquivos = {
        "dependencia": "docentes_dependencia.csv",
        "etapas": "docentes_etapas.csv",
        "formacao": "docentes_formacao.csv",
        "idade": "docentes_idade.csv",
        "vinculo": "docentes_vinculo.csv"
    }
    
    dataframes = {}
    for nome, caminho in nomes_arquivos.items():
        # Carrega cada dataframe usando ';' como separador
        df = pd.read_csv(caminho, delimiter=';')
        df.columns = df.columns.str.strip()
        dataframes[nome] = df
            
    return dataframes

# Carrega todos os dataframes
try:
    dfs = carregar_dados()
except FileNotFoundError as e:
    st.error(f"Erro ao carregar os dados: O arquivo {e.filename} não foi encontrado.")
    st.info("Por favor, certifique-se de que todos os 5 arquivos CSV estão na mesma pasta que o app.py.")
    st.stop()

# --- DEFININDO BARRA LATERAL COM FILTROS (Ano e Município) ---

# Definindo função auxiliar para normalizar texto para ordenação
def normalizar_para_ordenacao(texto):
    """
    Remove acentos de uma string para usá-la como chave de ordenação.
    Ex: 'Águia Branca' -> 'Aguia Branca'
    """
    # Normaliza a string para decompor os caracteres acentuados
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Remove os caracteres de combinação (acentos)
    return "".join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

# Foi usado o dataframe de 'etapas' como base para criar os filtros.
st.sidebar.header("⚙️ Filtros")
st.sidebar.markdown("Use os filtros abaixo para selecionar o ano e o município desejados.")

# Filtro de Ano
ano_selecionado = st.sidebar.selectbox(
    "Selecione o Ano",
    options=sorted(
                    dfs['etapas']['Ano'].unique(), 
                    reverse=True
                  )
)

# Filtro de Município
lista_municipios = sorted(
    dfs['etapas']['Município'].unique(),
    key=normalizar_para_ordenacao # Usando a função de normalização
    )
municipio_selecionado = st.sidebar.selectbox(
    "Selecione o Município",
    options=lista_municipios
)


# Conteúdo principal do app

# Título da página
st.title("👩🏾‍🏫 DocentES 👨🏻‍🏫")
st.write("Bem-vindo ao DocentES, a plataforma sobre os Docentes do Espírito Santo!")

# Criando estrutura com três colunas
col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
with col2:
    st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhWSVR_PA-xWPXwdQ5qyRDWAZZdVA1JhdQuaT6yI926pYTAg0boScUh3J-lsiu1i3KDyHJQmN_OgNx6HX4Zun6XDIRfqNXJe8CdyKcnwDymZp8P52JvRrKav0otT263CjHKyS_RitA5VPJFOg6NJ-uqRwuksj2r_J1mna9CnfEVq4psg-QMaH4bq2Uy2w/w485-h335/fc-removebg-preview.png", width=400)
with col3:
    st.write("")

st.write("Aqui você pode explorar dados sobre os professores do estado, incluindo informações demográficas, formação acadêmica, e muito mais.")

st.markdown("---")

# --- CRIAÇÃO DAS ABAS TEMÁTICAS (TABS) ---

# Nomeando as abas temáticas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Etapas de Ensino",
    "📊 Faixa Etária e Sexo",
    "📊 Formação Acadêmica",
    "📊 Vínculo Funcional",
    "📊 Dependência e Localização"
])

# --- ABA 1: ETAPAS DE ENSINO ---

with tab1:
    st.markdown("#### Docentes por Etapa de Ensino")
    df_etapas = dfs["etapas"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c1 = st.container(border=True)
    c1.markdown("1. Análise Descritiva da Base de Dados")
    tabela_descritiva = df_etapas.describe()
    c1.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

    # --- REQUISITO 2: Gráfico de Barras ---
    c2 = st.container(border=True)
    c2.markdown("2. Gráfico de Docentes por Etapa de Ensino")
    c2.markdown("O gráfico abaixo mostra o total de docentes em cada etapa de ensino para todo o estado, de acordo com o ano selecionado.")

    # Adicionando um filtro simples para o usuário poder escolher o ano
    ano_selecionado = c2.selectbox(
        "Selecione o Ano para visualizar no gráfico:",
        options=sorted(df_etapas['Ano'].unique(), reverse=True)
    )

    # Filtramos os dados pelo ano que o usuário escolheu
    df_filtrado_ano = df_etapas[df_etapas['Ano'] == ano_selecionado]

    # Selecionando apenas as colunas que representam as etapas de ensino
    colunas_etapas = ['Creche', 'Pré-Escola', 'EF - Anos Iniciais', 'EF - Anos Finais', 'EM Propedêutico', 'EM Integrado']
    
    # Somando o total de docentes para cada etapa
    total_por_etapa = df_filtrado_ano[colunas_etapas].sum()

    # Criando espaçamento entre o filtro e o gráfico
    c2.write("")

    # Usando o bar_chart(), como sugerido
    c2.bar_chart(total_por_etapa)
    
    c2.info("Este gráfico mostra a soma de todos os municípios para o ano selecionado.")


# --- ABA 2: FAIXA ETÁRIA E SEXO ---
with tab2:
    st.markdown("#### Docentes por Faixa Etária e Sexo")
    df_idade = dfs["idade"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c3 = st.container(border=True)
    c3.markdown("1. Análise Descritiva da Base de Dados")
    tabela_descritiva = df_idade.describe()
    c3.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

# --- ABA 3: NÍVEL DE FORMAÇÃO ---
with tab3:
    st.markdown("#### Docentes por Escolaridade ou Nível de Formação Acadêmica")
    df_formacao = dfs["formacao"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c5 = st.container(border=True)
    c5.markdown("1. Análise Descritiva da Base de Dados")
    tabela_descritiva = df_formacao.describe()
    c5.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

# --- ABA 4: VÍNCULO FUNCIONAL ---
with tab4:
    st.markdown("#### Docentes por Vínculo Funcional e Dependência Administrativa")
    df_vinculo = dfs["vinculo"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c7 = st.container(border=True)
    c7.markdown("1. Análise Descritiva da Base de Dados")
    tabela_descritiva = df_vinculo.describe()
    c7.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

# --- ABA 5: DEPENDÊNCIA E LOCALIZAÇÃO ---
with tab5:
    st.markdown("#### Docentes por Dependência Administrativa e Localização")
    df_dependencia = dfs["dependencia"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c9 = st.container(border=True)
    c9.markdown("1. Análise Descritiva da Base de Dados")
    tabela_descritiva = df_dependencia.describe()
    c9.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")


# Rodapé
st.markdown("---")
st.write("© 2025 DocentES. Com Dados do Censo Escolar, de 2022 a 2024. Todos os direitos reservados.")