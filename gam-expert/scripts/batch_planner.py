#!/usr/bin/env python3
"""
GAM Batch Planner - Bulk Operation Planning and Optimization
Helps plan, optimize, and monitor large-scale GAM operations
"""

import sys
import json
import csv
import math
from typing import Dict, List, Optional
from pathlib import Path


# API quota limits (requests per 100 seconds per user)
# These are conservative estimates - actual limits may vary by domain
API_QUOTAS = {
    'admin_directory': 2400,      # User/Group operations
    'gmail': 250,                  # Gmail operations
    'drive': 1200,                 # Drive operations
    'calendar': 500,               # Calendar operations
    'classroom': 500,              # Classroom operations
    'default': 1000                # Conservative default
}

# Estimated API calls per operation type
API_COST = {
    'create_user': 1,
    'update_user': 1,
    'delete_user': 1,
    'get_user': 1,
    'add_group_member': 1,
    'remove_group_member': 1,
    'update_group': 1,
    'add_drive_permission': 2,     # Read + Write
    'remove_drive_permission': 2,
    'send_email': 1,
    'create_calendar_event': 1,
    'default': 1
}


def count_csv_rows(filepath: str) -> int:
    """Count rows in a CSV file (excluding header)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            return sum(1 for row in reader)
    except FileNotFoundError:
        return -1
    except Exception as e:
        return -1


def analyze_bulk_operation(operation_type: str, entity_count: int,
                          csv_file: Optional[str] = None) -> Dict:
    """
    Analyze a bulk operation and provide planning recommendations

    Args:
        operation_type: Type of operation (e.g., 'update_user', 'add_group_member')
        entity_count: Number of entities to process
        csv_file: Optional CSV file path to analyze

    Returns:
        Dict with analysis and recommendations
    """
    # If CSV file provided, count actual rows
    if csv_file:
        actual_count = count_csv_rows(csv_file)
        if actual_count > 0:
            entity_count = actual_count

    # Determine API category
    api_category = 'admin_directory'
    if 'email' in operation_type or 'message' in operation_type:
        api_category = 'gmail'
    elif 'drive' in operation_type:
        api_category = 'drive'
    elif 'calendar' in operation_type:
        api_category = 'calendar'
    elif 'classroom' in operation_type:
        api_category = 'classroom'

    # Get quota limit and API cost
    quota_limit = API_QUOTAS.get(api_category, API_QUOTAS['default'])
    api_cost_per_op = API_COST.get(operation_type, API_COST['default'])

    # Calculate total API calls needed
    total_api_calls = entity_count * api_cost_per_op

    # Calculate optimal batch size
    # Conservative approach: use 80% of quota to leave headroom
    safe_quota = int(quota_limit * 0.8)
    optimal_batch_size = min(safe_quota // api_cost_per_op, entity_count)

    # Calculate number of batches needed
    num_batches = math.ceil(entity_count / optimal_batch_size)

    # Estimate time (assuming 100 seconds per batch)
    estimated_seconds = num_batches * 100
    estimated_minutes = estimated_seconds / 60

    # Generate recommendations
    recommendations = []

    if entity_count > 1000:
        recommendations.append(
            f"⚠️  Large operation: {entity_count} entities. "
            "Consider splitting into multiple runs on different days."
        )

    if num_batches > 1:
        recommendations.append(
            f"Use batch_size parameter: Set to {optimal_batch_size} "
            f"to stay within API quota limits."
        )

    if estimated_minutes > 30:
        recommendations.append(
            f"⏱️  Long-running operation: Estimated {estimated_minutes:.0f} minutes. "
            "Run during off-peak hours and monitor for errors."
        )

    if api_category == 'gmail' and entity_count > 100:
        recommendations.append(
            "Gmail API has strict quotas. Consider using batch_size of 50-100 "
            "and allow 2-3 minute delays between batches."
        )

    # Risk assessment
    if entity_count < 10:
        risk_level = "LOW"
    elif entity_count < 100:
        risk_level = "MEDIUM"
    elif entity_count < 1000:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        'success': True,
        'analysis': {
            'operation_type': operation_type,
            'api_category': api_category,
            'entity_count': entity_count,
            'total_api_calls': total_api_calls,
            'quota_limit': quota_limit,
            'api_cost_per_operation': api_cost_per_op
        },
        'planning': {
            'optimal_batch_size': optimal_batch_size,
            'num_batches': num_batches,
            'estimated_duration_minutes': round(estimated_minutes, 1),
            'risk_level': risk_level
        },
        'recommendations': recommendations,
        'suggested_command_options': generate_batch_options(optimal_batch_size)
    }


def generate_batch_options(batch_size: int) -> str:
    """Generate GAM command options for batching"""
    return f"batch_size {batch_size} wait_on_fail"


def split_csv_file(input_file: str, output_prefix: str, rows_per_file: int) -> Dict:
    """
    Split a large CSV file into smaller batches

    Args:
        input_file: Input CSV file path
        output_prefix: Prefix for output files (e.g., 'batch_')
        rows_per_file: Number of rows per output file

    Returns:
        Dict with split results
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)

        total_rows = len(rows)
        num_files = math.ceil(total_rows / rows_per_file)
        output_files = []

        for i in range(num_files):
            start_idx = i * rows_per_file
            end_idx = min(start_idx + rows_per_file, total_rows)
            batch_rows = rows[start_idx:end_idx]

            output_file = f"{output_prefix}{i+1:03d}.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(batch_rows)

            output_files.append({
                'file': output_file,
                'row_count': len(batch_rows),
                'range': f"{start_idx+1}-{end_idx}"
            })

        return {
            'success': True,
            'input_file': input_file,
            'total_rows': total_rows,
            'rows_per_file': rows_per_file,
            'num_files': num_files,
            'output_files': output_files
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def generate_progress_script(operation: str, csv_files: List[str],
                             output_file: str = 'run_batches.sh') -> Dict:
    """
    Generate a shell script to run batched operations with progress tracking

    Args:
        operation: GAM command template with {csv_file} placeholder
        csv_files: List of CSV batch files
        output_file: Output script filename

    Returns:
        Dict with script generation results
    """
    try:
        script_lines = [
            '#!/bin/bash',
            '# Auto-generated batch processing script',
            '# Generated by GAM Batch Planner',
            '',
            'TOTAL_BATCHES=' + str(len(csv_files)),
            'CURRENT_BATCH=0',
            'FAILED_BATCHES=()',
            '',
            'echo "Starting batch processing: $TOTAL_BATCHES batches"',
            'echo "Started at: $(date)"',
            'echo ""',
            ''
        ]

        for i, csv_file in enumerate(csv_files, 1):
            cmd = operation.replace('{csv_file}', csv_file)
            script_lines.extend([
                f'# Batch {i}/{len(csv_files)}',
                'CURRENT_BATCH=' + str(i),
                f'echo "Processing batch $CURRENT_BATCH/$TOTAL_BATCHES: {csv_file}"',
                f'if {cmd}; then',
                '  echo "✓ Batch $CURRENT_BATCH completed successfully"',
                'else',
                '  echo "✗ Batch $CURRENT_BATCH FAILED"',
                f'  FAILED_BATCHES+=("{csv_file}")',
                'fi',
                'echo ""',
                ''
            ])

        script_lines.extend([
            'echo "Batch processing complete at: $(date)"',
            'echo ""',
            'if [ ${#FAILED_BATCHES[@]} -eq 0 ]; then',
            '  echo "✓ All batches completed successfully!"',
            'else',
            '  echo "✗ ${#FAILED_BATCHES[@]} batch(es) failed:"',
            '  for batch in "${FAILED_BATCHES[@]}"; do',
            '    echo "  - $batch"',
            '  done',
            '  exit 1',
            'fi'
        ])

        script_content = '\n'.join(script_lines)

        with open(output_file, 'w') as f:
            f.write(script_content)

        # Make script executable
        import os
        os.chmod(output_file, 0o755)

        return {
            'success': True,
            'script_file': output_file,
            'batch_count': len(csv_files),
            'message': f'Generated executable script: {output_file}'
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def estimate_completion_time(current_batch: int, total_batches: int,
                            elapsed_seconds: float) -> Dict:
    """
    Estimate remaining time based on current progress

    Args:
        current_batch: Number of batches completed
        total_batches: Total number of batches
        elapsed_seconds: Seconds elapsed so far

    Returns:
        Dict with time estimates
    """
    if current_batch == 0:
        return {
            'success': False,
            'error': 'No batches completed yet - cannot estimate'
        }

    avg_seconds_per_batch = elapsed_seconds / current_batch
    remaining_batches = total_batches - current_batch
    estimated_remaining_seconds = remaining_batches * avg_seconds_per_batch

    completion_pct = (current_batch / total_batches) * 100

    return {
        'success': True,
        'progress': {
            'current_batch': current_batch,
            'total_batches': total_batches,
            'completion_percentage': round(completion_pct, 1),
            'batches_remaining': remaining_batches
        },
        'timing': {
            'elapsed_seconds': round(elapsed_seconds, 1),
            'elapsed_minutes': round(elapsed_seconds / 60, 1),
            'avg_seconds_per_batch': round(avg_seconds_per_batch, 1),
            'estimated_remaining_seconds': round(estimated_remaining_seconds, 1),
            'estimated_remaining_minutes': round(estimated_remaining_seconds / 60, 1),
            'estimated_total_minutes': round((elapsed_seconds + estimated_remaining_seconds) / 60, 1)
        }
    }


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  analyze <operation_type> <count> [csv_file]")
        print("    - Analyze bulk operation and suggest batching strategy")
        print("    - Example: analyze update_user 500 users.csv")
        print()
        print("  split <input_csv> <output_prefix> <rows_per_file>")
        print("    - Split large CSV into smaller batch files")
        print("    - Example: split users.csv batch_ 100")
        print()
        print("  script <gam_command> <csv_files...>")
        print("    - Generate progress tracking script")
        print("    - Example: script 'gam csvfile {csv_file}:email ...' batch_001.csv batch_002.csv")
        print()
        print("  estimate <current> <total> <elapsed_seconds>")
        print("    - Estimate completion time based on current progress")
        print("    - Example: estimate 5 20 300")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'analyze':
        if len(sys.argv) < 4:
            print("Error: analyze requires operation_type and count")
            sys.exit(1)

        operation_type = sys.argv[2]
        try:
            count = int(sys.argv[3])
        except ValueError:
            print(f"Error: count must be a number, got '{sys.argv[3]}'")
            sys.exit(1)

        csv_file = sys.argv[4] if len(sys.argv) > 4 else None
        result = analyze_bulk_operation(operation_type, count, csv_file)
        print(json.dumps(result, indent=2))

    elif action == 'split':
        if len(sys.argv) < 5:
            print("Error: split requires input_csv, output_prefix, and rows_per_file")
            sys.exit(1)

        input_csv = sys.argv[2]
        output_prefix = sys.argv[3]
        try:
            rows_per_file = int(sys.argv[4])
        except ValueError:
            print(f"Error: rows_per_file must be a number")
            sys.exit(1)

        result = split_csv_file(input_csv, output_prefix, rows_per_file)
        print(json.dumps(result, indent=2))

    elif action == 'script':
        if len(sys.argv) < 4:
            print("Error: script requires gam_command and csv_files")
            sys.exit(1)

        gam_command = sys.argv[2]
        csv_files = sys.argv[3:]
        result = generate_progress_script(gam_command, csv_files)
        print(json.dumps(result, indent=2))

    elif action == 'estimate':
        if len(sys.argv) < 5:
            print("Error: estimate requires current, total, and elapsed_seconds")
            sys.exit(1)

        try:
            current = int(sys.argv[2])
            total = int(sys.argv[3])
            elapsed = float(sys.argv[4])
        except ValueError:
            print("Error: arguments must be numbers")
            sys.exit(1)

        result = estimate_completion_time(current, total, elapsed)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == '__main__':
    main()
