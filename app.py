import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Renda per Capita", layout="wide")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Dados_Pib.xlsx")  # Nome correto do seu arquivo
    return df

# Carregar os dados
df = carregar_dados()

# Título
st.title("📊 Dashboard de PIB per Capita no Brasil")

# Filtros laterais
estados = df["Estado"].unique()
anos = sorted(df["Ano"].unique())

estado_selecionado = st.sidebar.selectbox("Selecione o Estado", estados)
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos)

# Filtrar dados
df_filtrado = df[(df["Estado"] == estado_selecionado) & (df["Ano"] == ano_selecionado)]

# Métricas
col1, col2 = st.columns(2)
col1.metric("💰 PIB per Capita", f"R${df_filtrado['PIB per capita'].mean():,.2f}")
col2.metric("📅 Ano", int(ano_selecionado))

# Gráfico de linha do tempo do estado selecionado
df_linha = df[df["Estado"] == estado_selecionado]
fig = px.line(df_linha, x="Ano", y="PIB per capita", title=f"Evolução do PIB per Capita em {estado_selecionado}",
              markers=True, labels={"PIB per capita": "PIB per capita (R$)"})
st.plotly_chart(fig, use_container_width=True)

# Gráfico comparando estados no ano selecionado
df_ano = df[df["Ano"] == ano_selecionado]
fig2 = px.bar(df_ano.sort_values("PIB per capita", ascending=False), 
              x="Estado", y="PIB per capita", 
              title=f"PIB per Capita por Estado em {ano_selecionado}",
              labels={"PIB per capita": "PIB per capita (R$)"})
st.plotly_chart(fig2, use_container_width=True)
