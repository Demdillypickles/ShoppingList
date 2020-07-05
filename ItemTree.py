from typing import Dict
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt:http://localhost:7687", auth=("neo4j", "qwer1234"))

# ------------  Custom Typing Objects  ------------

__ReqMaterial = str
"""An item that is required to craft the desired item."""
__QtyNeeded = int
"""The amount of a __ReqMaterial required to fulfill a recipe."""
__IngredientList = Dict[__ReqMaterial, __QtyNeeded]
"""A dict defining the required materials:{'ingredient1': 10, 'ingredient2': 25, etc...}"""

# ----------  Graph Interface Functions -----------


def create_new_entry(entry_name: str, ingredients: __IngredientList) -> None:
    """Add a new recipe to the graph. If existing items are referenced in the recipe,
    relationships will be connected with existing items. Items not already in the graph
     will be added."""

    with driver.session() as session:
        session.write_transaction(_add_recipe, entry_name, ingredients)


def req_lookup(entry_name: str) -> Dict[__ReqMaterial, __QtyNeeded]:
    """Searches graph for an item by name and returns the required materials in a dict."""
    requirements = {}
    with driver.session() as session:
        result = _get_recipe(session, entry_name)
        for req in result:
            requirements[req['ingredient']] = req['qty']
        return requirements


def make_cookbook():
    """Create a JSON file containing all recipes in the current graph"""
    cookbook = {}
    with driver.session() as session:
        recipes = _all_recipes(session)
        for recipe in recipes:
            req = {recipe['material']: recipe['qty']}
            try:
                cookbook[recipe['result']].update(req)
            except KeyError:
                cookbook[recipe['result']] = req
    return cookbook


# ---------------  Cypher Queries  ----------------

def _add_recipe(tx, result: str, recipe: __IngredientList):
    return tx.run('MERGE (item:Item {name: $result}) WITH item '
                  'FOREACH (req IN keys($recipe) | '
                  'MERGE (i:Item {name: req}) '
                  'MERGE (item)-[:REQUIRES{qty: $recipe[req]}]->(i) '
                  ')', result=result, recipe=recipe)


def _get_recipe(tx, item):
    return tx.run('MATCH (n:Item {name: $item})-[req:REQUIRES]->(a) '
                  'RETURN a.name AS ingredient, req.qty AS qty', item=item)


def _all_recipes(tx,):
    return tx.run('MATCH (n)-[r:REQUIRES]->(i) '
                  'RETURN n.name AS result, r.qty AS qty, i.name AS material')
