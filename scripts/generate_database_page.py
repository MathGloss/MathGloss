import re, sys, csv

def main(database_template_path,database_table_path,database_path):
    # Read the database template file
    with open(database_template_path, mode='r', encoding='utf-8') as database_template_file:
        database_template_content = database_template_file.read()
    # Read the database table file
    with open(database_table_path, mode='r', encoding='utf-8') as database_table_file:
        database_table_content = database_table_file.read()
    # Join the database template and table into our database page
    database_page_content = re.sub("DATABASE_TABLE",database_table_content,database_template_content)
    # Write to the "databse.html" file
    with open(database_path, mode='w', encoding='utf-8') as database_file:
        database_file.write(database_page_content)

if __name__ == "__main__":
    if (len(sys.argv) == 4):
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print("Error: wrong number of arguments")
        exit
