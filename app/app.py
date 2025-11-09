from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)

# Configuration de la connexion PostgreSQL
DB_CONFIG = {
    "host": "host.docker.internal",
    "database": "mydb",
    "user": "myuser",
    "password": "pass1234",
    "port": 5432
}

def get_connection():
    """Crée une connexion à la base PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Page principale avec le formulaire et la liste des utilisateurs."""
    conn = get_connection()
    cur = conn.cursor()

    # Si le formulaire est soumis
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')  # redirige vers la page principale après insertion

    # Sinon, afficher la liste des utilisateurs
    cur.execute("SELECT * FROM users ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', users=rows)

if __name__ == '__main__':
    # L'application tourne sur le port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)