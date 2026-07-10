import os
import logging
from datetime import datetime, timezone
from decimal import Decimal
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv(dotenv_path='.env')
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("JAMOB")

def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")

def registrar_entrada(placa, modelo):
    placa = placa.strip().upper()
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO veiculos (placa, modelo) VALUES (%s, %s);", (placa, modelo))
            conn.commit()
    return f"✔ Veículo {placa} registrado com sucesso."

def registrar_saida(placa):
    placa = placa.strip().upper()
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM veiculos WHERE placa = %s;", (placa,))
            v = cur.fetchone()
            if not v: return "✘ Veículo não encontrado."
            
            tempo = int((datetime.now(timezone.utc) - v['hora_entrada']).total_seconds() // 60)
            valor = max(Decimal("0.15") * tempo, Decimal("5.00")).quantize(Decimal("0.01"))
            
            cur.execute("INSERT INTO historico (placa, modelo, hora_entrada, hora_saida, permanencia_min, valor_cobrado) VALUES (%s, %s, %s, %s, %s, %s);",
                        (v['placa'], v['modelo'], v['hora_entrada'], datetime.now(timezone.utc), tempo, valor))
            cur.execute("DELETE FROM veiculos WHERE id = %s;", (v['id'],))
            conn.commit()
            return f"✔ Saída: {placa} | Tempo: {tempo}min | Valor: R$ {valor}"

def relatorio_financeiro():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(valor_cobrado) FROM historico;")
            total = cur.fetchone()[0] or 0
            return f"💰 Faturamento Total Acumulado: R$ {total:.2f}"

def main():
    while True:
        print("\n--- JAMOB · Gestão Inteligente ---")
        print("1) Entrada | 2) Saída | 3) Pátio | 4) Financeiro | 0) Sair")
        op = input("Opção → ")
        try:
            if op == "1": print(registrar_entrada(input("Placa: "), input("Modelo: ")))
            elif op == "2": print(registrar_saida(input("Placa: ")))
            elif op == "3": 
                with get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT placa, modelo FROM veiculos;")
                        for row in cur.fetchall(): print(f"🚗 {row[0]} - {row[1]}")
            elif op == "4": print(relatorio_financeiro())
            elif op == "0": break
        except Exception as e: print(f"Erro no sistema: {e}")

if __name__ == "__main__":
    main()
