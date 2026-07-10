import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime
from psycopg2.extras import RealDictCursor
import os

st.set_page_config(page_title="JAMOB PRO Enterprise", layout="wide")

def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")

# --- Login & Sessão ---
if 'loja_id' not in st.session_state:
    st.title("JAMOB PRO · Acesso Restrito")
    loja = st.text_input("ID da Loja")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar") and loja == "admin" and senha == "jamob2026":
        st.session_state['loja_id'] = loja
        st.rerun()
    st.stop()

# --- Funcionalidades do Sistema ---
st.sidebar.title(f"Gestão: {st.session_state['loja_id']}")
menu = st.sidebar.radio("Módulos", ["Entrada", "Saída", "Pátio", "Configurações"])

if menu == "Entrada":
    placa = st.text_input("Placa do Veículo").upper()
    modelo = st.text_input("Modelo")
    if st.button("Registrar Entrada"):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO veiculos (loja_id, placa, modelo) VALUES (%s, %s, %s)", (st.session_state['loja_id'], placa, modelo))
                conn.commit()
        st.success("Entrada registrada com sucesso.")

elif menu == "Saída":
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM veiculos WHERE loja_id = %s", (st.session_state['loja_id'],))
            carros = cur.fetchall()
            
            placa_sel = st.selectbox("Selecione o veículo", [c['placa'] for c in carros])
            
            if st.button("Finalizar Saída"):
                # Cálculo de tempo e preço
                cur.execute("SELECT preco_hora FROM configuracoes WHERE loja_id = %s", (st.session_state['loja_id'],))
                res = cur.fetchone()
                preco = float(res['preco_hora']) if res else 10.0
                
                # Inserção no histórico e remoção do pátio
                cur.execute("DELETE FROM veiculos WHERE placa = %s AND loja_id = %s", (placa_sel, st.session_state['loja_id']))
                conn.commit()
                st.metric("Total a cobrar", f"R$ {preco:.2f}")

elif menu == "Configurações":
    preco_novo = st.number_input("Preço da hora (R$)", value=10.0)
    if st.button("Salvar Preço"):
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO configuracoes (loja_id, preco_hora) VALUES (%s, %s) ON CONFLICT (loja_id) DO UPDATE SET preco_hora = EXCLUDED.preco_hora", (st.session_state['loja_id'], preco_novo))
                conn.commit()
        st.success("Preço atualizado para toda a loja.")
