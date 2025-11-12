#!/usr/bin/env python3
"""
GAM CSV Template Generator
Generates CSV templates and sample data for common GAM operations
"""

import sys
import json
import csv
from typing import Dict, List, Optional


# Template definitions for common GAM operations
TEMPLATES = {
    'users_create': {
        'description': 'Create new users',
        'columns': [
            'email',
            'firstname',
            'lastname',
            'password',
            'orgunitpath',
            'changepassword'
        ],
        'required': ['email', 'firstname', 'lastname', 'password'],
        'sample_data': [
            ['john.smith@example.com', 'John', 'Smith', 'TempPass123!', '/Sales', 'true'],
            ['jane.doe@example.com', 'Jane', 'Doe', 'TempPass456!', '/Marketing', 'true']
        ]
    },
    'users_update': {
        'description': 'Update existing users',
        'columns': [
            'email',
            'orgunitpath',
            'suspended',
            'changepassword'
        ],
        'required': ['email'],
        'sample_data': [
            ['user1@example.com', '/Engineering', 'false', 'false'],
            ['user2@example.com', '/Sales', 'false', 'true']
        ]
    },
    'users_suspend': {
        'description': 'Suspend user accounts',
        'columns': ['email', 'reason'],
        'required': ['email'],
        'sample_data': [
            ['terminated.user@example.com', 'Employment ended'],
            ['inactive.user@example.com', 'Long-term leave']
        ]
    },
    'group_members_add': {
        'description': 'Add members to groups',
        'columns': ['group', 'email', 'role'],
        'required': ['group', 'email'],
        'sample_data': [
            ['sales@example.com', 'john.smith@example.com', 'MEMBER'],
            ['sales@example.com', 'jane.doe@example.com', 'MEMBER'],
            ['sales@example.com', 'manager@example.com', 'MANAGER']
        ]
    },
    'group_members_remove': {
        'description': 'Remove members from groups',
        'columns': ['group', 'email'],
        'required': ['group', 'email'],
        'sample_data': [
            ['marketing@example.com', 'former.employee@example.com'],
            ['allstaff@example.com', 'contractor@example.com']
        ]
    },
    'groups_create': {
        'description': 'Create new groups',
        'columns': [
            'email',
            'name',
            'description',
            'whocanjoin',
            'whocanpostmessage'
        ],
        'required': ['email', 'name'],
        'sample_data': [
            ['team-eng@example.com', 'Engineering Team', 'Engineering department', 'INVITED_CAN_JOIN', 'ALL_MEMBERS_CAN_POST'],
            ['team-sales@example.com', 'Sales Team', 'Sales department', 'INVITED_CAN_JOIN', 'ALL_MEMBERS_CAN_POST']
        ]
    },
    'aliases_add': {
        'description': 'Add email aliases to users',
        'columns': ['user_email', 'alias'],
        'required': ['user_email', 'alias'],
        'sample_data': [
            ['john.smith@example.com', 'jsmith@example.com'],
            ['jane.doe@example.com', 'j.doe@example.com']
        ]
    },
    'drive_permissions': {
        'description': 'Add Drive file permissions',
        'columns': [
            'file_id',
            'email',
            'role',
            'type'
        ],
        'required': ['file_id', 'email', 'role'],
        'sample_data': [
            ['1ABC123xyz', 'user1@example.com', 'writer', 'user'],
            ['1ABC123xyz', 'team@example.com', 'reader', 'group']
        ]
    },
    'calendar_permissions': {
        'description': 'Set calendar ACL permissions',
        'columns': ['user_email', 'calendar_id', 'permission_email', 'role'],
        'required': ['user_email', 'calendar_id', 'permission_email', 'role'],
        'sample_data': [
            ['admin@example.com', 'conference.room@example.com', 'team@example.com', 'editor'],
            ['admin@example.com', 'shared.calendar@example.com', 'user@example.com', 'reader']
        ]
    },
    'ou_move': {
        'description': 'Move users to different organizational units',
        'columns': ['email', 'orgunitpath'],
        'required': ['email', 'orgunitpath'],
        'sample_data': [
            ['promoted.user@example.com', '/Management'],
            ['transferred.user@example.com', '/Sales/Enterprise']
        ]
    },
    'password_reset': {
        'description': 'Reset user passwords',
        'columns': ['email', 'password', 'changepassword'],
        'required': ['email', 'password'],
        'sample_data': [
            ['user1@example.com', 'NewTemp123!', 'true'],
            ['user2@example.com', 'NewTemp456!', 'true']
        ]
    },
    'delegation_add': {
        'description': 'Add email delegation',
        'columns': ['user_email', 'delegate_email'],
        'required': ['user_email', 'delegate_email'],
        'sample_data': [
            ['manager@example.com', 'assistant@example.com'],
            ['executive@example.com', 'admin@example.com']
        ]
    }
}


