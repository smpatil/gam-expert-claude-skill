---
name: gam-expert
description: |
  Expert at executing GAM (Google Apps Manager) commands for Google Workspace administration.
  Use this skill when the user needs to manage Google Workspace users, groups, calendars, drive files,
  organizational units, or other Google Workspace resources. The skill reads GAM documentation,
  constructs proper commands, processes spreadsheets with Python when needed, and always confirms
  before executing major operations. Assumes GAM7 is already installed and configured.
---

# GAM Expert

## Quick start
- When asked to manage Google Workspace resources (users, groups, drive, calendars, etc.), load this skill.
- Read relevant GAM wiki documentation from the `GAM.wiki/` folder to understand command syntax.
- Construct proper GAM commands based on documentation and user requirements.
- Use Python for spreadsheet processing when CSV/Excel files are involved.
- Always confirm with the user before executing commands that modify, delete, or affect multiple resources.

## Instructions

### 1. Understand the user's request
- Identify what Google Workspace resource(s) need to be managed (users, groups, drive files, etc.)
- Determine the operation type: create, update, delete, read/print, bulk operation
- Check if spreadsheets or CSV files are involved

### 2. Read relevant GAM documentation
Use the progressive documentation approach:

**First: Check `references/` folder** (always available):
- `quick_reference.md` - Top 50 most common commands
- `command_syntax.md` - Detailed command patterns
- `common_patterns.md` - Frequently used templates
- `safety_checklist.md` - Safety guidelines
- `troubleshooting.md` - Common errors and solutions

**Second: Fetch GAM wiki pages online** (when needed for advanced/specific commands):
Use WebFetch to get the latest documentation from GitHub:
```
https://raw.githubusercontent.com/GAM-team/GAM/wiki/[PageName].md
```

Key GAM wiki pages:
- `Collections-of-Users.md` - User selection patterns
- `Groups.md` - Group management
- `Groups-Membership.md` - Group membership operations
- `Drive-Items.md` - Drive file operations
- `Calendars.md` - Calendar management
- `Organizational-Units.md` - OU management
- `Bulk-Processing.md` - Batch operations
- `CSV-Input-Filtering.md` - Working with CSV input
- `CSV-Output-Filtering.md` - Formatting CSV output

**Third: Local GAM.wiki folder** (optional, if user has cloned it):
- Check if `GAM.wiki/` folder exists in parent directories
- If available, read directly for offline comprehensive access

**Strategy**: Start with references/ for common operations. Fetch wiki pages online for specific/advanced needs. This keeps the skill lightweight while ensuring access to complete documentation.

### 3. Construct GAM commands
Based on the documentation:
- Build the correct GAM command syntax
- Handle complex entity selections (users, groups, OUs)
- Apply proper filters and options
- Consider CSV input/output when working with multiple items

### 4. Process spreadsheets and validate commands
When the user provides CSV or Excel files or constructs GAM commands:
- Use Python helper scripts for common operations
- Validate command syntax and analyze safety
- Process CSV/Excel data for bulk operations
- Generate preview commands and safety warnings

**Available helper scripts**:
- `scripts/gam_helper.py` - Command validation, safety analysis, entity extraction
- `scripts/spreadsheet_processor.py` - CSV/Excel reading and processing
- `scripts/batch_planner.py` - Planning and organizing bulk operations
- `scripts/csv_generator.py` - Generating GAM-compatible CSV files
- `scripts/error_analyzer.py` - Analyzing and troubleshooting GAM errors
- `scripts/config_checker.py` - Verifying GAM installation and configuration

**Reference documentation in `references/` folder**:
- `command_syntax.md` - Detailed GAM command syntax patterns
- `common_patterns.md` - Frequently used command patterns
- `quick_reference.md` - Top 50 most common commands
- `safety_checklist.md` - Safety guidelines and confirmation requirements
- `troubleshooting.md` - Common errors and solutions
- `api_scopes.md` - Required Google API scopes

### 5. Analyze command safety
Before executing any command:
- Use `scripts/gam_helper.py` to analyze the command for safety concerns
- Check risk level (LOW, MEDIUM, HIGH, CRITICAL)
- Review warnings about destructive operations, bulk changes, or large-scale impacts
- Generate preview/dry-run commands when available

### 6. Confirm before executing
**CRITICAL**: Before running any GAM command that:
- Modifies or deletes resources
- Affects multiple users/groups
- Changes permissions or settings
- Performs bulk operations

