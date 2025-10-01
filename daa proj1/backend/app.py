from flask import Flask, request, jsonify, send_from_directory
from models import RecipeGraph
from algorithms import suggest_recipes
import os

app = Flask(__name__)
recipes_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')
graph = RecipeGraph(recipes_file)

@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'frontend'), path)

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    available_ings = data.get('ingredients', [])
    suggestions = suggest_recipes(graph, available_ings)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
