import os
import time
import psycopg2
from psycopg2 import OperationalError

DATABASE_URL = os.getenv("SUPABASE_DB_URL")  # e.g. postgresql://user:pass@host:port/dbname

def keep_alive():
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
            conn.close()
            print("Supabase keep-alive ping successful")
        except OperationalError as e:
            print(f"Failed to ping Supabase: {e}")
        time.sleep(14 * 60)  # Sleep for 14 minutes

if __name__ == "__main__":
    keep_alive()


# this needs psycob2
# If you want to test outside Django, here’s a basic script you can run on your machine or server (requires psycopg2):