**Always**:
1. Show the exact command(s) you plan to run
2. Explain what the command will do
3. Ask for explicit user confirmation
4. Wait for user approval before executing

For read-only operations (print, info, show commands), you may execute without confirmation unless the user requests otherwise.

### 7. Execute and report results
- Run the GAM command using bash
- Capture and parse the output
- Report success/failure clearly
- If errors occur, consult documentation and suggest fixes
- For CSV output, offer to analyze or visualize results

## Inputs

### Required
- User's goal or task description (e.g., "add users to group", "list all users in OU")
- `references/` folder with curated GAM documentation (included in skill)
- Internet access for fetching GAM wiki pages online (via WebFetch)

### Optional
- CSV or Excel files for bulk operations
- Specific email addresses, group names, or resource identifiers
- Filter criteria (domains, queries, patterns)
- Output format preferences
- Local GAM.wiki clone for offline comprehensive documentation access

## Outputs

### Command outputs
- GAM command syntax constructed and executed
- Terminal output from GAM commands
- Success/failure status

### Data outputs
- CSV files generated from GAM output
- Processed spreadsheets with analysis or transformations
- Summary reports of operations performed

## Constraints

- **GAM must be pre-installed**: Assumes `gam` command is available in PATH
- **Network access required**: GAM operations require internet connectivity to Google APIs; fetching wiki pages also requires internet
- **Authentication required**: Assumes GAM is already authenticated (oauth2.txt exists)
- **Destructive operations**: Always confirm before modifying/deleting resources
- **Python environment**: Standard libraries sufficient; pandas and openpyxl optional for advanced spreadsheet operations
- **Documentation access**: references/ folder always available; GAM wiki pages fetched online as needed

## Error handling

### Common errors and solutions

1. **Command not found: gam**
   - Verify GAM installation: `which gam` or `gam version`
   - Check PATH configuration
   - Ask user for GAM installation location

2. **Authentication errors**
   - Check if oauth2.txt exists: `ls ~/.gam/oauth2.txt` or similar
   - Suggest running: `gam oauth create`
   - Verify service account authorization

3. **Syntax errors**
   - Re-read relevant GAM wiki documentation
   - Check for typos in entity names or options
   - Verify quote handling for names with spaces

4. **Permission errors**
   - Verify GAM has necessary API scopes
   - Check admin privileges for the operation
   - Suggest re-authorizing with required scopes

5. **API quota exceeded**
   - Suggest batch_size parameter to throttle requests
   - Wait and retry
   - Use `gam info user` to check API quotas

**Recovery strategy**: For any failure:
1. Show the exact error message
2. Identify the likely cause based on error
3. Consult relevant documentation section
4. Suggest corrective action
5. Offer to retry with corrected command

## Examples

### Example 1: List all users in an organizational unit
**User request**: "Show me all users in the /Marketing/Sales OU"

**Process**:
1. Read `Collections-of-Users.md` and `Organizational-Units.md`
2. Construct command: `gam print users ou "/Marketing/Sales"`
3. Execute (read-only, no confirmation needed)
4. Parse and present results

### Example 2: Add multiple users to a group from CSV
**User request**: "Add the users in users.csv to the marketing@example.com group"

**Process**:
1. Read `Groups-Membership.md` and `CSV-Input-Filtering.md`
2. Use Python to validate users.csv format:
   ```python
   import pandas as pd
   df = pd.read_csv('users.csv')
   print(df.head())
   ```
3. Construct command: `gam update group marketing@example.com add members csvfile users.csv:Email`
4. **Show command and ask for confirmation**: "This will add N users to marketing@example.com. Proceed?"
5. Wait for approval
6. Execute and report results

### Example 3: Create a new group with specific settings
**User request**: "Create a new group called team@example.com that only members can post to"

**Process**:
1. Read `Groups.md` for group creation and settings
2. Construct command:
   ```
   gam create group team@example.com name "Team Group" whoCanPostMessage ALL_MEMBERS_CAN_POST whoCanJoin CAN_REQUEST_TO_JOIN
   ```
3. **Show command and ask for confirmation**: "This will create a new group with these settings: ..."
4. Execute after approval

### Example 4: Export Drive file permissions to spreadsheet
**User request**: "I need a report of who has access to files in the Shared Drive"

**Process**:
1. Read `Drive-Items.md` and `Shared-Drives.md`
2. Construct command: `gam user admin@example.com print drivefileacls <SharedDriveID> > permissions.csv`
3. Execute (read-only)
4. Use Python to analyze and format results:
   ```python
   import pandas as pd
   df = pd.read_csv('permissions.csv')
   summary = df.groupby(['emailAddress', 'role']).size()
   print(summary)
   ```
