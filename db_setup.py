import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    cur = conn.cursor()
    
    # Tabelas com isolamento por loja_id
    cur.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id SERIAL PRIMARY KEY,
        loja_id VARCHAR(50) NOT NULL,
        placa VARCHAR(10) NOT NULL,
        modelo VARCHAR(50),
        hora_entrada TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS historico (
        id SERIAL PRIMARY KEY,
        loja_id VARCHAR(50) NOT NULL,
        placa VARCHAR(10),
        modelo VARCHAR(50),
        hora_entrada TIMESTAMP WITH TIME ZONE,
        hora_saida TIMESTAMP WITH TIME ZONE,
        permanencia_min INTEGER,
        valor_cobrado DECIMAL(10,2)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Banco de dados JAMOB configurado com sucesso!")

if __name__ == "__main__":
    setup()
