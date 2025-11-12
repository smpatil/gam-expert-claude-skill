#!/usr/bin/env python3
"""
GAM Error Analyzer - Parse and diagnose GAM error messages
Provides solutions and recommendations for common GAM errors
"""

import sys
import json
import re
from typing import Dict, List, Optional, Tuple


# Error patterns and their solutions
ERROR_PATTERNS = [
    {
        'pattern': r'command not found.*gam',
        'category': 'installation',
        'severity': 'critical',
        'title': 'GAM not installed or not in PATH',
        'description': 'The gam command is not available in your system PATH.',
        'solutions': [
            'Verify GAM installation: Run `which gam` or `where gam`',
            'If not installed, follow installation guide: https://github.com/GAM-team/GAM/wiki',
            'If installed, add GAM directory to PATH environment variable',
            'On macOS/Linux: Add `export PATH=$PATH:/path/to/gam` to ~/.bashrc or ~/.zshrc',
            'On Windows: Add GAM directory to System Environment Variables'
        ]
    },
    {
        'pattern': r'Error:\s*oauth2\.txt\s*(not found|does not exist)',
        'category': 'authentication',
        'severity': 'critical',
        'title': 'OAuth2 authentication not configured',
        'description': 'GAM has not been authenticated with Google Workspace.',
        'solutions': [
            'Run: gam oauth create',
            'Follow the authentication prompts in your browser',
            'Ensure you authenticate with a Google Workspace super admin account',
            'Verify oauth2.txt was created in your GAM configuration directory',
            'Check GAM config directory: gam version (shows config file path)'
        ]
    },
    {
        'pattern': r'insufficient.*permission|does not have.*scope',
        'category': 'authorization',
        'severity': 'high',
        'title': 'Insufficient API permissions/scopes',
        'description': 'GAM lacks the necessary API scopes for this operation.',
        'solutions': [
            'Re-authorize GAM with required scopes: gam oauth create',
            'During auth, ensure all requested permissions are granted',
            'Check which scopes are currently authorized: gam oauth info',
            'For specific APIs, authorize specific scopes: gam oauth create <scope>',
            'Verify your admin account has necessary privileges in Admin Console'
        ]
    },
    {
        'pattern': r'(403|Forbidden)|Not authorized|Access denied',
        'category': 'authorization',
        'severity': 'high',
        'title': 'Access denied - Forbidden',
        'description': 'Your account lacks permission to perform this action.',
        'solutions': [
            'Verify you are authenticated as a Google Workspace super admin',
            'Check domain-wide delegation is properly configured for service accounts',
            'Ensure the API is enabled in Google Cloud Console',
            'For Drive operations, verify you have access to the specific resource',
            'Check organizational unit restrictions in Admin Console'
        ]
    },
    {
        'pattern': r'(404|Not found)|Entity does not exist|Resource not found',
        'category': 'entity',
        'severity': 'medium',
        'title': 'Entity not found',
        'description': 'The specified user, group, or resource does not exist.',
        'solutions': [
            'Verify the email address or identifier is spelled correctly',
            'For users: Check if user exists with `gam info user <email>`',
            'For groups: Check if group exists with `gam info group <email>`',
            'For Drive files: Verify the file ID is correct',
            'Check if entity was recently deleted (may still be in API cache)'
        ]
    },
    {
        'pattern': r'(429|Quota exceeded)|Rate limit|Too many requests',
        'category': 'quota',
        'severity': 'medium',
        'title': 'API quota/rate limit exceeded',
        'description': 'You have exceeded the API rate limits for this operation.',
        'solutions': [
            'Wait a few minutes before retrying',
            'Use batch_size parameter to throttle requests: batch_size 50',
            'Add wait_on_fail to automatically retry: wait_on_fail',
            'Split large operations across multiple days',
            'Check quota usage in Google Cloud Console',
            'Consider requesting quota increase for your project'
        ]
    },
    {
        'pattern': r'(400|Bad request)|Invalid.*value|Malformed',
        'category': 'syntax',
        'severity': 'medium',
        'title': 'Invalid request - Bad syntax',
        'description': 'The command syntax or parameter values are incorrect.',
        'solutions': [
            'Check GAM wiki documentation for correct syntax',
            'Verify all required parameters are provided',
            'Check for typos in command, entity names, and options',
            'Ensure quotes are properly balanced around values with spaces',
            'Validate CSV file format if using csvfile',
            'Try command with a single test entity first'
        ]
    },
    {
        'pattern': r'(409|Conflict)|Already exists|Duplicate',
        'category': 'conflict',
        'severity': 'low',
        'title': 'Entity already exists',
        'description': 'The resource you are trying to create already exists.',
        'solutions': [
            'Check if entity already exists before creating',
            'Use update instead of create if entity exists',
            'For users: Check with `gam info user <email>`',
            'For groups: Check with `gam info group <email>`',
            'Consider using "create user ... notifyparent false" to avoid duplicate parent notifications'
        ]
    },
    {
        'pattern': r'service account|client_secrets\.json',
        'category': 'service_account',
        'severity': 'high',
        'title': 'Service account configuration issue',
        'description': 'Problem with service account authentication or client_secrets.json.',
        'solutions': [
            'Verify client_secrets.json is in GAM config directory',
            'Ensure service account has domain-wide delegation enabled',
            'Add required API scopes to service account in Admin Console',
            'Navigate to: Security > API controls > Domain-wide delegation',
            'Verify Client ID matches the one in client_secrets.json',
            'Re-download client_secrets.json from Google Cloud Console if corrupted'
        ]
    },
    {
        'pattern': r'ssl.*error|certificate.*error|CERTIFICATE_VERIFY_FAILED',
        'category': 'network',
        'severity': 'medium',
        'title': 'SSL/Certificate error',
        'description': 'Problem verifying SSL certificates.',
        'solutions': [
            'Check your internet connection',
            'Verify system date and time are correct',
            'Update SSL certificates: Update your operating system',
            'Check corporate proxy/firewall settings',
            'Try: gam config no_verify_ssl true (NOT recommended for production)',
            'Contact IT if behind corporate firewall'
        ]
    },
    {
        'pattern': r'name or service not known|Failed to establish connection|Connection refused',
        'category': 'network',
        'severity': 'high',
        'title': 'Network connectivity error',
        'description': 'Cannot connect to Google APIs.',
        'solutions': [
            'Check your internet connection',
            'Verify firewall allows access to Google APIs',
            'Check if proxy configuration is needed',
            'Test connectivity: ping google.com',
            'Verify DNS is working correctly',
            'Try accessing https://admin.google.com in browser'
        ]
    },
    {
        'pattern': r'csv.*file.*not found|No such file',
        'category': 'file',
        'severity': 'medium',
        'title': 'CSV file not found',
        'description': 'The specified CSV file cannot be found.',
        'solutions': [
            'Verify the file path is correct',
            'Use absolute path instead of relative path',
            'Check file exists: ls <filename>',
            'Ensure file name is spelled correctly (case-sensitive)',
            'Verify you are in the correct directory: pwd',
            'Check file permissions: ls -l <filename>'
        ]
    },
    {
        'pattern': r'InvalidValue.*orgUnitPath',
        'category': 'entity',
        'severity': 'medium',
        'title': 'Invalid organizational unit path',
        'description': 'The specified OU path does not exist or is malformed.',
        'solutions': [
            'OU paths must start with "/" (forward slash)',
            'OU paths are case-sensitive',
            'List all OUs to find correct path: gam print ous',
            'Ensure OU path is quoted: ou "/Sales/West"',
            'Use proper hierarchy: /ParentOU/ChildOU',
            'Verify OU exists in Admin Console'
        ]
    },
    {
        'pattern': r'Member not found|is not a member',
        'category': 'entity',
        'severity': 'low',
        'title': 'Group member not found',
        'description': 'The user is not a member of the specified group.',
        'solutions': [
            'Verify user email is correct',
            'Check current group membership: gam info group <group>',
            'List all members: gam print group-members group <group>',
            'For external members, ensure group allows external users',
            'Try adding member first before removing/updating'
        ]
    },
    {
        'pattern': r'Cyclic memberships not allowed',
        'category': 'conflict',
        'severity': 'medium',
        'title': 'Cyclic group membership detected',
        'description': 'Cannot add group as member because it would create a cycle.',
        'solutions': [
            'Cannot add Group A to Group B if B is already a member of A',
            'Review group membership hierarchy',
            'Remove the reverse membership first',
            'Redesign group structure to avoid cycles',
            'Use gam print groups to visualize group relationships'
        ]
    }
]


