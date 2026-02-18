# GAM Troubleshooting Guide

Common errors, their causes, and solutions.

---

## Table of Contents
- [Installation & Configuration](#installation--configuration)
- [Authentication & Authorization](#authentication--authorization)
- [API Quotas & Rate Limits](#api-quotas--rate-limits)
- [Entity Errors](#entity-errors)
- [Command Syntax Errors](#command-syntax-errors)
- [Network & Connectivity](#network--connectivity)
- [CSV & File Errors](#csv--file-errors)
- [Drive Operations](#drive-operations)
- [Group Operations](#group-operations)

---

## Installation & Configuration

### Error: `command not found: gam`

**Cause:** GAM is not installed or not in system PATH.

**Solutions:**
```bash
# Check if GAM is installed
which gam  # macOS/Linux
where gam  # Windows

# If not found, install GAM7
# Visit: https://github.com/GAM-team/GAM/wiki/How-to-Install-GAM7

# If installed, add to PATH
export PATH=$PATH:/path/to/gam  # Add to ~/.bashrc or ~/.zshrc

# Or create alias
alias gam="/path/to/gam/gam"
```

---

### Error: `oauth2.txt not found`

**Cause:** GAM has not been authenticated yet.

**Solutions:**
```bash
# Create OAuth authentication
gam oauth create

# Follow browser prompts to authenticate
# Make sure to authenticate with a Google Workspace super admin account

# Verify authentication
gam oauth info

# Check config directory
gam version  # Shows config file location
```

---

### Error: `client_secrets.json not found`

**Cause:** API project credentials missing.

**Solutions:**
```bash
# Check GAM config directory
gam version

# If missing, you need to:
# 1. Create a GCP project
# 2. Enable required APIs
# 3. Create OAuth credentials
# 4. Download client_secrets.json
# 5. Place in GAM config directory

# Full guide:
# https://github.com/GAM-team/GAM/wiki/How-to-Install-GAM7
```

---

## Authentication & Authorization

### Error: `Error 403: Forbidden` or `Access denied`

**Cause:** Insufficient permissions or missing API scopes.

**Solutions:**
```bash
# Re-authorize with all scopes
gam oauth create

# Check current authorization
gam oauth info

# Verify admin privileges in Admin Console
# Must be Super Admin or have necessary delegated admin privileges

# For service account errors, check domain-wide delegation:
# Admin Console > Security > API controls > Domain-wide delegation
```

---

### Error: `insufficient permission for this task` or `does not have required scope`

**Cause:** GAM needs additional API scopes for this operation.

**Solutions:**
```bash
# Re-create OAuth with all scopes
gam oauth create

# During authorization, grant ALL requested permissions

# For specific scope issues, authorize that scope:
gam oauth create scope https://www.googleapis.com/auth/admin.directory.user

# Common scopes needed:
# - admin.directory.user (user management)
# - admin.directory.group (group management)
# - apps.groups.settings (group settings)
# - drive (Drive operations)
# - gmail.settings.basic (Gmail settings)
# - calendar (Calendar operations)

# Verify scopes
gam oauth info
```

---

### Error: `Invalid authorization` or `Token has been expired or revoked`

**Cause:** OAuth token expired or was revoked.

**Solutions:**
```bash
# Re-authenticate
gam oauth create

# For service accounts, check:
# 1. Service account key file (client_secrets.json) is valid
# 2. Domain-wide delegation is properly configured
# 3. Service account hasn't been deleted/disabled in GCP
```

---

## API Quotas & Rate Limits

### Error: `429: Too many requests` or `Quota exceeded` or `Rate limit`

**Cause:** Exceeded Google API rate limits.

**Solutions:**
```bash
# Wait a few minutes and retry
sleep 120 && gam <command>

# Use batch_size to throttle requests
gam config batch_size 50 csvfile users.csv gam user ~email ...

# Use wait_on_fail to auto-retry
gam config wait_on_fail csvfile users.csv gam user ~email ...

# Split operations across time
python3 scripts/batch_planner.py split users.csv batch_ 100
# Process one batch per hour

# Check quota usage in Google Cloud Console
# APIs & Services > Dashboard

# Request quota increase if needed (in GCP Console)
```

---

### Error: `Backend error` or `500 Internal Server Error`

**Cause:** Temporary Google API issue or rate limiting.

**Solutions:**
```bash
# Wait and retry (usually resolves in seconds/minutes)
sleep 30 && gam <command>

# Use wait_on_fail for automatic retry
gam config wait_on_fail <command>

# If persists, check Google Workspace Status Dashboard
# https://www.google.com/appsstatus
```

---

## Entity Errors

### Error: `404: Not found` or `Entity does not exist`

**Cause:** User, group, or resource doesn't exist.

**Solutions:**
```bash
# Verify entity exists
gam info user john@example.com
gam info group team@example.com

# Check spelling (case-sensitive for some operations)
# Verify domain is correct

# For recently deleted entities, check deleted users
gam print users deleted

# Restore if within 20 days
gam undelete user john@example.com
```

---

### Error: `Resource not found` (Drive files)

**Cause:** File ID is incorrect or user doesn't have access.

**Solutions:**
```bash
# Verify file ID from URL
# https://drive.google.com/file/d/<FILE_ID>/view

# Check if user has access to file
gam user owner@example.com show filelist id <fileID>

# If file is in Shared Drive, specify that
gam user admin@example.com show filelist <sharedDriveID>
```

---

### Error: `409: Conflict` or `Already exists` or `Duplicate`

**Cause:** Trying to create entity that already exists.

**Solutions:**
```bash
# Check if entity exists first
gam info user john@example.com

# Use update instead of create
gam update user john@example.com ...

# For bulk operations, skip duplicates
gam csvfile users.csv gam create user ~email ... continue_on_error
```

---

### Error: `Member not found` or `is not a member`

**Cause:** User is not a member of the specified group.

**Solutions:**
```bash
# Check current membership
gam info group team@example.com members
gam print group-members group team@example.com

# Add member first before trying to remove/update
gam update group team@example.com add member user@example.com

# Verify email address is correct
```

---

## Command Syntax Errors

### Error: `400: Bad request` or `Invalid value` or `Malformed`

**Cause:** Command syntax or parameter values are incorrect.

**Solutions:**
```bash
# Check GAM wiki for correct syntax
# https://github.com/GAM-team/GAM/wiki

# Common issues:
# - Missing quotes around values with spaces
gam update user john@example.com ou "/Sales Team"  # Correct
gam update user john@example.com ou /Sales Team   # Wrong

# - Wrong parameter names (check wiki)
# - Missing required parameters

# Validate command before running
python3 scripts/gam_helper.py validate "<command>"

# Test with a single entity first
```

---

### Error: `InvalidValue: orgUnitPath`

**Cause:** Organizational unit path is invalid.

**Solutions:**
```bash
# OU paths must:
# - Start with forward slash: /
# - Use correct case (case-sensitive)
# - Match exact hierarchy: /Parent/Child

# List all OUs to find correct path
gam print ous

# Correct examples:
gam update user john@example.com ou "/"              # Root
gam update user john@example.com ou "/Sales"         # Top-level OU
gam update user john@example.com ou "/Sales/West"    # Nested OU

# Wrong examples:
gam update user john@example.com ou "Sales"          # Missing /
gam update user john@example.com ou "/sales"         # Wrong case
```

---

### Error: `Unbalanced quotes` or `Unexpected token`

**Cause:** Quote mismatch in command.

**Solutions:**
```bash
# Check for balanced quotes
# Every opening quote needs closing quote

# Use matching quote types
gam user john@example.com signature "Hello 'World'"  # Correct
gam user john@example.com signature "Hello "World""  # Wrong

# Escape quotes if needed (shell-dependent)
gam user john@example.com signature "Hello \"World\""
```

---

## Network & Connectivity

### Error: `Name or service not known` or `Connection refused` or `Failed to establish connection`

**Cause:** Network connectivity issues.

**Solutions:**
```bash
# Check internet connection
ping google.com

# Check DNS resolution
nslookup admin.google.com

# Check firewall/proxy settings
# Ensure access to:
# - googleapis.com
# - google.com
# - accounts.google.com

# If behind corporate proxy, configure:
export http_proxy=http://proxy:port
export https_proxy=http://proxy:port

# Or in gam.cfg:
# http_proxy = http://proxy:port
```

---

### Error: `SSL: CERTIFICATE_VERIFY_FAILED` or `Certificate error`

**Cause:** SSL certificate validation issues.

**Solutions:**
```bash
# Check system date/time (must be accurate)
date

# Update SSL certificates (OS-specific)
# macOS: Install certificates from Python
/Applications/Python*/Install\ Certificates.command

# Linux: Update ca-certificates
sudo apt-get update && sudo apt-get install ca-certificates

# Temporary workaround (NOT for production):
gam config no_verify_ssl true

# Check corporate firewall isn't intercepting SSL
```

---

## CSV & File Errors

### Error: `No such file or directory` (CSV file)

**Cause:** CSV file path is incorrect or file doesn't exist.

**Solutions:**
```bash
# Verify file exists
ls -la users.csv

# Use absolute path
gam csvfile /full/path/to/users.csv ...

# Check current directory
pwd

# Verify file permissions
chmod 644 users.csv
```

---

### Error: `CSV file has no header` or `Column not found`

**Cause:** CSV file formatting issue.

**Solutions:**
```bash
# Validate CSV structure
python3 scripts/csv_generator.py validate users.csv 'email'

# Preview CSV
head -5 users.csv

# Ensure:
# - First row is header with column names
# - Column names match ~variable in command
# - No empty header columns
# - Proper CSV formatting (commas, quotes)

# Example correct CSV:
# email,firstname,lastname
# john@example.com,John,Smith
```

---

### Error: `Required column missing` in CSV operations

**Cause:** CSV doesn't have expected column.

**Solutions:**
```bash
# Check CSV header
head -1 users.csv

# Column name in CSV must match ~variable in command
# CSV header: email,name
# Command must use: ~email and ~name

# Validate before running
python3 scripts/csv_generator.py validate users.csv 'email,name'
```

---

## Drive Operations

### Error: `Insufficient permission` (Drive)

**Cause:** User doesn't own file or lack necessary permissions.

**Solutions:**
```bash
# Check file ownership
gam user admin@example.com show filelist id <fileID>

# For Shared Drives, ensure user has Organizer role
gam show drivefileacl <sharedDriveID>

# Use owner's account for operations
gam user owner@example.com add drivefileacl <fileID> ...

# For domain-wide operations, use service account with delegation
```

---

### Error: `File not found` but file exists in Drive

**Cause:** File might be in trash or user doesn't have access.

**Solutions:**
```bash
# Check if file is trashed
gam user owner@example.com show filelist query "trashed=true" id <fileID>

# Restore from trash
gam user owner@example.com restore drivefile <fileID>

# Check file permissions
gam user owner@example.com show drivefileacl <fileID>
```

---

## Group Operations

### Error: `Cyclic memberships not allowed`

**Cause:** Trying to add a group to another group that would create a circular dependency.

**Solutions:**
```bash
# Cannot add Group A to Group B if B is already in A
# Check current membership
gam info group groupA@example.com members
gam info group groupB@example.com members

# Remove the reverse membership first
gam update group groupA@example.com remove member groupB@example.com

# Then add the desired membership
gam update group groupB@example.com add member groupA@example.com
```

---

### Error: `Group settings not found`

**Cause:** Trying to access group settings for a group that doesn't exist or isn't a Google Group.

**Solutions:**
```bash
# Verify group exists
gam info group team@example.com

# Check group type (must be Google Group, not Cloud Identity Group)
gam info group team@example.com

# For Cloud Identity Groups, use different commands
gam info cigroup team@example.com
```

---

## Diagnostic Tools

Use the error analyzer script:

```bash
# Analyze specific error
python3 scripts/error_analyzer.py analyze "Error: oauth2.txt not found"

# Analyze log file for error patterns
python3 scripts/error_analyzer.py logfile gam.log

# Get debug commands for error category
python3 scripts/error_analyzer.py debug authentication
```

Check environment health:

```bash
# Full diagnostic
python3 scripts/config_checker.py

# JSON output
python3 scripts/config_checker.py --json
```

---

## General Debugging Steps

1. **Enable debug mode**
   ```bash
   gam config debug_level info <command>
   ```

2. **Check GAM version**
   ```bash
   gam version
   # Ensure you're on latest version
   ```

3. **Verify configuration**
   ```bash
   gam info domain
   gam oauth info
   ```

4. **Test with simple command**
   ```bash
   gam info domain
   # If this works, GAM is configured correctly
   ```

5. **Check Google Workspace Status**
   - Visit: https://www.google.com/appsstatus
   - Verify no ongoing issues

6. **Review full error message**
   - Don't just look at first line
   - Full error context often reveals cause

7. **Search GAM issues**
   - GitHub: https://github.com/GAM-team/GAM/issues
   - Google Group: https://groups.google.com/g/google-apps-manager

---

## Getting Help

When asking for help, provide:

1. **GAM version:** `gam version`
2. **Full command** (redact sensitive info)
3. **Complete error message**
4. **What you've tried already**
5. **Expected vs actual behavior**

**Resources:**
- GAM Wiki: https://github.com/GAM-team/GAM/wiki
- GAM Issues: https://github.com/GAM-team/GAM/issues
- GAM Google Group: https://groups.google.com/g/google-apps-manager
- GAM Chat Room: https://github.com/GAM-team/GAM/wiki/GAM-Public-Chat-Room
