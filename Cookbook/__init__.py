# Cookbook is the manager of JSON files and contains functions for loading and dumping ItemTrees
import json
import ItemTree


def _get_cookbook(game):
    """Helper function. Retrieves JSON file for further processing. """
    with open(f"./{game}.json", 'r') as file:
        cookbook = json.load(file)
    return cookbook


def _sorted_book(cookbook) -> dict:
    """Helper Function. Used to alphabetize a Cookbook. """
    new_book = {}
    for key in sorted(cookbook):
        new_book[key] = cookbook[key]
    return new_book


def make_cookbook(game):
    cookbook = ItemTree.make_cookbook()
    with open(f"./{game}.json", 'w') as file:
        json.dump(_sorted_book(cookbook), file, indent=2)


def load_cookbook(game):
    cookbook = _get_cookbook(game)
    for result, recipe in cookbook.items():
        ItemTree.create_new_entry(result, recipe)

print(_get_cookbook('NMS'))