import html
import difflib


def read_references(file_path):
    """Reads references from a specified text file and returns them as a list of strings."""
    references = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            references = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
    return references


def read_text_file(file_path):
    """Read text file with proper encoding"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # remove BOM marker if present
        if content.startswith('\ufeff'):
            content = content[1:]
        return content


def write_text_file(content, output_path):
    """Write content to text file with proper encoding"""
    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def highlight_differences(df, col_src, col_tar, html_file):
    # make sure the columns exist
    if col_src not in df.columns or col_tar not in df.columns:
        raise ValueError(f"Column {col_src} or {col_tar} not found in the CSV file.")

    # Create HTML table
    html_content = f'''
    <html>
    <head>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .diff {{ color: red; font-weight: bold; background-color: skyblue; padding: 1px 3px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <h2>Difference Comparison</h2>
        <table>
            <tr>
    '''
    
    # Add all column headers
    for col in df.columns:
        html_content += f'<th>{html.escape(col)}</th>'
    
    html_content += '</tr>'

    # Process each row
    for index, row in df.iterrows():
        src_value = str(row[col_src])
        tar_value = str(row[col_tar])
        
        # Use SequenceMatcher to find matching blocks
        matcher = difflib.SequenceMatcher(None, src_value, tar_value)
        
        # Generate HTML for source value
        src_html = []
        pos = 0
        for block in matcher.get_matching_blocks():
            # Add non-matching (different) part with highlighting
            if pos < block.a:
                src_html.append(f'<span class="diff">{html.escape(src_value[pos:block.a])}</span>')
            # Add matching part without highlighting
            if block.size > 0:
                src_html.append(html.escape(src_value[block.a:block.a + block.size]))
            pos = block.a + block.size
        
        # Generate HTML for target value
        tar_html = []
        pos = 0
        for block in matcher.get_matching_blocks():
            # Add non-matching (different) part with highlighting
            if pos < block.b:
                tar_html.append(f'<span class="diff">{html.escape(tar_value[pos:block.b])}</span>')
            # Add matching part without highlighting
            if block.size > 0:
                tar_html.append(html.escape(tar_value[block.b:block.b + block.size]))
            pos = block.b + block.size
        
        # Start row in HTML table
        html_content += '<tr>'
        
        # Add each cell for the current row
        for col in df.columns:
            if col == col_src:
                html_content += f'<td>{"".join(src_html)}</td>'
            elif col == col_tar:
                html_content += f'<td>{"".join(tar_html)}</td>'
            else:
                # Add other columns without highlighting
                html_content += f'<td>{html.escape(str(row[col]))}</td>'
        
        # Close the row
        html_content += '</tr>'

    # Close HTML tags
    html_content += '''
        </table>
    </body>
    </html>
    '''

    # Write HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML file saved to {html_file}")