def analyze_error(error_message: str) -> Dict:
    """
    Analyze a GAM error message and provide solutions

    Args:
        error_message: Error message from GAM command

    Returns:
        Dict with error analysis and solutions
    """
    matches = []

    # Try to match error patterns
    for error_info in ERROR_PATTERNS:
        if re.search(error_info['pattern'], error_message, re.IGNORECASE):
            matches.append({
                'category': error_info['category'],
                'severity': error_info['severity'],
                'title': error_info['title'],
                'description': error_info['description'],
                'solutions': error_info['solutions']
            })

    # Extract HTTP status codes if present
    http_codes = re.findall(r'\b(4\d{2}|5\d{2})\b', error_message)

    # Extract entity information
    entities = extract_entities_from_error(error_message)

    if not matches:
        # Generic error analysis
        matches.append({
            'category': 'unknown',
            'severity': 'medium',
            'title': 'Unrecognized error',
            'description': 'This error pattern is not in the database.',
            'solutions': [
                'Check the full error message for specific details',
                'Search GAM wiki for similar errors',
                'Check GAM GitHub issues: https://github.com/GAM-team/GAM/issues',
                'Verify command syntax in GAM documentation',
                'Try running command with a single test entity',
                'Enable debug mode: gam config debug_level info',
                'Post in GAM Google Group with full error details'
            ]
        })

    return {
        'success': True,
        'error_message': error_message,
        'matches': matches,
        'http_codes': http_codes,
        'entities_mentioned': entities,
        'primary_match': matches[0] if matches else None
    }


