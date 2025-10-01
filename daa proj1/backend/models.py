import json
import networkx as nx
from networkx.algorithms import bipartite

class RecipeGraph:
    def __init__(self, recipes_file):
        with open(recipes_file, 'r') as f:
            self.recipes = json.load(f)
        self.graph = nx.Graph()
        self.build_graph()

    def build_graph(self):
        for recipe in self.recipes:
            recipe_node = f"recipe_{recipe['name']}"
            self.graph.add_node(recipe_node, type='recipe')
            for ing in recipe['ingredients']:
                ing_node = f"ing_{ing}"
                self.graph.add_node(ing_node, type='ingredient')
                self.graph.add_edge(recipe_node, ing_node)

    def get_recipes(self):
        return [node for node, data in self.graph.nodes(data=True) if data['type'] == 'recipe']

    def get_ingredients_for_recipe(self, recipe_node):
        return [n for n in self.graph.neighbors(recipe_node) if self.graph.nodes[n]['type'] == 'ingredient']

    def get_recipes_for_ingredient(self, ing_node):
        return [n for n in self.graph.neighbors(ing_node) if self.graph.nodes[n]['type'] == 'recipe']
