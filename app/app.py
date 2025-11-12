from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# 🔧 Configuration PostgreSQL via variables d'environnement
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db-service"),  
    "database": os.environ.get("DB_NAME", "mydb"),
    "user": os.environ.get("DB_USER", "myuser"),
    "password": os.environ.get("DB_PASSWORD", "pass1234"),
    "port": int(os.environ.get("DB_PORT", 5432))
}

def get_connection():
    """Crée une connexion à la base PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page principale avec le formulaire et la liste des utilisateurs."""
    conn = get_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if name and email:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                (name, email)
            )
            conn.commit()
        return redirect('/')

    cur.execute("SELECT * FROM users ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', users=rows)

if __name__ == '__main__':
   
    app.run(host='0.0.0.0', port=5000, debug=True)
