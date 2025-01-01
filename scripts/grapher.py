import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# create individual node
def create_node(tx, node_id, node_name, properties):
    query = (
        "MERGE (n:Concept {id: $id}) "
        "SET n += $properties, n.name = $name"
    )
    
    tx.run(query, id=node_id, name=node_name, properties=properties)
    print(f"Node created with id: {node_id} and properties: {properties}")

# create neo4j graph from database.json
def create_database(database):
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
            node_name = properties.pop('Wikidata Label',None)
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

def main():
    create_database("neo4j_database.json")

if __name__ == "__main__":
    main()