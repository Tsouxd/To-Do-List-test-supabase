import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

# Configuration Supabase
url = "https://uwwtqcnwozpcnfswhziq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3d3RxY253b3pwY25mc3doemlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUwMzk1NjIsImV4cCI6MjA5MDYxNTU2Mn0.ycbt3azHdlsJN1i0mwv3ntyCTnc6-zPP3Dvyje7ak_U"
supabase: Client = create_client(url, key)

# --- ROUTES ---

# LIRE (Afficher l'interface)
@app.route('/')
def index():
    # On récupère les tâches triées par ID
    response = supabase.table("tasks").select("*").order("id").execute()
    tasks = response.data
    return render_template('index.html', tasks=tasks)

# CRÉER
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        supabase.table("tasks").insert({"title": title}).execute()
    return redirect(url_for('index'))

# METTRE À JOUR (Statut terminé)
@app.route('/update/<int:task_id>/<string:status>')
def update(task_id, status):
    new_status = (status == 'true')
    supabase.table("tasks").update({"completed": new_status}).eq("id", task_id).execute()
    return redirect(url_for('index'))

# SUPPRIMER
@app.route('/delete/<int:task_id>')
def delete(task_id):
    supabase.table("tasks").delete().eq("id", task_id).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)