import os
import csv
from mistralai import Mistral
from pathlib import Path
import time

# Set up the API client
API_URL = "https://api.mistral-llm.com/v1/completions"
API_KEY = API_KEY
client = Mistral(api_key=API_KEY)

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

# Assuming the CSV file is located at /Users/lucyhorowitz/Documents/GitHub/MathGloss/mathlib.csv
csv_file_path = Path("/Users/lucyhorowitz/Documents/GitHub/MathGloss/mathlib.csv")
process_mathlib_csv(csv_file_path)
