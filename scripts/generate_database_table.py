import re, sys, csv

def generate_html_content(csv_file_path):
    # Function to convert Markdown-style links to HTML-style links
    def convert_markdown_to_html(text):
        return re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    # Read the CSV file
    with open(csv_file_path, newline='', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Get the headers
        # Start the HTML file
        html_content = '''<table id="database" class="display">\n    <thead>\n        <tr class="header">'''
        # Add headers to the HTML file
        for header in headers:
            html_content += f'\n            <th>{convert_markdown_to_html(header)}</th>'
        html_content += '''\n        </tr>\n    </thead>\n    <tbody>'''
        # Add rows to the HTML file
        row_class = 'odd'
        for row in csv_reader:
            html_content += f'\n        <tr class="{row_class}">'
            for cell in row:
                html_content += f'\n            <td>{convert_markdown_to_html(cell)}</td>'
            html_content += '\n        </tr>'
            row_class = 'even' if row_class == 'odd' else 'odd'
        html_content += '''</tbody>\n</table>'''
    return html_content

def main(csv_file_path,html_file_path):
    html_content = generate_html_content(csv_file_path)

    with open(html_file_path, mode='w', encoding='utf-8') as html_file:
        html_file.write(html_content)

if __name__ == "__main__":
    if (len(sys.argv) == 3):
        main(sys.argv[1],sys.argv[2])
    else:
        print("Error: wrong number of arguments")
        exit
