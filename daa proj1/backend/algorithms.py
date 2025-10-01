from collections import defaultdict


def suggest_recipes(graph, available_ings, max_suggestions=5):
    """
    Suggest recipes based on available ingredients.
    Use greedy: Sort by match percentage.
    """
    available_set = set(available_ings)
    suggestions = []
    for recipe_node in graph.get_recipes():
        recipe_name = recipe_node.replace('recipe_', '')
        ings = [n.replace('ing_', '')
                for n in graph.get_ingredients_for_recipe(recipe_node)]
        ing_set = set(ings)
        matched = ing_set & available_set
        missing = ing_set - available_set
        match_pct = len(matched) / len(ing_set) if ing_set else 0
        if match_pct > 0:
            subs = suggest_substitutions(graph, missing, available_ings)
            suggestions.append({
                'name': recipe_name,
                'match_pct': match_pct,
                'matched_ings': list(matched),
                'missing_ings': list(missing),
                'substitutions': subs
            })
    # Sort by match_pct descending
    suggestions.sort(key=lambda x: x['match_pct'], reverse=True)
    return suggestions[:max_suggestions]


def suggest_substitutions(graph, missing_ings, available_ings):
    """
    Greedy: For each missing, find a substitute from available that shares recipes.
    """
    subs = {}
    available_set = set(available_ings)
    for miss in missing_ings:
        miss_node = f"ing_{miss}"
        if not graph.graph.has_node(miss_node):
            continue
        candidates = []
        for recipe in graph.get_recipes_for_ingredient(miss_node):
            for ing in graph.get_ingredients_for_recipe(recipe):
                ing_name = ing.replace('ing_', '')
                if ing_name in available_set and ing_name != miss:
                    candidates.append(ing_name)
        if candidates:
            # Greedy: pick the one with most occurrences
            sub = max(set(candidates), key=candidates.count)
            subs[miss] = sub
    return subs