5. Present formatted results

### Example 5: Bulk user suspension with safety check
**User request**: "Suspend all users in the terminated.csv file"

**Process**:
1. Read `Collections-of-Users.md` for csvfile syntax
2. Use Python to preview the file:
   ```python
   import pandas as pd
   df = pd.read_csv('terminated.csv')
   print(f"Found {len(df)} users to suspend:")
   print(df['email'].tolist()[:10])  # Show first 10
   ```
3. **CRITICAL CONFIRMATION**: "⚠️  This will SUSPEND {count} user accounts. This is a major operation. Please review the list and type 'CONFIRM' to proceed."
4. Wait for explicit "CONFIRM" response
5. Execute: `gam csvfile terminated.csv:email update user ~email suspended on`
6. Report results and any errors

## Reference

### Documentation strategy

**1. references/ folder (Primary - Always Available)**
Curated quick-reference documentation included in the skill:
- `command_syntax.md` - Detailed command patterns
- `common_patterns.md` - Frequently used commands
- `quick_reference.md` - Top 50 commands
- `safety_checklist.md` - Safety guidelines
- `troubleshooting.md` - Common errors & solutions
- `api_scopes.md` - Required API scopes

Read these first - they cover 80% of common GAM operations.

**2. GAM.wiki online (Secondary - Fetch As Needed)**
Fetch specific pages from GitHub when needed for advanced operations:
```
https://raw.githubusercontent.com/GAM-team/GAM/wiki/[PageName].md
```

Available pages (100+ total):
- **User management**: Collections-of-Users.md, user commands
- **Groups**: Groups.md, Groups-Membership.md, Cloud-Identity-Groups.md
- **Drive**: Drive-Items.md, Drive-File-Selection.md, Shared-Drives.md
- **Calendar**: Calendars.md, Calendars-Events.md, Calendars-Access.md
- **Chrome/ChromeOS**: ChromeOS-Devices.md, Chrome-Policies.md
- **Classroom**: Classroom-Courses.md, Classroom-Membership.md
- **Organization**: Organizational-Units.md, Administrators.md
- **Data formats**: CSV-Input-Filtering.md, CSV-Output-Filtering.md
- **Advanced**: Bulk-Processing.md, Command-Data-From-Google-Docs-Sheets-Storage.md

Use WebFetch to get the latest documentation directly from the GAM repository.

**3. Local GAM.wiki clone (Optional - For Offline Access)**
Users can optionally clone the wiki for comprehensive offline access:
```bash
git clone https://github.com/GAM-team/GAM.wiki.git
```
If present in parent directories, can be read directly.

### Helper scripts usage
All helper scripts in `scripts/` folder are executable Python files that can be:
- Called directly for standalone operations
- Imported as modules for reusable functions
- Referenced in SKILL.md for Claude to use as needed

Run any script with `--help` or no arguments to see usage information.

Example usage:
```bash
# Analyze command safety before executing
python3 scripts/gam_helper.py analyze "gam update group sales@example.com add member user@example.com"

# Validate CSV file structure
python3 scripts/spreadsheet_processor.py validate users.csv email,firstname,lastname

# Check GAM configuration
python3 scripts/config_checker.py
```

### Safety guidelines
1. **Confirm destructive operations**: Delete, suspend, modify permissions
2. **Confirm bulk operations**: Anything affecting >5 resources
3. **Validate input data**: Check CSV files before using in commands
4. **Dry run when possible**: Use `gam print` to preview before executing
5. **Backup critical data**: Suggest backing up before major changes
6. **Test with small sample**: For bulk operations, test with 1-2 items first

### Command patterns
Common GAM command structure:
```
gam <entity-selection> <command> <resource> <options>

Examples:
gam user bob@example.com show info
gam group sales@example.com add member alice@example.com
gam print users query "orgUnitPath='/Sales'"
gam all users delete messages query "in:trash older_than:30d"
gam csvfile users.csv:email gam user ~email update ou "/Marketing"
```

## Notes

- This skill requires GAM7 (not legacy GAM) for full feature support
- Always consult the latest documentation as GAM is actively maintained
- Be especially careful with delete operations - they are often irreversible
- Use `gam print` commands to preview data before modifying
- CSV files can reference Google Sheets using gdoc: syntax
- Regular expressions can be used for pattern matching in many commands
- The skill can read any file in the GAM.wiki folder - reference specific docs as needed