def extract_entities_from_error(error_message: str) -> Dict:
    """Extract entity references from error message"""
    entities = {
        'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', error_message),
        'ous': re.findall(r'/[A-Za-z0-9/_-]+', error_message),
        'file_ids': re.findall(r'\b[A-Za-z0-9_-]{20,}\b', error_message)
    }
    return {k: v for k, v in entities.items() if v}


def categorize_errors_from_log(log_file: str) -> Dict:
    """
    Parse a GAM log file and categorize errors

    Args:
        log_file: Path to GAM log file

    Returns:
        Dict with categorized errors
    """
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()

        # Find error lines
        error_lines = [line for line in log_content.split('\n')
                      if 'error' in line.lower() or 'failed' in line.lower()]

        categories = {}
        for line in error_lines:
            result = analyze_error(line)
            if result['matches']:
                category = result['matches'][0]['category']
                categories[category] = categories.get(category, 0) + 1

        return {
            'success': True,
            'log_file': log_file,
            'total_error_lines': len(error_lines),
            'error_categories': categories,
            'sample_errors': error_lines[:10]
        }

    except FileNotFoundError:
        return {
            'success': False,
            'error': f'Log file not found: {log_file}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def suggest_debug_commands(error_category: str) -> List[str]:
    """
    Suggest GAM commands to help debug specific error categories

    Args:
        error_category: Category of error

    Returns:
        List of suggested debug commands
    """
    debug_commands = {
        'authentication': [
            'gam version',
            'gam oauth info',
            'gam info domain'
        ],
        'authorization': [
            'gam oauth info',
            'gam user <admin@domain.com> check serviceaccount',
            'gam info domain'
        ],
        'entity': [
            'gam info user <email>',
            'gam info group <email>',
            'gam print users',
            'gam print groups'
        ],
        'quota': [
            'gam info domain',
            'gam report usage customer',
        ],
        'network': [
            'ping google.com',
            'curl https://www.googleapis.com',
            'gam version'
        ],
        'file': [
            'ls -la <filename>',
            'pwd',
            'head <filename>'
        ]
    }

    return debug_commands.get(error_category, ['gam version', 'gam info domain'])


def format_error_report(analysis: Dict, verbose: bool = False) -> str:
    """Format error analysis as human-readable text"""
    if not analysis['success'] or not analysis['matches']:
        return "Unable to analyze error"

    primary = analysis['primary_match']

    lines = [
        "=" * 70,
        f"ERROR ANALYSIS: {primary['title']}",
        "=" * 70,
        f"Severity: {primary['severity'].upper()}",
        f"Category: {primary['category']}",
        "",
        "DESCRIPTION:",
        primary['description'],
        "",
        "SOLUTIONS:",
    ]

    for i, solution in enumerate(primary['solutions'], 1):
        lines.append(f"{i}. {solution}")

    if analysis['entities_mentioned']:
        lines.extend([
            "",
            "ENTITIES MENTIONED:",
            json.dumps(analysis['entities_mentioned'], indent=2)
        ])

    if verbose and len(analysis['matches']) > 1:
        lines.extend([
            "",
            "OTHER POSSIBLE CAUSES:",
        ])
        for match in analysis['matches'][1:]:
            lines.append(f"- {match['title']}")

    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  analyze <error_message>     - Analyze a specific error message")
        print("  logfile <log_file>          - Categorize errors from log file")
        print("  debug <category>            - Show debug commands for error category")
        print()
        print("Example:")
        print('  error_analyzer.py analyze "Error: oauth2.txt not found"')
        print('  error_analyzer.py logfile gam.log')
        print('  error_analyzer.py debug authentication')
        sys.exit(1)

    action = sys.argv[1]

    if action == 'analyze':
        if len(sys.argv) < 3:
            print("Error: analyze requires error message")
            sys.exit(1)

        error_message = ' '.join(sys.argv[2:])
        result = analyze_error(error_message)

        # Print formatted report
        print(format_error_report(result, verbose=True))
        print()
        print("JSON output:")
        print(json.dumps(result, indent=2))

    elif action == 'logfile':
        if len(sys.argv) < 3:
            print("Error: logfile requires log file path")
            sys.exit(1)

        log_file = sys.argv[2]
        result = categorize_errors_from_log(log_file)
        print(json.dumps(result, indent=2))

    elif action == 'debug':
        if len(sys.argv) < 3:
            print("Error: debug requires error category")
            sys.exit(1)

        category = sys.argv[2]
        commands = suggest_debug_commands(category)

        print(f"Debug commands for '{category}' errors:")
        print()
        for cmd in commands:
            print(f"  {cmd}")

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == '__main__':
    main()
