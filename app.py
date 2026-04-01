import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv # Import pour charger le .env
from supabase import create_client, Client

# Charger les variables d'environnement du fichier .env
load_dotenv()

app = Flask(__name__)

# Récupération des variables d'environnement
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Initialisation du client Supabase
if not url or not key:
    print("Erreur: Les variables d'environnement SUPABASE_URL ou SUPABASE_KEY sont manquantes.")
else:
    supabase: Client = create_client(url, key)

# --- ROUTES ---

@app.route('/')
def index():
    # On récupère les tâches triées par ID
    response = supabase.table("tasks").select("*").order("id").execute()
    tasks = response.data
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        supabase.table("tasks").insert({"title": title}).execute()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>/<string:status>')
def update(task_id, status):
    new_status = (status == 'true')
    supabase.table("tasks").update({"completed": new_status}).eq("id", task_id).execute()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    supabase.table("tasks").delete().eq("id", task_id).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Rappel : utilise port=5001 si le port 5000 est déjà pris par ton système
    app.run(debug=True, port=5000)