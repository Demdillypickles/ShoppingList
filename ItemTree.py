import neo4j

driver = neo4j.GraphDatabase.driver("bolt:http://localhost:7687", auth=("neo4j", "qwer1234"))


def create_new_entry(dri, entry_name, ingredients):
    with dri.session() as session:
        session.write_transaction(add_recipe, entry_name, ingredients)


def find_entry(dri, entry_name):
    with dri.session() as session:
        return session.read_transaction(get_recipe, entry_name)


def add_recipe(tx, result, recipe):
    return tx.run('MERGE (item:Item {name: $result}) WITH item '
                  'FOREACH (req IN $recipe | '
                  'MERGE (i:Item {name: req[0]}) '
                  'MERGE (item)-[:REQUIRES{qty:req[1]}]->(i) '
                  ')'
                  , result=result, recipe=recipe)


def get_recipe(tx, item):
    return tx.run('MATCH (n:Item {name: $item})-[req:REQUIRES]->(a) '
                  'RETURN a.name AS ingredient, req.qty AS qty'
                  , item=item)
