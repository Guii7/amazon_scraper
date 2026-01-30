import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', 5432),
    database=os.getenv('POSTGRES_DB', 'n8n'),
    user=os.getenv('POSTGRES_USER', 'n8n_user'),
    password=os.getenv('POSTGRES_PASSWORD', '')
)
cur = conn.cursor()
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'amazon_offers'
    ORDER BY ordinal_position
""")
print("COLUNAS EXISTENTES NA TABELA amazon_offers:")
print("-" * 70)
for r in cur.fetchall():
    print(f'{r[0]:30} | {r[1]:20} | {r[2]}')
conn.close()
