import os
from api.config import load_api_info
from core.reference_checker import ReferenceChecker
from utils.file_handler import read_references, write_text_file, highlight_differences
from utils.format_handler import clean_markdown_table, parse_markdown_table


def get_file_path(input_file):
    """Determine the file path from input argument or user input"""
    if input_file is None:
        return input("Please enter the path to the reference file: ")
    return input_file


def filter_invalid_lines(text):
    """Filter out empty lines, header lines, and separator lines"""
    valid_lines = []
    lines = text.strip().split('\n')
    
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
            
        # Skip header lines that match the pattern (e.g., "| 错误格式 | 正确格式 | 错误原因 |")
        if '错误格式' in line and '正确格式' in line and '|' in line:
            continue
            
        # Skip separator lines (e.g., "|----------|----------|----------|")
        if line.strip().replace('|', '').replace('-', '').strip() == '':
            continue
            
        valid_lines.append(line)
        
    return '\n'.join(valid_lines)


def process_references(references, checker, stream=True, num_per_request=1):
    """Process references in batches using the checker"""
    if num_per_request <= 0 or len(references) <= num_per_request:
        # Process all references at once
        result = checker.check_references('\n'.join(references), stream=stream)
        # Filter invalid lines but preserve the first two lines (header) for the first batch
        lines = result.strip().split('\n')
        if len(lines) > 2:
            header_lines = lines[:2]
            content_lines = filter_invalid_lines('\n'.join(lines[2:]))
            return '\n'.join(header_lines + [content_lines])
        return result
    
    # Process in batches
    all_results = []
    batch_count = (len(references) + num_per_request - 1) // num_per_request
    
    for i in range(0, len(references), num_per_request):
        batch = references[i:i+num_per_request]
        print(f"\n\nProcessing batch {i//num_per_request + 1}/{batch_count} ({len(batch)} references)")
        
        # Check references in the batch
        batch_string = '\n'.join(batch)
        batch_result = checker.check_references(batch_string, stream=stream)
        
        # For the first batch, keep the header and separator but filter other invalid lines
        if i == 0:
            lines = batch_result.strip().split('\n')
            if len(lines) > 2:
                header_lines = lines[:2]
                content_lines = filter_invalid_lines('\n'.join(lines[2:]))
                batch_result = '\n'.join(header_lines) + '\n' + content_lines
        else:
            # For subsequent batches, filter all invalid lines
            batch_result = filter_invalid_lines(batch_result)
        
        if batch_result.strip():  # Only add non-empty results
            all_results.append(batch_result)

    # Combine results
    if len(all_results) > 1:
        combined_results = all_results[0]
        combined_results += '\n' + '\n'.join(all_results[1:])
    else:
        combined_results = all_results[0] if all_results else ""
    
    return combined_results


def save_results(modified_references, output_path=None):
    """Parse and save the results"""
    # Clean the markdown table
    clean_table = clean_markdown_table(modified_references)

    # Parse the cleaned table
    df = parse_markdown_table(clean_table)
    
    # Filter out right references
    df = df.loc[df['错误原因'].str.len() > 0].copy()

    # Save to file if output path is provided
    if output_path:
        output_md_file = output_path + "checked.md"
        output_html_file = output_path + "checked.html"
        write_text_file(modified_references, output_md_file)
        highlight_differences(df, '错误格式', '正确格式', output_html_file)
        print(f"\nResults saved to {output_path}")
    return df


def main(api_provider='deepseek', model='deepseek-r1', system_content_path='system_content', 
         stream=True, input_file=None, output_path=None, num_per_request=10):
    # Load configuration
    api_info = load_api_info(api_provider=api_provider)
    assert model in api_info['models'], f"Invalid model for provider {api_provider}"

    # Get file path and read references
    file_path = get_file_path(input_file)
    references = read_references(file_path)
    if not references:
        print("No references found in the file. Please check the file and try again.")
        return
    
    # Initialize the checker
    checker = ReferenceChecker(
        api_info, model=model,
        system_content_path=system_content_path
    )

    # Process references
    modified_references = process_references(references, checker, stream=stream, num_per_request=num_per_request)

    # Save results
    df = save_results(modified_references, output_path)
    
    print("\n\nReferences have been successfully processed!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check and modify references using a language model.")
    parser.add_argument("--api_provider", type=str, default=None, help="API provider")
    parser.add_argument("--model", type=str, default=None, help="Model name")
    parser.add_argument("--system_content_path", type=str, default='system_content.md', help="System content path")
    parser.add_argument("--input_file", type=str, default=None, help="Input file path")
    parser.add_argument("--output_path", type=str, default=None, help="Output path")
    parser.add_argument("--stream", type=bool, default=True, help="Stream response")
    parser.add_argument("--num_per_request", type=int, default=10, help="Number of references per request")
    
    args = parser.parse_args()
    main(
        api_provider=args.api_provider,
        model=args.model,
        system_content_path=args.system_content_path, 
        input_file=args.input_file,
        output_path=args.output_path,
        stream=args.stream,
        num_per_request=args.num_per_request
    )
