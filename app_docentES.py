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

st.subheader(f"Exibindo dados para: {municipio_selecionado} ({ano_selecionado})")

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
  
    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c1 = st.container(border=True)
    c1.markdown("1. Análise Descritiva da Base de Dados")
    tabela_descritiva = dfs["etapas"].describe()
    c1.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

    c2 = st.container(border=True)
    c2.write("Conteúdo dentro do container 2")

with tab2:
    st.header("Docentes por gênero e faixa etária, segundo o município")
    st.write("Conteúdo da aba 2")

with tab3:
    st.header("Docentes por nível de escolaridade e formação acadêmica, segundo o município")
    st.write("Conteúdo da aba 3")

with tab4:
    st.header("Docentes por nível de escolaridade e formação acadêmica, segundo o município")
    st.write("Conteúdo da aba 3")

with tab5:
    st.header("Docentes por situação funcional e dependência administrativa, segundo o município")
    st.write("Conteúdo da aba 4")


# Rodapé
st.markdown("---")
st.write("© 2024 DocentES. Com Dados do Censo Escolar 2024. Todos os direitos reservados.")