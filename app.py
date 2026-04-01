import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from supabase import create_client, Client

# Charger les variables d'environnement (optionnel, tu peux les mettre en dur pour le test)
load_dotenv()

app = Flask(__name__)

# Configuration Supabase
url = "https://uwwtqcnwozpcnfswhziq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3d3RxY253b3pwY25mc3doemlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUwMzk1NjIsImV4cCI6MjA5MDYxNTU2Mn0.ycbt3azHdlsJN1i0mwv3ntyCTnc6-zPP3Dvyje7ak_U"
supabase: Client = create_client(url, key)

# --- ROUTES CRUD ---

# 1. Créer une tâche (CREATE)
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    title = data.get('title')
    
    # Insertion dans Supabase
    response = supabase.table("tasks").insert({"title": title}).execute()
    return jsonify(response.data), 201

# 2. Lire toutes les tâches (READ)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = supabase.table("tasks").select("*").execute()
    return jsonify(response.data)

# 3. Mettre à jour une tâche (UPDATE)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    completed = data.get('completed')
    
    response = supabase.table("tasks").update({"completed": completed}).eq("id", task_id).execute()
    return jsonify(response.data)

# 4. Supprimer une tâche (DELETE)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    response = supabase.table("tasks").delete().eq("id", task_id).execute()
    return jsonify({"message": "Tâche supprimée", "data": response.data})

if __name__ == '__main__':
    app.run(debug=True, port=5001)