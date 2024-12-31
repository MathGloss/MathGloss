import re
import pandas as pd
from neo4j import GraphDatabase
import requests
import json

def json_database_to_neo4j(json_file, uri, user, password):
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def create_node(tx, node):
        query = """
        MERGE (n:Node {id: $id})
        SET n += $properties
        """
        tx.run(query, id=node['id'], properties=node)
    
    with driver.session() as session:
        for node in data['nodes']:
            session.write_transaction(create_node, node)
    
    driver.close()

# Example usage
json_database_to_neo4j('database.json', 'bolt://localhost:7687', 'neo4j', 'password')