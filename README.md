# Welcome to MathGloss
MathGloss is a project to create a knowledge graph for undergraduate mathematics automatically, using modern NLP tools. These include concept and entity recognition, entity and definition extraction, parsing, and other natural language processing (NLP) techniques.

A preprint describing this prototype is available at [MathGloss: Building mathematical glossaries from text](https://arxiv.org/abs/2311.12649).

[Click here](https://mathgloss.github.io/MathGloss/database) to see the database.

## Building the Database
To build the `database.html` file from the `database.csv`, run the following commands:
```
python scripts/generate_database_table.py database.csv database-table.html
python scripts/generate_database_page.py database-template.html database-table.html database.html
```
