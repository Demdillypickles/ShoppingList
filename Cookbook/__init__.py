import json


def get_recipe(game, category, recipe):
    with open(f"Cookbook/{game}/{category}.json") as file:
        entry = json.load(file)[recipe]
    return entry
