import streamlit as st
import psycopg2
import os
import pandas as pd
from datetime import datetime, timezone
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

# Configuração da Página
st.set_page_config(page_title="JAMOB SaaS", layout="wide")

# Login Simples (SaaS)
if 'loja_id' not in st.session_state:
    st.title("JAMOB · Acesso ao Sistema")
    loja = st.text_input("ID da Loja")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        # Em produção, substitua isso por consulta ao banco
        if loja and senha == "jamob2026":
            st.session_state['loja_id'] = loja
            st.rerun()
    st.stop()

# Função de Conexão
def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

st.sidebar.title(f"JAMOB · {st.session_state['loja_id']}")
if st.sidebar.button("Sair"):
    del st.session_state['loja_id']
    st.rerun()

menu = st.sidebar.radio("Navegação", ["Entrada", "Saída", "Pátio", "Financeiro"])

# Lógica do App
if menu == "Entrada":
    placa = st.text_input("Placa").upper()
    modelo = st.text_input("Modelo")
    if st.button("Confirmar Entrada"):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO veiculos (loja_id, placa, modelo) VALUES (%s, %s, %s);", (st.session_state['loja_id'], placa, modelo))
                conn.commit()
        st.success("Entrada registrada.")

elif menu == "Pátio":
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT placa, modelo, hora_entrada FROM veiculos WHERE loja_id = %s;", (st.session_state['loja_id'],))
            df = pd.DataFrame(cur.fetchall())
            if not df.empty: st.table(df)
            else: st.info("Pátio vazio.")

elif menu == "Financeiro":
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(valor_cobrado) FROM historico WHERE loja_id = %s;", (st.session_state['loja_id'],))
            total = cur.fetchone()[0] or 0
            st.metric("Faturamento Acumulado", f"R$ {total:.2f}")
            
            # Botão Exportar
            cur.execute("SELECT * FROM historico WHERE loja_id = %s;", (st.session_state['loja_id'],))
            df = pd.DataFrame(cur.fetchall())
            st.download_button("Baixar Relatório (CSV)", df.to_csv(), "relatorio.csv", "text/csv")