def list_templates() -> Dict:
    """List all available templates"""
    template_list = []
    for key, template in TEMPLATES.items():
        template_list.append({
            'key': key,
            'description': template['description'],
            'columns': template['columns'],
            'required_columns': template['required']
        })

    return {
        'success': True,
        'count': len(template_list),
        'templates': template_list
    }


def generate_template(template_key: str, output_file: str,
                     include_samples: bool = True,
                     sample_rows: int = 2) -> Dict:
    """
    Generate a CSV template file

    Args:
        template_key: Key of template to generate
        output_file: Output CSV filename
        include_samples: Include sample data rows
        sample_rows: Number of sample rows to include

    Returns:
        Dict with generation results
    """
    if template_key not in TEMPLATES:
        return {
            'success': False,
            'error': f'Unknown template: {template_key}',
            'available_templates': list(TEMPLATES.keys())
        }

    template = TEMPLATES[template_key]

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(template['columns'])

            # Write sample data if requested
            if include_samples and template['sample_data']:
                for row in template['sample_data'][:sample_rows]:
                    writer.writerow(row)

        return {
            'success': True,
            'template': template_key,
            'description': template['description'],
            'output_file': output_file,
            'columns': template['columns'],
            'required_columns': template['required'],
            'sample_rows_included': sample_rows if include_samples else 0
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def generate_custom_template(columns: List[str], output_file: str,
                            sample_rows: int = 0) -> Dict:
    """
    Generate a custom CSV template with specified columns

    Args:
        columns: List of column names
        output_file: Output CSV filename
        sample_rows: Number of empty sample rows to include

    Returns:
        Dict with generation results
    """
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(columns)

            # Write empty sample rows
            for _ in range(sample_rows):
                writer.writerow([''] * len(columns))

        return {
            'success': True,
            'output_file': output_file,
            'columns': columns,
            'sample_rows': sample_rows
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def validate_csv(csv_file: str, required_columns: List[str]) -> Dict:
    """
    Validate that CSV has required columns and check for common issues

    Args:
        csv_file: CSV file to validate
        required_columns: List of required column names

    Returns:
        Dict with validation results
    """
    issues = []
    warnings = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

            if not fieldnames:
                return {
                    'success': False,
                    'error': 'CSV file has no header row'
                }

            # Check required columns
            actual_columns = set(fieldnames)
            required_set = set(required_columns)
            missing = required_set - actual_columns

            if missing:
                issues.append(f"Missing required columns: {', '.join(missing)}")

            # Check for empty column names
            if '' in fieldnames or None in fieldnames:
                issues.append("CSV has empty column names")

            # Read all rows and check for issues
            rows = list(reader)

            if not rows:
                warnings.append("CSV has no data rows (only header)")

            # Check for empty required fields
            empty_required_fields = {}
            for i, row in enumerate(rows, start=2):  # Start at 2 (row 1 is header)
                for col in required_columns:
                    if col in row and not row[col].strip():
                        if col not in empty_required_fields:
                            empty_required_fields[col] = []
                        empty_required_fields[col].append(i)

            if empty_required_fields:
                for col, row_nums in empty_required_fields.items():
                    if len(row_nums) <= 5:
                        issues.append(
                            f"Required column '{col}' is empty in rows: {', '.join(map(str, row_nums))}"
                        )
                    else:
                        issues.append(
                            f"Required column '{col}' is empty in {len(row_nums)} rows"
                        )

            # Check for duplicate emails (if email column exists)
            if 'email' in actual_columns:
                emails = [row.get('email', '').strip().lower() for row in rows]
                duplicates = [email for email in set(emails) if emails.count(email) > 1 and email]
                if duplicates:
                    warnings.append(
                        f"Duplicate emails found: {', '.join(duplicates[:5])}"
                        + (' ...' if len(duplicates) > 5 else '')
                    )

            is_valid = len(issues) == 0

            return {
                'success': True,
                'is_valid': is_valid,
                'row_count': len(rows),
                'columns': list(fieldnames),
                'required_columns': required_columns,
                'missing_columns': list(missing),
                'issues': issues,
                'warnings': warnings
            }

    except FileNotFoundError:
        return {
            'success': False,
            'error': f'File not found: {csv_file}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def suggest_template(description: str) -> Dict:
    """
    Suggest templates based on user description

    Args:
        description: What the user wants to do

    Returns:
        Dict with suggested templates
    """
    description_lower = description.lower()

    suggestions = []

    # Keyword matching
    keywords = {
        'create user': ['users_create'],
        'new user': ['users_create'],
        'add user': ['users_create'],
        'update user': ['users_update'],
        'move user': ['ou_move'],
        'suspend': ['users_suspend'],
        'group': ['groups_create', 'group_members_add'],
        'add member': ['group_members_add'],
        'remove member': ['group_members_remove'],
        'alias': ['aliases_add'],
        'drive': ['drive_permissions'],
        'calendar': ['calendar_permissions'],
        'password': ['password_reset'],
        'delegation': ['delegation_add'],
        'ou ': ['ou_move']
    }

    for keyword, template_keys in keywords.items():
        if keyword in description_lower:
            for key in template_keys:
                if key not in [s['key'] for s in suggestions]:
                    template = TEMPLATES[key]
                    suggestions.append({
                        'key': key,
                        'description': template['description'],
                        'relevance': 'high' if keyword == description_lower.strip() else 'medium'
                    })

    if not suggestions:
        # Return most common templates
        common_templates = ['users_create', 'group_members_add', 'users_update']
        for key in common_templates:
            template = TEMPLATES[key]
            suggestions.append({
                'key': key,
                'description': template['description'],
                'relevance': 'low'
            })

    return {
        'success': True,
        'query': description,
        'suggestions': suggestions
    }


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  list                              - List all available templates")
        print("  generate <template_key> <output>  - Generate template CSV file")
        print("  custom <col1,col2,...> <output>   - Generate custom template")
        print("  validate <csv_file> <req_cols>    - Validate CSV file")
        print("  suggest <description>             - Suggest templates")
        print()
        print("Examples:")
        print("  csv_generator.py list")
        print("  csv_generator.py generate users_create new_users.csv")
        print("  csv_generator.py custom 'email,name,department' custom.csv")
        print("  csv_generator.py validate users.csv 'email,firstname,lastname'")
        print("  csv_generator.py suggest 'add users to group'")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'list':
        result = list_templates()
        print(json.dumps(result, indent=2))

    elif action == 'generate':
        if len(sys.argv) < 4:
            print("Error: generate requires template_key and output_file")
            sys.exit(1)

        template_key = sys.argv[2]
        output_file = sys.argv[3]
        result = generate_template(template_key, output_file)
        print(json.dumps(result, indent=2))

        if result['success']:
            print(f"\n✓ Template generated: {output_file}")

    elif action == 'custom':
        if len(sys.argv) < 4:
            print("Error: custom requires columns and output_file")
            sys.exit(1)

        columns = sys.argv[2].split(',')
        output_file = sys.argv[3]
        sample_rows = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        result = generate_custom_template(columns, output_file, sample_rows)
        print(json.dumps(result, indent=2))

        if result['success']:
            print(f"\n✓ Custom template generated: {output_file}")

    elif action == 'validate':
        if len(sys.argv) < 4:
            print("Error: validate requires csv_file and required_columns")
            sys.exit(1)

        csv_file = sys.argv[2]
        required_columns = sys.argv[3].split(',')
        result = validate_csv(csv_file, required_columns)
        print(json.dumps(result, indent=2))

        if result.get('is_valid'):
            print(f"\n✓ CSV is valid")
        else:
            print(f"\n✗ CSV has issues")

    elif action == 'suggest':
        if len(sys.argv) < 3:
            print("Error: suggest requires description")
            sys.exit(1)

        description = ' '.join(sys.argv[2:])
        result = suggest_template(description)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == '__main__':
    main()
