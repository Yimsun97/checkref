import pandas as pd


def parse_markdown_table(markdown_text):
    """
    Convert Markdown table format to pandas DataFrame.
    
    Parameters:
    markdown_text (str): Text string containing a Markdown table
    
    Returns:
    pandas.DataFrame: Parsed dataframe
    """
    # Split text by lines
    lines = markdown_text.strip().split('\n')
    
    # Remove header separator line (usually contains --- symbols)
    header_line = lines[0]
    header = [col.strip() for col in header_line.split('|')[1:-1]]
    
    # Parse data rows
    data_rows = []
    for line in lines[2:]:
        # Skip empty lines
        if line.strip() == '':
            continue
        
        # Split lines and remove leading/trailing pipe characters and whitespace
        row_data = [col.strip() for col in line.split('|')[1:-1]]
        
        # Ensure row data length matches header length
        if len(row_data) == len(header):
            data_rows.append(row_data)
    
    # Create DataFrame
    df = pd.DataFrame(data_rows, columns=header)
    return df


def clean_markdown_table(text):
    """Remove code block markers and normalize the markdown table format"""
    # Remove code block markers
    text = text.replace('```', '')
    
    # Split into lines and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for the header line
    for i, line in enumerate(lines):
        if '错误格式' in line and '正确格式' in line:
            header_line = line
            
            # Create a standard markdown table
            result = [header_line]
            
            # Add separator line if it doesn't exist
            if i+1 < len(lines) and '---' not in lines[i+1]:
                separator = '| ' + ' | '.join(['---' for _ in header_line.split('|')[1:-1]]) + ' |'
                result.append(separator)
            elif i+1 < len(lines):
                result.append(lines[i+1])
                
            # Add all remaining data rows
            result.extend([line for line in lines if line != header_line and 
                          (line not in result and '---' not in line)])
            
            return '\n'.join(result)
    
    return text  # Return original if no header found
