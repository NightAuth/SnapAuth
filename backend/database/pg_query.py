
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


HOST = os.getenv('HOST')
DBNAME = os.getenv('DBNAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('DB_PASSWORD')


conn = psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD)
cur = conn.cursor()
    

try:
    cur.execute("""
                
                
                
                
                """)
    
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()