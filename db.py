import psycopg2
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv('PGDATABASE'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST'),
        port='5432'
    )
