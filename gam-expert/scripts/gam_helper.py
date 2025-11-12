#!/usr/bin/env python3
"""
GAM Helper - Command Validation and Safety Checks
Provides utilities for constructing, validating, and analyzing GAM commands
"""

import sys
import json
import re
from typing import Dict, List, Optional, Tuple

# Command categories for safety analysis
DESTRUCTIVE_COMMANDS = {
    'delete', 'remove', 'suspend', 'deprovision', 'wipe',
    'clear', 'revoke', 'disable', 'purge'
}

MODIFY_COMMANDS = {
    'update', 'add', 'create', 'modify', 'change',
    'move', 'transfer', 'set', 'insert'
}

READ_ONLY_COMMANDS = {
    'print', 'show', 'info', 'get', 'list', 'report'
}

BULK_INDICATORS = {
    'all', 'csvfile', 'ou_and_children', 'group'
}


def analyze_command_safety(command: str) -> Dict:
    """
    Analyze a GAM command for safety concerns

    Args:
        command: GAM command string to analyze

    Returns:
        Dict with safety analysis
    """
    command_lower = command.lower()
    tokens = command.split()

    # Extract command type
    command_type = None
    for token in tokens[1:]:  # Skip 'gam'
        if token in DESTRUCTIVE_COMMANDS | MODIFY_COMMANDS | READ_ONLY_COMMANDS:
            command_type = token
            break

    # Check for destructive operations
    is_destructive = any(cmd in command_lower for cmd in DESTRUCTIVE_COMMANDS)
    is_modifying = any(cmd in command_lower for cmd in MODIFY_COMMANDS)
    is_read_only = any(cmd in command_lower for cmd in READ_ONLY_COMMANDS)

    # Check for bulk operations
    is_bulk = any(indicator in command_lower for indicator in BULK_INDICATORS)

    # Count estimated affected entities
    estimated_count = estimate_affected_entities(command)

    # Determine risk level
    if is_destructive:
        risk_level = "CRITICAL"
    elif is_modifying and (is_bulk or estimated_count > 10):
        risk_level = "HIGH"
    elif is_modifying:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Generate warnings
    warnings = []
    if is_destructive:
        warnings.append("⚠️  DESTRUCTIVE OPERATION - This action may be irreversible")
    if is_bulk:
        warnings.append("⚠️  BULK OPERATION - Will affect multiple entities")
    if estimated_count > 50:
        warnings.append(f"⚠️  LARGE SCALE - Estimated {estimated_count}+ entities affected")
    if 'suspend' in command_lower:
        warnings.append("⚠️  ACCOUNT SUSPENSION - Users will lose access")
    if 'delete' in command_lower and 'message' not in command_lower:
        warnings.append("⚠️  DELETION - Data may be permanently lost")
    if 'wipe' in command_lower:
        warnings.append("⚠️  DEVICE WIPE - Will erase all device data")

    # Determine if confirmation required
    requires_confirmation = (
        is_destructive or
        (is_modifying and is_bulk) or
        estimated_count > 5
    )

    return {
        'success': True,
        'command': command,
        'command_type': command_type,
        'risk_level': risk_level,
        'is_destructive': is_destructive,
        'is_modifying': is_modifying,
        'is_read_only': is_read_only,
        'is_bulk': is_bulk,
        'estimated_affected': estimated_count,
        'requires_confirmation': requires_confirmation,
        'warnings': warnings,
        'recommendation': generate_recommendation(
            is_destructive, is_modifying, is_bulk, estimated_count
        )
    }


def estimate_affected_entities(command: str) -> int:
    """Estimate number of entities affected by command"""
    command_lower = command.lower()

    # Check for explicit entity counts or bulk indicators
    if 'all users' in command_lower:
        return 1000  # Placeholder for "many"
    elif 'all groups' in command_lower:
        return 100
    elif 'csvfile' in command_lower:
        # Try to extract filename and count rows if possible
        return 50  # Placeholder
    elif 'ou_and_children' in command_lower:
        return 100  # Placeholder
    elif 'group' in command_lower and 'members' in command_lower:
        return 20  # Placeholder for group members
    elif re.search(r'\buser\s+\S+@', command_lower):
        return 1  # Single user
    elif re.search(r'\bgroup\s+\S+@', command_lower):
        return 1  # Single group
    else:
        return 1  # Default single entity


def generate_recommendation(is_destructive: bool, is_modifying: bool,
                           is_bulk: bool, count: int) -> str:
    """Generate safety recommendation based on command analysis"""
    if is_destructive and is_bulk:
        return (
            "CRITICAL: Test this command on a small sample first. "
            "Consider using a preview command (gam print) to verify selection. "
            "Ensure backups are available before proceeding."
        )
    elif is_destructive:
        return (
            "HIGH RISK: Verify the target entity is correct. "
            "This operation may be irreversible."
        )
    elif is_modifying and count > 50:
        return (
            "CAUTION: Test with a small subset first (1-5 entities). "
            "Monitor for errors before processing the full set."
        )
    elif is_modifying:
        return "Standard confirmation recommended before execution."
    else:
        return "Safe to execute - read-only operation."


