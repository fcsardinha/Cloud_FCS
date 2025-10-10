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

# Será usado o dataframe de 'etapas' como base para criar os filtros.

# Cabeçalho da sidebar
st.sidebar.header("⚙️ Filtros")
st.sidebar.markdown("Use os filtros abaixo para selecionar o ano e o município desejados.")

# --- Filtro de Ano ---
ano_selecionado = st.sidebar.selectbox(
    "Selecione o Ano",
    options=sorted(
                    dfs['etapas']['Ano'].unique(), 
                    reverse=True
                  )
)

# --- Filtro de Município ---
# Criando a opção geral
opcao_geral = ["Todos os Municípios"]
# Criando uma lista ordenada dos municípios
lista_municipios = sorted(
    dfs['etapas']['Município'].unique(),
    key=normalizar_para_ordenacao # Usando a função de normalização
    )
# Juntando as duas listas!
opcoes_municipios = opcao_geral + lista_municipios

# Usamos a nova lista completa como opções do selectbox
municipio_selecionado = st.sidebar.selectbox(
    "Selecione o Município",
    options=opcoes_municipios
)

# Conteúdo principal do app

# Título da página
st.title("👩🏾‍🏫 DocentES 👨🏻‍🏫")
st.write("Bem-vindo ao DocentES, a plataforma sobre os Docentes do Espírito Santo!")

# Estrutura com duas colunas para alinhar a imagem
col1, col2 = st.columns([1,2])
with col2:
    st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhWSVR_PA-xWPXwdQ5qyRDWAZZdVA1JhdQuaT6yI926pYTAg0boScUh3J-lsiu1i3KDyHJQmN_OgNx6HX4Zun6XDIRfqNXJe8CdyKcnwDymZp8P52JvRrKav0otT263CjHKyS_RitA5VPJFOg6NJ-uqRwuksj2r_J1mna9CnfEVq4psg-QMaH4bq2Uy2w/w485-h335/fc-removebg-preview.png", width=400)


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
    c1.markdown("1. Análise Descritiva da Base de Dados (todo o Estado)")
    tabela_descritiva = df_etapas.drop(columns=['Ano','Código do Município']).describe()
    c1.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

    # --- REQUISITO 2: Gráfico de Barras ---
    c2 = st.container(border=True)
    c2.markdown("2. Gráfico de Docentes por Etapa de Ensino")
    # Informação de filtros aplicados no gráfico
    c2.info(f"Local: {municipio_selecionado} | Ano: {ano_selecionado}")
    c2.write("") # Espaçamento
    # Selecionando as colunas para o gráfico
    colunas_etapas = ['Creche', 'Pré-Escola', 'EF - Anos Iniciais', 'EF - Anos Finais', 'EM Propedêutico', 'EM Integrado']
    # Estabelecendo a lógica para o gráfico, conforme o filtro de município
    if municipio_selecionado == "Todos os Municípios":
        # SE o usuário escolher ver o estado todo:
        # 1. Filtrar o DataFrame apenas pelo ano
        df_filtrado_ano = df_etapas[df_etapas['Ano'] == ano_selecionado]
        # 2. Somar os valores de todos os municípios
        dados_grafico = df_filtrado_ano[colunas_etapas].sum()

    else:
        # SENÃO (o usuário escolheu um município específico)...
        # 1. Filtrar o DataFrame pelo ano E pelo município
        df_filtrado = df_etapas[
            (df_etapas['Ano'] == ano_selecionado) &
            (df_etapas['Município'] == municipio_selecionado)
        ]
        # 2. Pegar os dados do município e transpor (.T) para o gráfico
        dados_grafico = df_filtrado[colunas_etapas].T

    # Gerando o gráfico
    c2.bar_chart(dados_grafico)


