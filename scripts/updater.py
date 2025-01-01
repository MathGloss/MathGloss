import os
import sqlite3
from typing import List, Optional
import pandas as pd
import json
import urllib.parse

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

def remove_column(csv_file, column_name):
    df = pd.read_csv(csv_file)
    if column_name in df.columns:
        df = df.drop(columns=[column_name])
    df.to_csv(csv_file,index=False)

def add_column(database, new_csv, skip_new=False):
    new_data = pd.read_csv(new_csv)
    df = pd.read_csv(database)
    
    # Ensure all columns in new_data exist in df
    for column in new_data.columns:
        if column not in df.columns:
            df[column] = None
    
    # DataFrame to hold new rows to be added
    new_rows = pd.DataFrame(columns=df.columns)
    
    for index, row in new_data.iterrows():
        matching_index = df[df['Wikidata ID'] == row[0]].index
        if not skip_new:
            if matching_index.empty:
                new_rows = pd.concat([new_rows, pd.DataFrame([row], columns=new_data.columns)], ignore_index=True)
            else:
                df.at[matching_index[0], 'Context'] = row[1]
        elif not matching_index.empty:
            df.at[matching_index[0], 'Context'] = row[1]
    
    # Concatenate the new rows to the existing DataFrame
    df = pd.concat([df, new_rows], ignore_index=True)
    
    df.to_csv(database, index=False)

# removes rows (concepts) that only have appearances in one column in databse.csv, leaves database.json alone
def remove_isolates(database, column):
    df = pd.read_csv(database)
    columns = df.columns
    if column not in columns:
        print(f"Error: Column '{column}' not found.")
        return
    for index, row in df.iterrows():
        if row[column]:
            alone = True
            for heading in columns[2:]:
                if heading != column:
                    if pd.notna(row[heading]):
                        alone = False
            if alone:
                print(f"REMOVED {row["Wikidata Label"]}")
                df = df.drop(index)
    df.to_csv(database, index=False)

# creates new_database.json and new_database.csv from individual alignment files
def build_database(map,files,output="new_database.csv"):
    data_dict = {}
    for file in files:
        df = pd.read_csv(file)
        resource = df.columns.tolist()[1]
        
        for _, row in df.iterrows():
            if row.iloc[0] not in data_dict:
                data_dict[row.iloc[0]] = {}
            data_dict[row.iloc[0]][resource] = row.iloc[1]

    for key in data_dict:
        wikidata_id = key.split('[')[-1].split(']')[0]
        try:
            data_dict[key]["Wikidata Label"] = urllib.parse.unquote(map.id_to_titles(wikidata_id)[0]).replace('_', ' ')
        except:
            data_dict[key]["Wikidata Label"] = ""
    with open("new_database.json", 'w') as f:
        json.dump(data_dict, f, indent=4)

    result_df = pd.DataFrame.from_dict(data_dict, orient='index')

    # Rename the index to 'Wikidata ID'
    result_df.index.name = 'Wikidata ID'
    result_df.reset_index(inplace=True)

    # Specify the column order
    column_order = ["Wikidata ID", "Wikidata Label"] + [df.columns.tolist()[1] for df in [pd.read_csv(file) for file in files]]
    column_order = list(dict.fromkeys(column_order))  # Remove duplicates while preserving order

    # Save the DataFrame to a CSV file with specified column order
    result_df.to_csv(output, columns=column_order, index=False)

# reorders columns in database.csv, leaves database.json alone
def reorder_columns(database, columns):
    df = pd.read_csv(database)
    existing_columns = df.columns.tolist()
    
    # Ensure all specified columns are in the DataFrame
    for column in columns:
        if column not in existing_columns:
            raise ValueError(f"Column '{column}' not found in the database.")
    
    # Reorder columns
    df = df[columns]
    
    df.to_csv(database, index=False)

# sorts database.csv by column, leaves database.json alone
def sort_by(database, column):
    df = pd.read_csv(database)
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in the database.")
    df = df.sort_values(by=column, key=lambda col: col.str.lower())
    df.to_csv(database, index=False)

def main():
    map = WikiMapper('/Users/lucyhorowitz/Documents/MathGloss/wikidata/index_enwiki-20190420.db')
    alignments_dir = "/Users/lucyhorowitz/Documents/GitHub/MathGloss/alignments"
    files = [os.path.join(alignments_dir, file) for file in os.listdir(alignments_dir) if file.endswith('.csv')]

    #build_database(map, files)

    #remove_isolates("/Users/lucyhorowitz/Documents/GitHub/MathGloss/database.csv",'PlanetMath')
    #reorder_columns("/Users/lucyhorowitz/Documents/GitHub/MathGloss/database.csv", ["Wikidata ID","Wikidata Label","Chicago","Mathlib","nLab","Context","PlanetMath"])
    sort_by("/Users/lucyhorowitz/Documents/GitHub/MathGloss/database.csv","Wikidata Label")

if __name__ == "__main__":
    main()