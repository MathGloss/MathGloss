import sqlite3
from typing import List, Optional
import csv
import requests
import pandas as pd

class WikiMapper:
    """Uses a precomputed database created by `create_wikipedia_wikidata_mapping_db`."""

    def __init__(self, path_to_db: str):
        self._path_to_db = path_to_db
        self.conn = sqlite3.connect(self._path_to_db)

    def title_to_id(self, page_title: str) -> Optional[str]:
        """Given a Wikipedia page title, returns the corresponding Wikidata ID.
        The page title is the last part of a Wikipedia url **unescaped** and spaces
        replaced by underscores , e.g. for `https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem`,
        the title would be `Fermat's_Last_Theorem`.
        Args:
            page_title: The page title of the Wikipedia entry, e.g. `Manatee`.
        Returns:
            Optional[str]: If a mapping could be found for `wiki_page_title`, then return
                           it, else return `None`.
        """

        c = self.conn.execute("SELECT wikidata_id FROM mapping WHERE wikipedia_title=?", (page_title,))
        result = c.fetchone()

        if result is not None and result[0] is not None:
            return result[0]
        else:
            return None

    def url_to_id(self, wiki_url: str) -> Optional[str]:
        """Given an URL to a Wikipedia page, returns the corresponding Wikidata ID.
        This is just a convenience function. It is not checked whether the index and
        URL are from the same dump.
        Args:
            wiki_url: The URL to a Wikipedia entry.
        Returns:
            Optional[str]: If a mapping could be found for `wiki_url`, then return
                           it, else return `None`.
        """

        title = wiki_url.rsplit("/", 1)[-1]
        return self.title_to_id(title)

    def id_to_titles(self, wikidata_id: str) -> List[str]:
        """Given a Wikidata ID, return a list of corresponding pages that are linked to it.
        Due to redirects, the mapping from Wikidata ID to Wikipedia title is not unique.
        Args:
            wikidata_id (str): The Wikidata ID to map, e.g. `Q42797`.
        Returns:
            List[str]: A list of Wikipedia pages that are linked to this Wikidata ID.
        """

        c = self.conn.execute(
            "SELECT DISTINCT wikipedia_title FROM mapping WHERE wikidata_id =?", (wikidata_id,)
        )
        results = c.fetchall()

        return [e[0] for e in results]

wikicats = ['_(mathematics)', '_(category_theory)', '_(linear_algebra)', '_(algebraic_geometry)', '_(algebraic_topology)',
             '_(commutative_algebra)', '_(field_theory)', '_(game_theory)', '_(topology)', '_(differential_geometry)', '_(graph_theory)', 
             '_(group_theory)', '_(invariant_theory)', '_(module_theory)', '_(order_theory)', '_(ring_theory)',
             '_(representation_theory)', '_(set_theory)', '_(string_theory)', '_(symplectic geometry)', '_(tensor_theory)']

def is_disambiguation(wikidata_id):
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "format": "json"
    }
    response = requests.get(url, params=params).json()
    claims = response.get("entities", {}).get(wikidata_id, {}).get("claims", {})
    if "P31" in claims:
        for claim in claims["P31"]:
            disambiguation = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q4167410"
            person = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q5"
            theorem = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q65943"
            lemma = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q207505"
            proposition = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id") == "Q108163"
            return disambiguation or person or theorem or lemma or proposition
        return False

# file should be a csv in the following format: title,link,suggestion.
# suggestion is optional. title should be the name of the thing we care about. 
def map_with_suggestions(filename, map):
    #check that the thing is formatted appropriately and see whether we are doing suggestions.
    df = pd.read_csv(filename)
    columns = df.columns.tolist()
    suggestions = False
    if df.shape[1] == 3:
        if not (columns[1] == "link" and columns[2] == "suggestion"):
            print("invalid format")
            return
        resource = columns[1]
        suggestions = True
    elif df.shape[1] == 2:
        if not columns[1] == "link":
            print("invalid format")
            return
        resource = columns[0]
    else:
        print("invalid format")
        return
    
    writer = csv.writer(f"{resource}_mappings.csv")
    writer.writerow(['Wikidata ID', resource])
    if not suggestions:
        for index, row in df.iterrows():
            title = row[0].strip().replace(' ', '_')
            title = title[0].upper() + title[1:] 
            found = False
            for cat in wikicats:
                title_cat = title + cat
                wikidata_id = map.title_to_id(title_cat)
                if wikidata_id:
                    link = row[1]  # Use the second column as the PlanetMath link
                    writer.writerow([f"[{wikidata_id}](https://www.wikidata.org/wiki/{wikidata_id})", f"[{row[0]}]({link})"])
                    print(f"CAT {title_cat} found: {wikidata_id}")
                    found = True
                    break
            if not found:
                wikidata_id = map.title_to_id(title)
                if wikidata_id and not is_disambiguation(wikidata_id):
                    link = row[1]  # Use the second column as the PlanetMath link
                    writer.writerow([f"[{wikidata_id}](https://www.wikidata.org/wiki/{wikidata_id})", f"[{row[0]}]({link})"])
                    print(f"REG {title} found: {wikidata_id}")
                    found = True
            if not found:
                print(f"NOT FOUND {row[0]}")
    else:
        for index, row in df.iterrows():
            title = row[0].strip().replace(' ', '_')
            title = title[0].upper() + title[1:] 
            link = row[1]
            suggestion = row[2].strip().replace(' ', '_')
            suggestion = suggestion[0].upper() + suggestion[1:] 
            found = False
            for cat in wikicats:
                suggestion_cat = suggestion + cat
                wikidata_id = map.title_to_id(suggestion_cat)
                if wikidata_id and not is_disambiguation(wikidata_id):
                    writer.writerow([f"[{wikidata_id}](https://www.wikidata.org/wiki/{wikidata_id})", f"[{row[0].strip()}]({link})"])
                    print(f"SUGCAT {suggestion_cat} found: {wikidata_id}")
                    found = True
                    break
            if not found:
                wikidata_id = map.title_to_id(suggestion)
                if wikidata_id and not is_disambiguation(wikidata_id):
                    writer.writerow([f"[{wikidata_id}](https://www.wikidata.org/wiki/{wikidata_id})", f"[{row[0].strip()}]({link})"])
                    print(f"SUG {suggestion} found: {wikidata_id}")
                    found = True
                else:    
                    for cat in wikicats:
                        title_cat = title + cat
                        wikidata_id = map.title_to_id(title_cat)
                        if wikidata_id and not is_disambiguation(wikidata_id):
                            writer.writerow([f"[{wikidata_id}](https://www.wikidata.org/wiki/{wikidata_id})", f"[{row[0].strip()}]({link})"])
                            print(f"REGCAT {title_cat} found: {wikidata_id}")
                            found = True
                            break
                    if not found:
                        wikidata_id = map.title_to_id(title)
                        if wikidata_id and not is_disambiguation(wikidata_id):
                            writer.writerow([f"[{wikidata_id}](https://www.wikidata.org/wiki/{wikidata_id})", f"[{row[0].strip()}]({link})"])
                            print(f"REG {title} found: {wikidata_id}")
                            found = True
        if not found:
            print(f"NOT FOUND {filename}")



def main():
    map = WikiMapper('/Users/lucyhorowitz/Documents/MathGloss/wikidata/index_enwiki-20190420.db')
    map_with_suggestions('/Users/lucyhorowitz/Documents/MathGloss/planetmath/titles.csv', "PlanetMath", map)

if __name__ == "__main__":
    main()