# --- ABA 2: FAIXA ETÁRIA E SEXO ---
with tab2:
    st.markdown("#### Docentes por Faixa Etária e Sexo")
    df_idade = dfs["idade"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c3 = st.container(border=True)
    c3.markdown("1. Análise Descritiva da Base de Dados (todo o Estado)")
    tabela_descritiva = df_idade.drop(columns=['Ano','Código do Município']).describe()
    c3.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

    # --- REQUISITO 2: Gráfico de Barras ---
    c4 = st.container(border=True)
    c4.markdown("2. Gráfico de Docentes por Faixa Etária e Sexo")
    # Informação de filtros aplicados no gráfico
    c4.info(f"Local: {municipio_selecionado} | Ano: {ano_selecionado}")
    
    c4.write("") # Espaçamento

    # Selecionando as colunas para o gráfico
    colunas_idade = ['Até 24 anos', 'De 25 a 29 anos', 'De 30 a 39 anos', 'De 40 a 49 anos', 'De 50 a 54 anos', 'De 55 a 59 anos', '60 anos ou mais']
    # Estabelecendo a lógica para o gráfico, conforme o filtro de município
    if municipio_selecionado == "Todos os Municípios":
        df_filtrado_ano = df_idade[df_idade['Ano'] == ano_selecionado]
        dados_base = df_filtrado_ano.groupby("Sexo")[colunas_idade].sum().reset_index()
    else:
        dados_base = df_idade[
            (df_idade['Ano'] == ano_selecionado) &
            (df_idade['Município'] == municipio_selecionado)
        ]

    # Reorganizando os dados com melt
    dados_longo = dados_base.melt(
        id_vars="Sexo", 
        value_vars=colunas_idade, 
        var_name="Faixa Etária", 
        value_name="Total de Docentes"
        )
    
    # Definindo a ordem correta das faixas etárias
    ordem_faixas = [
        'Até 24 anos', 
        'De 25 a 29 anos', 
        'De 30 a 39 anos', 
        'De 40 a 49 anos',
        'De 50 a 54 anos',
        'De 55 a 59 anos',
        '60 anos ou mais'
        ]
    # Convertendo 'Faixa Etária' em categoria com ordem definida
    dados_longo['Faixa Etária'] = pd.Categorical(
        dados_longo['Faixa Etária'], 
        categories=ordem_faixas,
        ordered=True
        )
    # Estrutura com duas colunas para alinhar a imagem
    col3, col4 = c4.columns([1,2])
    with col3:
        # Definindo filtro por sexo
        sexo_selecionado = st.selectbox(
                "Selecione o Sexo:",
                options=["Todos", "Feminino", "Masculino"]
            )
    c4.write("") # Espaçamento
    if sexo_selecionado != "Todos":
        dados_grafico = dados_longo[dados_longo['Sexo'] == sexo_selecionado]
    else:
        dados_grafico = dados_longo
    
    if not dados_grafico.empty:
        c4.bar_chart(
            dados_grafico,
            x="Faixa Etária", 
            y="Total de Docentes", 
            color='Sexo'
            )
    else:
        c4.warning("Nenhum dado disponível para os filtros selecionados.")

# --- ABA 3: NÍVEL DE FORMAÇÃO ---
with tab3:
    st.markdown("#### Docentes por Escolaridade ou Nível de Formação Acadêmica")
    df_formacao = dfs["formacao"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c5 = st.container(border=True)
    c5.markdown("1. Análise Descritiva da Base de Dados (todo o Estado)")
    tabela_descritiva = df_formacao.drop(columns=['Ano','Código do Município']).describe()
    c5.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

    # --- REQUISITO 2: Gráfico de Barras ---
    c6 = st.container(border=True)
    c6.markdown("2. Gráfico de Docentes por Formação Acadêmica")
    # Informação de filtros aplicados no gráfico
    c6.info(f"Local: {municipio_selecionado} | Ano: {ano_selecionado}")
    
    c6.write("") # Espaçamento

    # Selecionando as colunas para o gráfico
    colunas_formacao = [
        'Ensino Fundamental', 'Ensino Médio', 'Graduação - Licenciatura',
        'Graduação - Sem Licenciatura', 'Especialização', 'Mestrado', 'Doutorado'
    ]
    
    # Definindo a ordem lógica para as barras do gráfico
    ordem_grafico = [
        'Ensino Fundamental', 
        'Ensino Médio', 
        'Graduação - Licenciatura',
        'Graduação - Sem Licenciatura', 
        'Especialização', 
        'Mestrado', 
        'Doutorado'
    ]

    if municipio_selecionado == "Todos os Municípios":
        # SE o usuário escolheu ver o estado todo...
        df_filtrado_ano = df_formacao[df_formacao['Ano'] == ano_selecionado]
        # Somamos os valores de todos os municípios
        dados_soma = df_filtrado_ano[colunas_formacao].sum()
        # Reordenamos os dados de acordo com nossa lista
        dados_grafico = dados_soma.reindex(ordem_grafico)

    else:
        # SENÃO (o usuário escolheu um município específico)...
        df_filtrado = df_formacao[
            (df_formacao['Ano'] == ano_selecionado) &
            (df_formacao['Município'] == municipio_selecionado)
        ]
        # Transpondo os dados
        dados_transpostos = df_filtrado[colunas_formacao].T
        # Reordenando o índice (formações) de acordo com a lista
        dados_grafico = dados_transpostos.reindex(ordem_grafico)

    # Exibindo o gráfico
    c6.bar_chart(dados_grafico)

# --- ABA 4: VÍNCULO FUNCIONAL ---
with tab4:
    st.markdown("#### Docentes por Vínculo Funcional e Dependência Administrativa")
    df_vinculo = dfs["vinculo"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c7 = st.container(border=True)
    c7.markdown("1. Análise Descritiva da Base de Dados (todo o Estado)")
    tabela_descritiva = df_vinculo.describe()
    c7.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")

    # --- REQUISITO 2: Gráfico de Barras ---
    c8 = st.container(border=True)
    c8.markdown("2. Gráfico de Docentes por Vínculo Funcional e Dependência Administrativa")
    # Informação de filtros aplicados no gráfico
    c8.info(f"Local: {municipio_selecionado} | Ano: {ano_selecionado}")
    
    c8.write("") # Espaçamento
    
    # Preparando os dados base (Estado ou Município)
    if municipio_selecionado == "Todos os Municípios":
        df_filtrado_ano = df_vinculo[df_vinculo['Ano'] == ano_selecionado]
        # Agrupando por Vínculo para ter a soma correta por categoria
        dados_base = df_filtrado_ano.groupby('Vínculo Funcional').sum(numeric_only=True).reset_index()
    else:
        # Para município específico, apenas filtramos
        dados_base = df_vinculo[
            (df_vinculo['Ano'] == ano_selecionado) &
            (df_vinculo['Município'] == municipio_selecionado)
        ]

    # Criando o filtro por Vínculo Funcional
    lista_vinculos = dados_base['Vínculo Funcional'].unique().tolist()
    
    col_5, col_6 = c8.columns([1, 2]) # Para o filtro não ocupar a tela toda
    with col_5:
        vinculo_selecionado = st.selectbox(
            "Selecione o Vínculo Funcional:",
            options=lista_vinculos
        )
    
    # Filtrando os dados pelo vínculo selecionado
    dados_filtrados_vinculo = dados_base[dados_base['Vínculo Funcional'] == vinculo_selecionado]

    # Preparando os dados finais para o bar_chart
    colunas_grafico = ['Federal', 'Estadual', 'Municipal']
    
    # Pegando apenas as colunas numéricas e transpomos (.T)
    # para que as dependências virem as barras do gráfico
    dados_para_plotar = dados_filtrados_vinculo[colunas_grafico].T

    # Exibindo o gráfico
    if not dados_para_plotar.empty:
        c8.bar_chart(dados_para_plotar)
    else:
        c8.warning("Nenhum dado encontrado para a seleção atual.")

# --- ABA 5: DEPENDÊNCIA E LOCALIZAÇÃO ---
with tab5:
    st.markdown("#### Docentes por Dependência Administrativa e Localização")
    df_dependencia = dfs["dependencia"]

    # Definindo containers dentro da aba

    # --- REQUISITO 1: Tabela Descritiva ---
    c9 = st.container(border=True)
    c9.markdown("1. Análise Descritiva da Base de Dados (todo o Estado)")
    tabela_descritiva = df_dependencia.describe()
    c9.write(tabela_descritiva)
 
    # Definindo espaçamento entre os containers
    st.write("")


    # --- REQUISITO 2: Gráfico de Barras
    c10 = st.container(border=True)
    c10.markdown("2. Gráfico de Docentes por Localização e Dependência Administrativa")
    # Informação de filtros aplicados no gráfico
    c10.info(f"Local: {municipio_selecionado} | Ano: {ano_selecionado}")
    
    c10.write("") # Espaçamento
    
    # Preparando os dados base (Estado ou Município) ---
    if municipio_selecionado == "Todos os Municípios":
        dados_base = df_dependencia[df_dependencia['Ano'] == ano_selecionado]
    else:
        dados_base = df_dependencia[
            (df_dependencia['Ano'] == ano_selecionado) &
            (df_dependencia['Município'] == municipio_selecionado)
        ]

    # Criando o filtro por Localização (Urbana, Rural)
    col_7, col_8 = c10.columns([1, 2])
    with col_7:
        localizacao_selecionada = st.selectbox(
            "Selecione a Localização:",
            options=["Todas", "Urbana", "Rural"],
            key="filtro_localizacao" # Chave fixa para evitar resetar a seleção ao interagir com outros filtros
        )

    # Preparando os dados finais para o bar_chart
    colunas_grafico = ['Federal', 'Estadual', 'Municipal', 'Privada']
    
    # Verificamos PRIMEIRO se a visão é estadual ou municipal
    if municipio_selecionado == "Todos os Municípios":
        # Se for estadual, a operação final é sempre uma SOMA.
        if localizacao_selecionada != "Todas":
            # Filtramos pela localização escolhida (Urbana ou Rural)
            dados_filtrados_loc = dados_base[dados_base['Localização'] == localizacao_selecionada]
        else:
            # Se for "Todas", usamos o dataframe base (com ambas as localizações)
            dados_filtrados_loc = dados_base
        
        # A operação final é somar tudo para ter o total do estado
        dados_para_plotar = dados_filtrados_loc[colunas_grafico].sum()

    else:
        # Se for municipal, a operação final é sempre uma TRANSPOSIÇÃO.
        if localizacao_selecionada != "Todas":
            # Filtramos pela localização (teremos 1 linha)
            dados_filtrados_loc = dados_base[dados_base['Localização'] == localizacao_selecionada]
            
            # Transpomos e renomeamos a coluna
            dados_transpostos = dados_filtrados_loc[colunas_grafico].T
            dados_transpostos.columns = ['Nº de Docentes']
            dados_para_plotar = dados_transpostos
        else:
            # Se for "Todas", primeiro somamos as linhas de Urbana e Rural daquele município
            # e depois transpomos.
            soma_municipio = dados_base[colunas_grafico].sum().to_frame(name='Nº de Docentes')
            dados_para_plotar = soma_municipio
        
    # Exibindo o gráfico
    if dados_para_plotar.empty:
        c10.warning("Nenhum dado encontrado para a seleção atual.")
    else:
        c10.bar_chart(dados_para_plotar)

# Rodapé
st.markdown("---")
st.write("© 2025 DocentES. Com Dados do Censo Escolar, de 2022 a 2024. Todos os direitos reservados.")