from typing import List, Tuple, Dict
import neo4j

driver = neo4j.GraphDatabase.driver("bolt:http://localhost:7687", auth=("neo4j", "qwer1234"))

__ReqMateral = str
__QtyNeeded = int
__IngredientList = List[Tuple[__ReqMateral, __QtyNeeded]]

def create_new_entry(entry_name: str, ingredients: __IngredientList) -> None:
    """Add a new recipe to the graph. If existing items are referenced in the recipe,
    relationships will be connected with existing items. Items not already in the graph
     will be added.
     The ingredients should be organized as nested lists:
     [(ingredient1, qty), (ingredient2, qty), (etc...)]"""

    with driver.session() as session:
        session.write_transaction(_add_recipe, entry_name, ingredients)


def req_lookup(entry_name: str) -> Dict[__ReqMateral, __QtyNeeded]:
    """Searches graph for an item by name and returns the required materials in a dict."""
    requirements = {}
    with driver.session() as session:
        result = _get_recipe(session, entry_name)
        for req in result:
            requirements[req['ingredient']] = req['qty']
        return requirements


# Cypher Queries ------------------------

def _add_recipe(tx, result: str, recipe: ):
    return tx.run('MERGE (item:Item {name: $result}) WITH item '
                  'FOREACH (req IN $recipe | '
                  'MERGE (i:Item {name: req[0]}) '
                  'MERGE (item)-[:REQUIRES{qty:req[1]}]->(i) '
                  ')', result=result, recipe=recipe)


def _get_recipe(tx, item):
    return tx.run('MATCH (n:Item {name: $item})-[req:REQUIRES]->(a) '
                  'RETURN a.name AS ingredient, req.qty AS qty', item=item)


print(req_lookup('Antimatter'))
