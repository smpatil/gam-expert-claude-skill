#!/usr/bin/env python3
"""
GAM Spreadsheet Processor
Helper script for processing CSV and Excel files for GAM operations
"""

import sys
import csv
import json
from pathlib import Path

def read_csv(filename, encoding='utf-8'):
    """Read CSV file and return data as list of dictionaries"""
    try:
        with open(filename, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            data = list(reader)
            return {
                'success': True,
                'data': data,
                'row_count': len(data),
                'columns': reader.fieldnames if data else []
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def validate_csv_columns(filename, required_columns):
    """Validate that CSV has required columns"""
    result = read_csv(filename)
    if not result['success']:
        return result

    data = result['data']
    if not data:
        return {
            'success': False,
            'error': 'CSV file is empty'
        }

    actual_columns = set(result['columns'])
    required_set = set(required_columns)
    missing = required_set - actual_columns

    if missing:
        return {
            'success': False,
            'error': f"Missing required columns: {', '.join(missing)}",
            'actual_columns': list(actual_columns),
            'missing_columns': list(missing)
        }

    return {
        'success': True,
        'message': 'All required columns present',
        'row_count': len(data),
        'columns': result['columns']
    }

def preview_csv(filename, rows=10, encoding='utf-8'):
    """Preview first N rows of CSV file"""
    result = read_csv(filename, encoding)
    if not result['success']:
        return result

    data = result['data']
    preview_data = data[:rows]

    return {
        'success': True,
        'total_rows': len(data),
        'preview_rows': len(preview_data),
        'columns': result['columns'],
        'preview': preview_data
    }

def transform_csv(input_file, output_file, column_mapping, filter_func=None):
    """
    Transform CSV file by renaming columns and optionally filtering rows

    Args:
        input_file: Input CSV filename
        output_file: Output CSV filename
        column_mapping: Dict mapping old column names to new column names
        filter_func: Optional function to filter rows (return True to keep row)
    """
    try:
        result = read_csv(input_file)
        if not result['success']:
            return result

        data = result['data']

        # Filter rows if filter function provided
        if filter_func:
            data = [row for row in data if filter_func(row)]

        # Transform column names
        transformed_data = []
        for row in data:
            new_row = {}
            for old_col, new_col in column_mapping.items():
                if old_col in row:
                    new_row[new_col] = row[old_col]
            transformed_data.append(new_row)

        # Write output file
        if transformed_data:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(column_mapping.values()))
                writer.writeheader()
                writer.writerows(transformed_data)

        return {
            'success': True,
            'input_rows': len(result['data']),
            'output_rows': len(transformed_data),
            'output_file': output_file
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def analyze_gam_output(csv_file, group_by_column=None):
    """Analyze GAM output CSV file"""
    result = read_csv(csv_file)
    if not result['success']:
        return result

    data = result['data']
    analysis = {
        'success': True,
        'total_rows': len(data),
        'columns': result['columns']
    }

    # Group by column if specified
    if group_by_column and group_by_column in result['columns']:
        from collections import Counter
        values = [row.get(group_by_column, '') for row in data]
        analysis['group_by'] = {
            'column': group_by_column,
            'unique_values': len(set(values)),
            'distribution': dict(Counter(values).most_common(20))
        }

    return analysis

def merge_csv_files(file_list, output_file, join_column=None):
    """Merge multiple CSV files"""
    try:
        all_data = []
        columns_set = set()

        for filename in file_list:
            result = read_csv(filename)
            if not result['success']:
                return {
                    'success': False,
                    'error': f"Error reading {filename}: {result['error']}"
                }
            all_data.extend(result['data'])
            columns_set.update(result['columns'])

        # Write merged file
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(columns_set))
            writer.writeheader()
            writer.writerows(all_data)

        return {
            'success': True,
            'files_merged': len(file_list),
            'total_rows': len(all_data),
            'output_file': output_file
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  preview <file> [rows]           - Preview CSV file")
        print("  validate <file> <col1,col2,...> - Validate required columns")
        print("  analyze <file> [group_by_col]   - Analyze GAM output")
        print("  merge <out_file> <file1> <file2> ... - Merge CSV files")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'preview':
        filename = sys.argv[2]
        rows = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = preview_csv(filename, rows)
        print(json.dumps(result, indent=2))

    elif command == 'validate':
        filename = sys.argv[2]
        required_cols = sys.argv[3].split(',')
        result = validate_csv_columns(filename, required_cols)
        print(json.dumps(result, indent=2))

    elif command == 'analyze':
        filename = sys.argv[2]
        group_by = sys.argv[3] if len(sys.argv) > 3 else None
        result = analyze_gam_output(filename, group_by)
        print(json.dumps(result, indent=2))

    elif command == 'merge':
        output_file = sys.argv[2]
        input_files = sys.argv[3:]
        result = merge_csv_files(input_files, output_file)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
