import csv

def update_database(database_file, update_file):
    # Read the database file into a list of rows and extract headers
    with open(database_file, mode='r', newline='') as db_file:
        reader = csv.reader(db_file)
        database = list(reader)
        db_headers = database[0]

    # Read the update file into a list of rows and extract headers
    with open(update_file, mode='r', newline='') as upd_file:
        reader = csv.reader(upd_file)
        update = list(reader)
        upd_headers = update[0]

    # Determine the columns to be added (those not in the database headers)
    new_columns = [i for i, header in enumerate(upd_headers) if header not in db_headers]

    # Extend the database headers with new columns
    db_headers.extend([upd_headers[i] for i in new_columns])

    # Update the database rows with new columns
    for row in update[1:]:
        if row[0] in [db_row[0] for db_row in database]:
            db_row = next(db_row for db_row in database if db_row[0] == row[0])
            db_row.extend([row[i] for i in new_columns])
        else:
            new_row = row[:1] + [''] * (len(db_headers) - len(row)) + [row[i] for i in new_columns]
            database.append(new_row)

    # Write the updated database back to the file
    with open(database_file, mode='w', newline='') as db_file:
        writer = csv.writer(db_file)
        writer.writerows(database)

def remove_column(database_file, column_header):
    # Read the database file into a list of rows and extract headers
    with open(database_file, mode='r', newline='') as db_file:
        reader = csv.reader(db_file)
        database = list(reader)
        db_headers = database[0]

    # Find the index of the column to be removed
    if column_header in db_headers:
        col_index = db_headers.index(column_header)
        # Remove the header
        db_headers.pop(col_index)
        # Remove the column from each row
        for row in database[1:]:
            row.pop(col_index)

        # Write the updated database back to the file
        with open(database_file, mode='w', newline='') as db_file:
            writer = csv.writer(db_file)
            writer.writerows(database)
    else:
        print(f"Column '{column_header}' not found in the database.")

def remove_empty_rows(database_file):
    # Read the database file into a list of rows
    with open(database_file, mode='r', newline='') as db_file:
        reader = csv.reader(db_file)
        database = list(reader)
        db_headers = database[0]

    # Filter out rows that only have an entry in the first column
    filtered_database = [row for row in database if any(cell.strip() for cell in row[1:]) or row == db_headers]

    # Write the updated database back to the file
    with open(database_file, mode='w', newline='') as db_file:
        writer = csv.writer(db_file)
        writer.writerows(filtered_database)

if __name__ == "__main__":
    # Example usage
    #update_database('/Users/lucyhorowitz/Documents/GitHub/MathGloss/database.csv', '/Users/lucyhorowitz/Documents/GitHub/CatGloss/database.csv')
    #remove_column('/Users/lucyhorowitz/Documents/GitHub/MathGloss/database.csv', 'MuLiMa')
    remove_empty_rows('/Users/lucyhorowitz/Documents/GitHub/MathGloss/database.csv')