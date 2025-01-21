import os
import csv
from mistralai import Mistral
from pathlib import Path
import time
import argparse
from dotenv import load_dotenv

# Set up the API client
load_dotenv()
client = Mistral(api_key= os.getenv("MISTRAL_API_KEY"))

import os
import csv
import re
from pathlib import Path
import time

def get_suggestions(term):
    messages = [
        {
            "role": "user",
            "content": f"Rewrite the following term in the singular, if it is plural, and fix incorrect punctuation. Write nothing else. Write the original term if it is correct and singular. \n\nText: {term}"
        }
    ]

    chat_response = client.chat.complete(
        model="open-mistral-nemo",
        messages=messages
    )
    time.sleep(5)
    return chat_response.choices[0].message.content.strip()

def process_mathlib_csv(file_path):
    temp_file_path = file_path.with_suffix('.tmp')

    with file_path.open('r', newline='') as csvfile, temp_file_path.open('w', newline='') as temp_csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['suggestion']
        writer = csv.DictWriter(temp_csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            term = row['term']
            suggestion = get_suggestions(term)
            row['suggestion'] = suggestion
            writer.writerow(row)

    temp_file_path.replace(file_path)


def main():
    parser = argparse.ArgumentParser(description='Use Mistral to generate "suggestions" for terms that may not be searchable in Wikidata for some reason (e.g. plural, incomplete noun phrase) from a list of terms with links. It will change the file you give it to have the extra "suggestion" column.')
    parser.add_argument('-d', '--termlist', type=str, required=True, help='Path to the list of terms')
    parser.add_argument('-c', '--csv_file', type=str, required=True, help='Path to the CSV file of terms from one source. It should have the following format: title,link,(optional )suggestion. Title should be the name of the thing you want to search for in Wikidata.')
    args = parser.parse_args()

    map = WikiMapper(args.database)
    do_mappings(args.csv_file, map)


if __name__ == "__main__":
    main()

