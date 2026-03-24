from environs import Env
import psycopg2
from psycopg2.extras import Json

env = Env()
env.read_env()

def get_db_connection():
    # Heroku automatically sets DATABASE_URL
    conn = psycopg2.connect(env.str("DATABASE_URL"), sslmode='require')
    return conn

def check_cache(data_hash, topic, func_name):
    key = f"{data_hash}_{topic}_{func_name}"
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT response FROM guyana_budget_llm_cache WHERE cache_key = %s", (key,))
    result = cur.fetchone()
    
    cur.close()
    conn.close()
    return result[0] if result else None

def save_to_cache(data_hash, topic, func_name, response):
    key = f"{data_hash}_{topic}_{func_name}"
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO guyana_budget_llm_cache (cache_key, response) VALUES (%s, %s) ON CONFLICT (cache_key) DO UPDATE SET response = EXCLUDED.response",
        (key, Json(response))
    )
    
    conn.commit()
    cur.close()
    conn.close()