def generate_preview_command(command: str) -> Optional[str]:
    """
    Convert a modify command to a preview/print command

    Args:
        command: GAM modify command

    Returns:
        Preview command string or None if not applicable
    """
    command_lower = command.lower()

    # User operations
    if 'update user' in command_lower or 'create user' in command_lower:
        if 'csvfile' in command_lower:
            # Extract CSV file reference
            match = re.search(r'csvfile\s+([^\s:]+)', command)
            if match:
                csv_file = match.group(1)
                return f"gam print users csvfile {csv_file}"
        else:
            # Single user - show current info
            match = re.search(r'(?:update|create)\s+user\s+(\S+)', command)
            if match:
                user_email = match.group(1)
                return f"gam user {user_email} show info"

    # Group operations
    if 'update group' in command_lower or 'add member' in command_lower:
        match = re.search(r'group\s+(\S+)', command)
        if match:
            group_email = match.group(1)
            return f"gam info group {group_email}"

    # OU operations
    if 'ou' in command_lower and 'update' in command_lower:
        match = re.search(r'ou\s+["\']([^"\']+)["\']', command)
        if match:
            ou_path = match.group(1)
            return f"gam print users ou \"{ou_path}\""

    # Drive operations
    if 'drive' in command_lower and ('add' in command_lower or 'update' in command_lower):
        match = re.search(r'user\s+(\S+)', command)
        if match:
            user_email = match.group(1)
            return f"gam user {user_email} show drivefileacls"

    return None


def validate_command_syntax(command: str) -> Dict:
    """
    Basic syntax validation for GAM commands

    Args:
        command: GAM command string

    Returns:
        Dict with validation results
    """
    errors = []
    warnings = []

    # Check if command starts with 'gam'
    if not command.strip().startswith('gam'):
        errors.append("Command must start with 'gam'")

    # Check for unbalanced quotes
    single_quotes = command.count("'")
    double_quotes = command.count('"')
    if single_quotes % 2 != 0:
        errors.append("Unbalanced single quotes")
    if double_quotes % 2 != 0:
        errors.append("Unbalanced double quotes")

    # Check for common typos
    common_typos = {
        'usre': 'user',
        'gorup': 'group',
        'craete': 'create',
        'delte': 'delete',
        'updte': 'update'
    }
    for typo, correction in common_typos.items():
        if typo in command.lower():
            warnings.append(f"Possible typo: '{typo}' should be '{correction}'")

    # Check for suspicious patterns
    if '~' in command and 'csvfile' not in command.lower():
        warnings.append("Tilde '~' found - ensure it's used correctly for CSV substitution")

    # Check for required entity specification
    command_lower = command.lower()
    if any(cmd in command_lower for cmd in ['update', 'delete', 'suspend']):
        if not any(ent in command_lower for ent in ['user', 'group', 'ou', 'orgunit', 'csvfile']):
            errors.append("Command appears to modify data but no entity type specified")

    is_valid = len(errors) == 0

    return {
        'success': True,
        'is_valid': is_valid,
        'errors': errors,
        'warnings': warnings,
        'command': command
    }


def extract_entities(command: str) -> Dict:
    """
    Extract entity references from a GAM command

    Args:
        command: GAM command string

    Returns:
        Dict with extracted entities
    """
    entities = {
        'users': [],
        'groups': [],
        'ous': [],
        'csv_files': [],
        'domains': []
    }

    # Extract email addresses (users/groups)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', command)
    for email in emails:
        if email not in entities['users'] and email not in entities['groups']:
            # Heuristic: groups often have generic names
            if any(keyword in email.lower() for keyword in ['group', 'team', 'dept', 'all']):
                entities['groups'].append(email)
            else:
                entities['users'].append(email)

    # Extract OU paths
    ou_matches = re.findall(r'ou\s+["\']([^"\']+)["\']', command, re.IGNORECASE)
    entities['ous'].extend(ou_matches)

    # Extract CSV files
    csv_matches = re.findall(r'csvfile\s+([^\s:]+)', command, re.IGNORECASE)
    entities['csv_files'].extend(csv_matches)

    # Extract domains
    domain_matches = re.findall(r'domain\s+(\S+)', command, re.IGNORECASE)
    entities['domains'].extend(domain_matches)

    return {
        'success': True,
        'entities': entities,
        'total_count': sum(len(v) for v in entities.values())
    }


def suggest_dry_run(command: str) -> Optional[str]:
    """
    Suggest a dry-run version of the command

    Args:
        command: Original GAM command

    Returns:
        Dry-run command or None if not applicable
    """
    # For many operations, using 'gam print' is the dry-run equivalent
    preview = generate_preview_command(command)
    if preview:
        return preview

    # For CSV bulk operations, suggest processing just first few rows
    if 'csvfile' in command.lower():
        return (
            "Create a test CSV with just 2-3 rows and run the command on that first. "
            "Example: head -n 4 original.csv > test.csv (includes header + 3 rows)"
        )

    return None


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  analyze <command>      - Analyze command safety")
        print("  validate <command>     - Validate command syntax")
        print("  preview <command>      - Generate preview/dry-run command")
        print("  extract <command>      - Extract entities from command")
        print()
        print("Example:")
        print('  gam_helper.py analyze "gam update group sales@example.com add member user@example.com"')
        sys.exit(1)

    action = sys.argv[1]

    if action in ['analyze', 'validate', 'preview', 'extract']:
        if len(sys.argv) < 3:
            print(f"Error: {action} requires a GAM command as argument")
            sys.exit(1)

        # Join remaining arguments as the command (handles quotes)
        command = ' '.join(sys.argv[2:])

    if action == 'analyze':
        result = analyze_command_safety(command)
        print(json.dumps(result, indent=2))

    elif action == 'validate':
        result = validate_command_syntax(command)
        print(json.dumps(result, indent=2))

    elif action == 'preview':
        preview = generate_preview_command(command)
        result = {
            'success': True,
            'original_command': command,
            'preview_command': preview,
            'dry_run_suggestion': suggest_dry_run(command) if not preview else None
        }
        print(json.dumps(result, indent=2))

    elif action == 'extract':
        result = extract_entities(command)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == '__main__':
    main()
