import os
import sys
import psycopg2

# Read database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print(f"Trying to connect to PostgreSQL at {DB_HOST}:{DB_PORT} ...")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5
    )
    print("✅ Connection successful!")
    conn.close()
except psycopg2.OperationalError as e:
    print("❌ OperationalError:", e)
except Exception as e:
    print("❌ Unexpected error:", e)

sys.exit(0)