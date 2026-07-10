import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="JAMOB PRO Enterprise", layout="wide")

# Função de Conexão
def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

# --- Interface com Logo e Mascote ---
with st.sidebar:
    # AQUI ESTÁ A INTEGRAÇÃO DAS IMAGENS
    st.image("jamob.png", use_column_width=True)
    st.image("mascote_jamob.png", use_column_width=True)
    st.title("JAMOB PRO")
    menu = st.radio("Módulos", ["Visão Geral", "OS & Atendimento", "Estoque & Catálogo", "Financeiro & Fiscal"])

# --- Lógica do Sistema ---
if menu == "Visão Geral":
    st.header("Cockpit de Gestão")
    col1, col2, col3 = st.columns(3)
    col1.metric("OS Abertas", "12")
    col2.metric("Faturamento Mensal", "R$ 15.450,00")
    col3.metric("Eficiência", "98%")
    
    # Gráfico Plotly
    df = pd.DataFrame({"Serviço": ["Lavagem", "Mecânica", "Polimento"], "Receita": [2500, 8000, 4950]})
    fig = px.pie(df, values='Receita', names='Serviço', title="Distribuição por Receita")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "OS & Atendimento":
    st.header("Gestão de Ordens de Serviço")
    placa = st.text_input("Placa do Veículo")
    if st.button("Abrir nova OS"):
        st.success(f"OS aberta para {placa}!")

elif menu == "Estoque & Catálogo":
    st.header("Gerenciador de Peças e Serviços")
    st.write("Cadastre seus itens para automatizar as baixas.")

elif menu == "Financeiro & Fiscal":
    st.header("Relatório para Contador")
    if st.button("Gerar PDF Oficial"):
        st.info("Relatório PDF gerado com sucesso!")

# AVISO DE SEGURANÇA
st.sidebar.markdown("---")
st.sidebar.write("JAMOB PRO - Gestão Inteligente")
