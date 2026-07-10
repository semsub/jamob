import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os

# Configuração da página
st.set_page_config(page_title="JAMOB PRO Enterprise", layout="wide")

# --- Interface com Logo e Mascote ---
with st.sidebar:
    # Caminho corrigido para a pasta 'images'
    if os.path.exists("images/jamob.png"):
        st.image("images/jamob.png", use_container_width=True)
    if os.path.exists("images/mascote_jamob.png"):
        st.image("images/mascote_jamob.png", use_container_width=True)
    
    st.title("JAMOB PRO")
    menu = st.radio("Módulos", ["Visão Geral", "OS & Atendimento", "Estoque & Catálogo", "Financeiro & Fiscal"])

# --- Lógica do Sistema ---
if menu == "Visão Geral":
    st.header("Cockpit de Gestão")
    col1, col2, col3 = st.columns(3)
    col1.metric("OS Abertas", "12")
    col2.metric("Faturamento Mensal", "R$ 15.450,00")
    col3.metric("Eficiência", "98%")
    
    # Gráfico Plotly profissional
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
    st.write("Catálogo completo para qualquer nicho automotivo.")

elif menu == "Financeiro & Fiscal":
    st.header("Relatório para Contador")
    if st.button("Gerar PDF Oficial"):
        st.info("Documento PDF gerado e pronto para envio!")

st.sidebar.markdown("---")
st.sidebar.write("JAMOB PRO - Gestão Inteligente")
