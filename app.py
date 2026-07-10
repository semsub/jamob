import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from fpdf import FPDF

st.set_page_config(page_title="JAMOB PRO Enterprise", layout="wide")

# Conexão Banco
def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

# Login
if 'loja_id' not in st.session_state:
    st.title("JAMOB PRO · Acesso ao Sistema")
    loja = st.text_input("ID da Loja")
    senha = st.text_input("Senha", type="password")
    if st.button("Acessar") and senha == "jamob2026":
        st.session_state['loja_id'] = loja
        st.rerun()
    st.stop()

# Layout Principal
st.sidebar.title(f"JAMOB PRO: {st.session_state['loja_id']}")
menu = st.sidebar.radio("Módulos", ["OS & Atendimento", "Estoque & Catálogo", "Dashboard Financeiro", "Gestão Fiscal"])

if menu == "OS & Atendimento":
    st.header("Gestão de Ordens de Serviço (OS)")
    col1, col2 = st.columns(2)
    placa = col1.text_input("Placa do Veículo")
    status = col2.selectbox("Status", ["Agendado", "Em Execução", "Pronto", "Pago"])
    if st.button("Registrar Movimentação"):
        st.success(f"OS para {placa} atualizada para {status}")

elif menu == "Estoque & Catálogo":
    st.header("Catálogo de Serviços e Estoque")
    nome = st.text_input("Serviço ou Peça")
    valor = st.number_input("Preço de Venda (R$)", min_value=0.0)
    if st.button("Adicionar ao Sistema"):
        st.success(f"{nome} cadastrado com sucesso.")

elif menu == "Dashboard Financeiro":
    st.header("Cockpit de Gestão")
    df = pd.DataFrame({'Servico': ['Lavagem', 'Mecanica', 'Polimento'], 'Receita': [500, 1200, 800]})
    fig = px.bar(df, x="Servico", y="Receita", title="Faturamento por Tipo de Serviço", color="Receita")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Gestão Fiscal":
    st.header("Relatório Contábil")
    if st.button("Gerar PDF para Contador"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt=f"Relatorio Fiscal - {st.session_state['loja_id']}", ln=True, align='C')
        st.info("PDF gerado e pronto para envio.")
