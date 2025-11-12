#!/usr/bin/env python3
"""
GAM Config Checker - Environment and Configuration Validation
Verifies GAM installation, authentication, and readiness
"""

import sys
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def run_command(cmd: List[str], timeout: int = 10) -> Tuple[bool, str, str]:
    """
    Run a shell command and return success status and output

    Args:
        cmd: Command as list of strings
        timeout: Timeout in seconds

    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, '', 'Command timed out')
    except FileNotFoundError:
        return (False, '', f'Command not found: {cmd[0]}')
    except Exception as e:
        return (False, '', str(e))


def check_gam_installation() -> Dict:
    """Check if GAM is installed and accessible"""
    checks = {
        'gam_command_available': False,
        'gam_path': None,
        'gam_version': None,
        'python_version': None
    }

    # Check if gam command exists
    success, stdout, stderr = run_command(['which', 'gam'])
    if not success:
        # Try Windows 'where' command
        success, stdout, stderr = run_command(['where', 'gam'])

    if success:
        checks['gam_command_available'] = True
        checks['gam_path'] = stdout.strip()

    # Get GAM version
    success, stdout, stderr = run_command(['gam', 'version'])
    if success:
        checks['gam_version'] = stdout.strip()

        # Extract Python version from GAM version output
        import re
        python_match = re.search(r'Python ([\d.]+)', stdout)
        if python_match:
            checks['python_version'] = python_match.group(1)

    return {
        'success': checks['gam_command_available'],
        'checks': checks,
        'issues': [] if checks['gam_command_available'] else [
            'GAM command not found in PATH',
            'Install GAM from: https://github.com/GAM-team/GAM/wiki'
        ]
    }


def check_gam_authentication() -> Dict:
    """Check if GAM is authenticated"""
    checks = {
        'oauth_configured': False,
        'oauth_info': None,
        'service_account_configured': False,
        'domain': None
    }

    issues = []

    # Check oauth info
    success, stdout, stderr = run_command(['gam', 'oauth', 'info'], timeout=15)
    if success:
        checks['oauth_configured'] = True
        checks['oauth_info'] = stdout.strip()
    else:
        issues.append('OAuth not configured - Run: gam oauth create')

    # Check domain info
    success, stdout, stderr = run_command(['gam', 'info', 'domain'], timeout=15)
    if success:
        checks['domain'] = stdout.strip()

        # Check for service account mention
        if 'service account' in stdout.lower():
            checks['service_account_configured'] = True
    else:
        if 'oauth2.txt' in stderr.lower():
            issues.append('oauth2.txt not found - Authentication required')
        else:
            issues.append('Unable to retrieve domain info')

    return {
        'success': checks['oauth_configured'],
        'checks': checks,
        'issues': issues
    }


def check_gam_config_directory() -> Dict:
    """Locate and check GAM configuration directory"""
    config_dir = None
    config_files = {
        'oauth2.txt': False,
        'oauth2service.json': False,
        'client_secrets.json': False,
        'gam.cfg': False
    }

    # Get GAM version output which shows config directory
    success, stdout, stderr = run_command(['gam', 'version'])
    if success:
        import re
        # Look for config file path in version output
        match = re.search(r'Config File: (.+?)(?:\n|$)', stdout)
        if match:
            config_file_path = match.group(1).strip()
            config_dir = str(Path(config_file_path).parent)

    # Try common config locations if not found
    if not config_dir:
        common_locations = [
            Path.home() / '.gam',
            Path.home() / 'GAM',
            Path.home() / 'GAMADV-XTD3',
        ]

        for location in common_locations:
            if location.exists():
                config_dir = str(location)
                break

    # Check for config files
    issues = []
    if config_dir and Path(config_dir).exists():
        for filename in config_files.keys():
            file_path = Path(config_dir) / filename
            config_files[filename] = file_path.exists()

        # Generate issues for missing files
        if not config_files['oauth2.txt']:
            issues.append('oauth2.txt missing - Run: gam oauth create')

        if not config_files['client_secrets.json'] and not config_files['oauth2service.json']:
            issues.append(
                'No service account credentials found. '
                'For automated operations, configure service account.'
            )
    else:
        issues.append('GAM config directory not found')

    return {
        'success': config_dir is not None,
        'config_dir': config_dir,
        'config_files': config_files,
        'issues': issues
    }


def check_network_connectivity() -> Dict:
    """Check network connectivity to Google APIs"""
    checks = {
        'internet_available': False,
        'google_apis_reachable': False,
        'admin_console_reachable': False
    }

    issues = []

    # Check basic internet connectivity
    success, _, _ = run_command(['ping', '-c', '1', 'google.com'], timeout=5)
    if not success:
        success, _, _ = run_command(['ping', '-n', '1', 'google.com'], timeout=5)

    checks['internet_available'] = success
    if not success:
        issues.append('No internet connectivity detected')

    # Check Google APIs endpoint
    try:
        import urllib.request
        urllib.request.urlopen('https://www.googleapis.com', timeout=5)
        checks['google_apis_reachable'] = True
    except:
        checks['google_apis_reachable'] = False
        issues.append('Cannot reach Google APIs - Check firewall/proxy')

    # Check Admin Console
    try:
        import urllib.request
        urllib.request.urlopen('https://admin.google.com', timeout=5)
        checks['admin_console_reachable'] = True
    except:
        checks['admin_console_reachable'] = False
        issues.append('Cannot reach Admin Console')

    return {
        'success': checks['internet_available'],
        'checks': checks,
        'issues': issues
    }


def check_api_access() -> Dict:
    """Test basic API access with simple GAM commands"""
    checks = {
        'can_list_users': False,
        'can_access_domain_info': False,
        'user_count': 0
    }

    issues = []

    # Try to get domain info
    success, stdout, stderr = run_command(['gam', 'info', 'domain'], timeout=15)
    checks['can_access_domain_info'] = success
    if not success:
        issues.append(f'Cannot access domain info: {stderr[:100]}')

    # Try to list users (just count)
    success, stdout, stderr = run_command(
        ['gam', 'print', 'users', 'maxresults', '1'],
        timeout=15
    )
    checks['can_list_users'] = success
    if success:
        lines = stdout.strip().split('\n')
        checks['user_count'] = len(lines) - 1  # Subtract header
    else:
        issues.append(f'Cannot list users: {stderr[:100]}')

    return {
        'success': checks['can_access_domain_info'] or checks['can_list_users'],
        'checks': checks,
        'issues': issues
    }


def run_full_diagnostic() -> Dict:
    """Run all diagnostic checks"""
    print("Running GAM diagnostics...")
    print()

    results = {}

    # 1. Installation check
    print("1/5 Checking GAM installation...")
    results['installation'] = check_gam_installation()
    print(f"   {'✓' if results['installation']['success'] else '✗'} GAM installation")
    print()

    if not results['installation']['success']:
        return {
            'success': False,
            'results': results,
            'overall_status': 'GAM not installed',
            'critical_issues': results['installation']['issues']
        }

    # 2. Configuration check
    print("2/5 Checking GAM configuration...")
    results['configuration'] = check_gam_config_directory()
    print(f"   {'✓' if results['configuration']['success'] else '✗'} Configuration directory")
    print()

    # 3. Authentication check
    print("3/5 Checking authentication...")
    results['authentication'] = check_gam_authentication()
    print(f"   {'✓' if results['authentication']['success'] else '✗'} OAuth authentication")
    print()

    # 4. Network check
    print("4/5 Checking network connectivity...")
    results['network'] = check_network_connectivity()
    print(f"   {'✓' if results['network']['success'] else '✗'} Network connectivity")
    print()

    # 5. API access check
    print("5/5 Checking API access...")
    results['api_access'] = check_api_access()
    print(f"   {'✓' if results['api_access']['success'] else '✗'} API access")
    print()

    # Determine overall status
    all_success = all(r['success'] for r in results.values())
    critical_issues = []

    for category, result in results.items():
        critical_issues.extend(result.get('issues', []))

    if all_success:
        overall_status = 'READY'
    elif results['authentication']['success']:
        overall_status = 'PARTIALLY_CONFIGURED'
    else:
        overall_status = 'NOT_CONFIGURED'

    return {
        'success': all_success,
        'results': results,
        'overall_status': overall_status,
        'critical_issues': critical_issues
    }


def format_diagnostic_report(diagnostic: Dict) -> str:
    """Format diagnostic results as human-readable report"""
    lines = [
        "=" * 70,
        "GAM DIAGNOSTIC REPORT",
        "=" * 70,
        f"Overall Status: {diagnostic['overall_status']}",
        ""
    ]

    # Show each category
    for category, result in diagnostic['results'].items():
        status = '✓ PASS' if result['success'] else '✗ FAIL'
        lines.append(f"{category.upper()}: {status}")

        if 'checks' in result:
            for check_name, check_value in result['checks'].items():
                if isinstance(check_value, bool):
                    symbol = '✓' if check_value else '✗'
                    lines.append(f"  {symbol} {check_name}")
                elif check_value is not None:
                    lines.append(f"  • {check_name}: {check_value}")

        if result.get('issues'):
            lines.append("  Issues:")
            for issue in result['issues']:
                lines.append(f"    - {issue}")

        lines.append("")

    # Summary
    if diagnostic['critical_issues']:
        lines.extend([
            "CRITICAL ISSUES TO RESOLVE:",
            ""
        ])
        for issue in diagnostic['critical_issues']:
            lines.append(f"  • {issue}")
        lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Command-line interface"""
    if len(sys.argv) > 1 and sys.argv[1] == '--json':
        # JSON output only
        diagnostic = run_full_diagnostic()
        print(json.dumps(diagnostic, indent=2))
    else:
        # Human-readable output
        diagnostic = run_full_diagnostic()
        print()
        print(format_diagnostic_report(diagnostic))

        if diagnostic['success']:
            print("✓ GAM is properly configured and ready to use!")
        else:
            print("✗ GAM configuration incomplete - resolve issues above")

        sys.exit(0 if diagnostic['success'] else 1)


if __name__ == '__main__':
    main()
