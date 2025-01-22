import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import argparse
import re

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

def create_wikidata_edge(tx, source_id, target_id, relation_name, relation_id, resource):
    print(f"Creating edge from {source_id} to {target_id} with relation: {relation_name}")
    query = (
        f"MATCH (a:Concept {{id: $source_id}}), (b {{id: $target_id}}) "
        f"MERGE (a)-[r:{relation_name} {{wikidata_id: $relation_id, resource: $resource}}]->(b) "
        "RETURN r"
    )
    result = tx.run(query, source_id=source_id, target_id=target_id, relation_name=relation_name, relation_id=relation_id, resource=resource)
    if result.single():
        print(f"Edge created from {source_id} to {target_id} with relation: {relation_name}")
    else:
        print(f"No edge created from {source_id} to {target_id} with relation: {relation_name}")

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

def create_mention_edge(tx, source_id, target_id,resource):
    query = (
        "MATCH (a:Concept {id: $source_id}), (b:Concept {id: $target_id}) "
        "MERGE (a)-[r:MENTIONS]->(b) "
        f"SET r.`{resource}` = 'yes'"
    )
    tx.run(query, source_id=source_id, target_id=target_id)
    print(f"Edge created or updated from {source_id} to {target_id} with relation: MENTIONS and resource: {resource}")

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
                        session.execute_write(create_wikidata_edge, node_id, targets, relation_name, relationtype, resource)
            i += 1
    driver.close()

def create_edges_from_chicago():
    load_dotenv()
    password = os.getenv("NEO4J_PASSWORD")
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    with driver.session() as session:
        result = session.run("MATCH (n:Concept) RETURN n.id AS id, n.`Chicago name` AS chicago_name, n.`Chicago link` AS chicago_link")
        result = list(result)
        togo = len([record["id"] for record in result])
        i = 1
        for record in result:
            node_id = record["id"]
            chicago_link = record["chicago_link"]
            chicago_name = record["chicago_name"]
            print(f"Looking for mentions in {chicago_name}... ({i}/{togo})")
            if chicago_link:
                chicago_file_path = os.path.join(parent_dir, "chicago", f"{chicago_link.split('/')[-1]}.md")
                if os.path.exists(chicago_file_path):
                    with open(chicago_file_path, 'r') as chicago_file:
                        text = chicago_file.read()
                        links = re.findall(r'https://mathgloss.github.io/MathGloss/chicago/[^ ]+', text)
                        for link in links:
                            target_result = session.run("MATCH (n:Concept {`Chicago link`: $link}) RETURN n.id AS id", link=link[:-1])
                            target_record = target_result.single()
                            if target_record:
                                target_id = target_record["id"]
                                session.execute_write(create_mention_edge, node_id, target_id, "chicago")
            i += 1
                            
    driver.close()

def create_edges_from_nlab():
    load_dotenv()
    password = os.getenv("NEO4J_PASSWORD")
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    with driver.session() as session:
        result = session.run("MATCH (n:Concept) RETURN n.id AS id, n.`nLab name` AS nlab_name, n.`nLab link` AS nlab_link")
        result = list(result)
        togo = len([record["id"] for record in result])
        i = 1
        for record in result:
            node_id = record["id"]
            nlab_link = record["nlab_link"]
            nlab_name = record["nlab_name"]
            print(f"Looking for mentions in {nlab_name}... ({i}/{togo})")
            if nlab_link:
                # Fetch the content of the linked page
                response = requests.get(nlab_link)
                if response.status_code == 200:
                    linked_links = [f"https://ncatlab.org{thing}".replace("+","%20") for thing in re.findall(r'/nlab/show/[^"]*', response.text)]
                    for linked_link in linked_links:
                        target_result = session.run("MATCH (n:Concept {`nLab link`: $link}) RETURN n.id AS id", link=linked_link)
                        target_record = target_result.single()
                        if target_record:
                            target_id = target_record["id"]
                            if target_id != node_id: 
                                session.execute_write(create_mention_edge, node_id, target_id, "nlab")
            i += 1
                            
    driver.close()


def get_incoming_links(wikidata_id):

    load_dotenv()
    password = os.getenv("NEO4J_PASSWORD")
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    with driver.session() as session:
        result = session.run("MATCH (n:Concept) RETURN n.id AS id")
        node_ids = [record["id"] for record in result]
    driver.close()

    endpoint_url = "https://query.wikidata.org/sparql"
    query = f"""
    SELECT ?item ?property WHERE {{
      ?item ?property wd:{wikidata_id} .
    }}
    """
    headers = {"Accept": "application/json"}
    response = requests.get(endpoint_url, params={"query": query}, headers=headers)

    if response.status_code == 200:
        results = response.json()["results"]["bindings"]
        return [(result["item"]["value"].split('/')[-1], result["property"]["value"].split('/')[-1]) for result in results if not result["item"]["value"].__contains__('statement') and result["item"]["value"].split('/')[-1] in node_ids]
    else:
        raise Exception(f"SPARQL query failed: {response.status_code} - {response.text}")


def add_incoming_links(target_id, relations):
    load_dotenv()
    password = os.getenv("NEO4J_PASSWORD")
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", password))

    with driver.session() as session:
        for source_id, relation_id in relations:
            url = f"https://www.wikidata.org/w/api.php"
            params = {
                "action": "wbgetentities",
                "ids": relation_id,
                "format": "json",
                "props": "labels",
                "languages": "en"
            }
            response = requests.get(url, params=params).json()
            relation_name = response.get("entities", {}).get(relation_id, {}).get("labels", {}).get("en", {}).get("value", relation_id)
            if relation_name.__contains__('('):
                relation_name = relation_name[:relation_name.index('(')]
            relation_name = relation_name.upper().replace(" ","_").replace(',','').replace("'",'')
            session.execute_write(create_wikidata_edge, source_id, target_id, relation_name, relation_id, "Wikidata")
            
  

def main():
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    file_path = os.path.join(parent_dir, "database_neo4j.json")
    
    #create_nodes(file_path)
    #create_edges_from_wikidata()
    #create_edges_from_chicago()
    #create_edges_from_nlab()

    concept_links = get_incoming_links("Q24034552")
    object_links = get_incoming_links("Q246672")

    add_incoming_links("Q24034552", concept_links)
    add_incoming_links("Q246672", object_links)
   


if __name__ == "__main__":
    main()