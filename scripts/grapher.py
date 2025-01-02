import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

# create individual node
def create_node(tx, node_id, node_name, properties):
    query = (
        "MERGE (n:Concept {id: $id}) "
        "SET n += $properties, n.name = $name"
    )
    tx.run(query, id=node_id, name=node_name, properties=properties)
    print(f"Node created with id: {node_id} and properties: {properties}")

# create neo4j graph from database.json
def create_nodes(database):
    with open(database, 'r') as file:
        data = json.load(file)

    # Connect to Neo4j
    # Load environment variables from .env file
    load_dotenv()
    password = os.getenv("NEO4J_PASSWORD")
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    with driver.session() as session:
        for node_id, properties in data.items():
            # Extract the name from the properties
            node_name = properties.pop('Wikidata Label', None)
            # Create the node in the graph
            for key, value in list(properties.items()):
                if isinstance(value, str):
                    name_part = value.split('[')[-1].split(']')[0] if '[' in value and ']' in value else None
                    link_part = value.split('(')[-1].split(')')[0] if '(' in value and ')' in value else None
                    if name_part:
                        properties[f"{key} name"] = name_part
                    if link_part:
                        properties[f"{key} link"] = link_part
                    del properties[key]
            node_id = node_id.split('[')[-1].split(']')[0]
            session.execute_write(create_node, node_id, node_name, properties)
    driver.close()

def create_edge(tx, source_id, target_id, relation_name, relation_id, resource):
    query = (
        f"MATCH (a:Concept {{id: $source_id}}), (b:Concept {{id: $target_id}}) "
        f"MERGE (a)-[r:{relation_name} {{wikidata_id: $relation_id, resource: $resource}}]->(b)"
    )
    tx.run(query, source_id=source_id, target_id=target_id, relation_name=relation_name, relation_id=relation_id, resource=resource)
    print(f"Edge created from {source_id} to {target_id} with relation: {relation_name}")

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def get_wikidata_relations(wikidata_id):
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "format": "json"
    }
    response = requests.get(url, params=params).json()
    
    # claims is a dictionary with keys property IDs and values bunch of other dictionaries
    # each claim is about a wikidata entry, and we get the id by doing 
    # claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id")
    claims = response.get("entities", {}).get(wikidata_id, {}).get("claims", {})
    simplified_relations = {}
    for relationtype in claims:
        simplified_relations[relationtype] = []
        for claim in claims[relationtype]:
            try:
                simplified_relations[relationtype].append(claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id"))
            except: 
                continue
    return simplified_relations

def create_edges_from_wikidata():
    load_dotenv()
    password = os.getenv("NEO4J_PASSWORD")
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    with driver.session() as session:
        result = session.run("MATCH (n:Concept) RETURN n.id AS id")
        node_ids = [record["id"] for record in result]
        resource = "Wikidata"
        togo = len(node_ids)
        i = 1
        for node_id in node_ids:
            print(f"Searching relations for {node_id} ({i}/{togo})")
            relations = get_wikidata_relations(node_id)
            for relationtype in relations:
                for targets in relations[relationtype]:
                    url = f"https://www.wikidata.org/w/api.php"
                    params = {
                        "action": "wbgetentities",
                        "ids": relationtype,
                        "format": "json",
                        "props": "labels",
                        "languages": "en"
                    }
                    response = requests.get(url, params=params).json()
                    relation_name = response.get("entities", {}).get(relationtype, {}).get("labels", {}).get("en", {}).get("value", relationtype)
                    if relation_name.__contains__('('):
                        relation_name = relation_name[:relation_name.index('(')]
                    relation_name = relation_name.upper().replace(" ","_").replace(',','')
                    if targets in node_ids:
                        session.execute_write(create_edge, node_id, targets, relation_name, relationtype, resource)
            i += 1
    driver.close()

def main():
    create_edges_from_wikidata()
    #create_nodes("neo4j_database.json")

if __name__ == "__main__":
    main()