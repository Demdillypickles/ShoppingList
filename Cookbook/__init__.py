# Cookbook is the manager of JSON files and contains functions for loading and dumping ItemTrees
import json
import ItemTree


def get_cookbook(game):
    with open(f"Cookbook/{game}.json", 'r') as file:
        cookbook = json.load(file)
    return cookbook


def sorted_book(cookbook) -> dict:
    new_book = {}
    for key in sorted(cookbook):
        new_book[key] = cookbook[key]
    return new_book


def make_cookbook(game):
    cookbook = ItemTree.make_cookbook()
    with open(f"Cookbook/{game}.json", 'w') as file:
        json.dump(sorted_book(cookbook), file, indent=2)


def load_cookbook(game):
    cookbook = get_cookbook(game)
    for result, recipe in cookbook.items():
        ItemTree.create_new_entry(result, recipe)
