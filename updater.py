import pandas as pd

def remove_column(csv_file, column_name):
    df = pd.read_csv(csv_file)
    if column_name in df.columns:
        df = df.drop(columns=[column_name])
    df.to_csv(csv_file,index=False)

def add_data(database, new_csv, skip_new=False):
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

def main():
    add_data("database copy.csv", "output_mappings.csv")

if __name__ == "__main__":
    main()