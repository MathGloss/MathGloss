import re
import os
import json
from dotenv import load_dotenv

def extract_class_info(text,matchonly = False):
    text = "\n".join([line for line in text.splitlines() if not line.strip().startswith("@")])

    pattern = re.compile(r"""
        (?<=-/)\s*
        class\s+(?P<name>\w+)\s*
        (?P<paren>\([^)]*\))?\s*
        (?P<brackets>\[[^\]]*\])?\s*
        extends\s*(?P<extends>[\w\s,]*)(?=\s*:|\s*where)
    """, re.DOTALL | re.VERBOSE)
    
    docstring_pattern = re.compile(r"/--\s*(.*?)\s*-/", re.DOTALL)
    
    matches = pattern.finditer(text)
    if matchonly:
        return matches
    else:
        result = {}
        
        for match in matches:
            name = match.group("name")
            
            # Find the last docstring before this class
            docstring_match = list(docstring_pattern.finditer(text[:match.start()]))
            docstring = docstring_match[-1].group(1).strip() if docstring_match else ""
            
            result[name] = {
                "docstring": docstring,
                "()": match.group("paren").strip("() ").split(",") if match.group("paren") else [],
                "[]": match.group("brackets").strip("[] ").split(",") if match.group("brackets") else [],
                "extends": [e.strip() for e in match.group("extends").split(",") if e.strip()]
            }
        
        return result

# read the file
# Get the directory from the environment variable
# Load environment variables from .env file
load_dotenv()

directory = os.getenv('MATHLIB')


# Construct the full file path
file_paths = []
with open("/Users/lucyhorowitz/Documents/GitHub/MathGloss/alignments/mathlib_mappings.csv", "r", encoding="utf-8") as csvfile:
    lines = csvfile.readlines()
    for line in lines:
        parts = line.split(',')
        if len(parts) > 1:
            url = parts[1].strip()
            match = re.search(r"https://leanprover-community.github.io//mathlib4_docs/./(.*?)(#|$)", url)
            if match:
                file_path_part = match.group(1).replace(".html", ".lean")
                print(file_path_part)
                file_path = os.path.join(directory, file_path_part)
                file_paths.append(file_path)
# Remove duplicates from file_paths
file_paths = set(file_paths)
combined_class_info = {}

def update_class_info(file_paths, output_file):
    for end in file_paths:
        print(end)
        try:
            file_path = os.path.join(directory, end)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                class_info = extract_class_info(text)
                file_path = os.path.join(directory, end)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    class_info = extract_class_info(text)
                    print(class_info)
                    combined_class_info.update(class_info)
        except:
            print(f"PROBLEM WITH {end}")

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_class_info, json_file, indent=4)


def main():
    with open("things.txt", "w", encoding="utf-8") as file:
        for end in file_paths:
            print(end)
            try:
                file_path = os.path.join(directory, end)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    class_info = extract_class_info(text)
                    file_path = os.path.join(directory, end)
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                        class_info = extract_class_info(text,True)
                        file.write(class_info + "\n\n")
            except: 
                print(f"problem with {end}")


if __name__ == "__main__":
    main()