import streamlit as st

# Colocando a página em modo wide
st.set_page_config(layout="wide")

# Criando uma sidebar
st.sidebar.title("Menu")
with st.sidebar:
    st.write("Opções de navegação")
    option = st.selectbox("Escolha uma opção:", ["Início", "Sobre", "Contato"])

# Carregar os dados a partir dos inputs nos widgets da sidebar
st.sidebar.write(f"Você selecionou: {option}")

# Conteúdo principal da página

# Título da página
st.title("👩🏾‍🏫 DocentES 👨🏻‍🏫")
st.write("Bem-vindo ao DocentES, a plataforma sobre os Docentes do Espírito Santo!")
st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhWSVR_PA-xWPXwdQ5qyRDWAZZdVA1JhdQuaT6yI926pYTAg0boScUh3J-lsiu1i3KDyHJQmN_OgNx6HX4Zun6XDIRfqNXJe8CdyKcnwDymZp8P52JvRrKav0otT263CjHKyS_RitA5VPJFOg6NJ-uqRwuksj2r_J1mna9CnfEVq4psg-QMaH4bq2Uy2w/w485-h335/fc-removebg-preview.png", width=100)
st.write("Aqui você pode explorar dados sobre os professores do estado, incluindo informações demográficas, formação acadêmica, e muito mais.")
st.write("Use o menu à esquerda para navegar entre as diferentes seções do site.")

# Criando primeira seção vertical
st.header("Docentes por etapa e dependência administrativa, segundo o município")
# Criando estrutura com duas colunas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Docentes por etapa, segundo o município")
    st.write("Conteúdo da seção 1")
with col2:
    st.subheader("Docentes por dependência administrativa, segundo o município")
    st.write("Conteúdo da seção 2")

# Criando segunda seção vertical
st.header("Docentes por gênero e faixa etária, segundo o município")
# Criando estrutura com duas colunas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Docentes por gênero, segundo o município")
    st.write("Conteúdo da seção 1")
with col2:
    st.subheader("Docentes por faixa etária, segundo o município")
    st.write("Conteúdo da seção 2")

# Criando terceira seção vertical
st.header("Docentes por nível de escolaridade e formação acadêmica, segundo o município")
# Criando estrutura com duas colunas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Docentes por nível de escolaridade, segundo o município")
    st.write("Conteúdo da seção 1")
with col2:
    st.subheader("Docentes por formação acadêmica, segundo o município")
    st.write("Conteúdo da seção 2")

# Criando quarta seção vertical
st.header("Docentes por situação funcional e dependência administrativa, segundo o município")
# Criando estrutura com duas colunas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Docentes por situação funcional, segundo o município")
    st.write("Conteúdo da seção 1")
with col2:
    st.subheader("Docentes por dependência administrativa, segundo o município")
    st.write("Conteúdo da seção 2")

# Rodapé
st.markdown("---")
st.write("© 2024 DocentES. Com Dados do Censo Escolar 2024. Todos os direitos reservados.")