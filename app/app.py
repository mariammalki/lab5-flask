import os
import time
from flask import Flask, request, redirect, url_for, render_template
import psycopg
from psycopg.rows import dict_row

DB_HOST = os.environ.get('DB_HOST', 'host.docker.internal')
DB_NAME = os.environ.get('DB_NAME', 'mydb')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'pass1234')
DB_PORT = int(os.environ.get('DB_PORT', '5432'))

app = Flask(__name__)

def get_conn():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        connect_timeout=3,
    )

def wait_for_db(max_attempts=30, delay_seconds=2):
    last_err = None
    for i in range(1, max_attempts + 1):
        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return
        except Exception as e:
            last_err = e
            print(f"[init] DB pas prête (tentative {i}/{max_attempts}) : {e}")
            time.sleep(delay_seconds)
    raise RuntimeError(f"Impossible de se connecter à la DB après {max_attempts} tentatives : {last_err}")

def init_db():
    wait_for_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                );
            """)
        conn.commit()
    print("[init] Table 'contacts' OK")

@app.route("/healthz")
def healthz():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return "ok", 200
    except Exception as e:
        return str(e), 500

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if name and email:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (name, email) VALUES (%s, %s)",
                        (name, email),
                    )
                conn.commit()
        return redirect(url_for("index"))

    with get_conn() as conn:
        # row_factory pour avoir des dicts (équivalent DictCursor)
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT name, email FROM users ORDER BY id DESC")
            rows = cur.fetchall()
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)