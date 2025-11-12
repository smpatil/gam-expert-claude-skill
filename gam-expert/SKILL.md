---
name: gam-expert
description: |
  Expert at executing GAM (Google Apps Manager) commands for Google Workspace administration.
  Use this skill when the user needs to manage Google Workspace users, groups, calendars, drive files,
  organizational units, or other Google Workspace resources. The skill reads GAM documentation,
  constructs proper commands, processes CSV files when needed, and always confirms
  before executing major operations. Assumes GAM7 is already installed and configured.
---

# GAM Expert

## Quick start
- When asked to manage Google Workspace resources (users, groups, drive, calendars, etc.), load this skill.
- Read relevant GAM documentation to understand command syntax.
- Construct proper GAM commands based on documentation and user requirements.
- Use the Read tool to analyze CSV files when bulk operations are involved.
- Always confirm with the user before executing commands that modify, delete, or affect multiple resources.

## Instructions

### 1. Understand the user's request
- Identify what Google Workspace resource(s) need to be managed (users, groups, drive files, etc.)
- Determine the operation type: create, update, delete, read/print, bulk operation
- Check if spreadsheets or CSV files are involved

### 2. Read relevant GAM documentation
Use the progressive documentation approach:

**First: Check `references/` folder** (quick reference for common operations):
- `quick_reference.md` - Top 50 most common commands
- `command_syntax.md` - Detailed command patterns
- `common_patterns.md` - Frequently used templates
- `safety_checklist.md` - Safety guidelines
- `troubleshooting.md` - Common errors and solutions

**Second: Read from bundled `wiki/` folder** (complete GAM documentation, 165 pages):
The complete GAM wiki is bundled with this skill for offline access. Read specific pages as needed:
```
wiki/[PageName].md
```

Key GAM wiki pages:
- `wiki/Collections-of-Users.md` - User selection patterns
- `wiki/Groups.md` - Group management
- `wiki/Groups-Membership.md` - Group membership operations
- `wiki/Drive-Items.md` - Drive file operations
- `wiki/Calendars.md` - Calendar management
- `wiki/Organizational-Units.md` - OU management
- `wiki/Bulk-Processing.md` - Batch operations
- `wiki/CSV-Input-Filtering.md` - Working with CSV input
- `wiki/CSV-Output-Filtering.md` - Formatting CSV output

**Strategy**: Start with references/ for common operations. Read specific wiki pages for advanced/detailed documentation. All documentation is available offline with progressive disclosure - Claude only loads files when contextually relevant.

### 3. Construct GAM commands
Based on the documentation:
- Build the correct GAM command syntax
- Handle complex entity selections (users, groups, OUs)
- Apply proper filters and options
- Consider CSV input/output when working with multiple items

### 4. Validate commands and process CSV files
When the user provides CSV files or constructs GAM commands:
- Analyze command syntax and safety implications
- Use the Read tool to preview and validate CSV data
- Generate preview commands when appropriate
- Provide safety warnings for destructive operations

**Reference documentation in `references/` folder**:
- `command_syntax.md` - Detailed GAM command syntax patterns
- `common_patterns.md` - Frequently used command patterns
- `quick_reference.md` - Top 50 most common commands
- `safety_checklist.md` - Safety guidelines and confirmation requirements
- `troubleshooting.md` - Common errors and solutions
- `api_scopes.md` - Required Google API scopes

### 5. Analyze command safety
Before executing any command:
- Analyze the command for safety concerns using reasoning
- Assess risk level (LOW, MEDIUM, HIGH, CRITICAL)
- Identify destructive operations, bulk changes, or large-scale impacts
- Generate preview/dry-run commands when available (e.g., using `gam print`)

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
- `references/` folder with curated GAM quick reference (included in skill)
- `wiki/` folder with complete GAM documentation (165 pages, bundled in skill)

### Optional
- CSV or Excel files for bulk operations
- Specific email addresses, group names, or resource identifiers
- Filter criteria (domains, queries, patterns)
- Output format preferences

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
- **Network access required**: GAM operations require internet connectivity to Google APIs
- **Authentication required**: Assumes GAM is already authenticated (oauth2.txt exists)
- **Destructive operations**: Always confirm before modifying/deleting resources
- **Documentation access**: Complete documentation (references/ + wiki/) bundled for offline access

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
2. Use Read tool to preview users.csv and validate it has an Email column
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
4. Use Read tool to analyze the CSV and provide a summary of access patterns
5. Present formatted results

### Example 5: Bulk user suspension with safety check
**User request**: "Suspend all users in the terminated.csv file"

**Process**:
1. Read `Collections-of-Users.md` for csvfile syntax
2. Use Read tool to preview terminated.csv and count the users
3. **CRITICAL CONFIRMATION**: "⚠️  This will SUSPEND {count} user accounts. This is a major operation. Please review the list and type 'CONFIRM' to proceed."
4. Wait for explicit "CONFIRM" response
5. Execute: `gam csvfile terminated.csv:email update user ~email suspended on`
6. Report results and any errors

## Reference

### Documentation strategy

**1. references/ folder (Quick Reference)**
Curated quick-reference documentation for common operations:
- `command_syntax.md` - Detailed command patterns
- `common_patterns.md` - Frequently used commands
- `quick_reference.md` - Top 50 commands
- `safety_checklist.md` - Safety guidelines
- `troubleshooting.md` - Common errors & solutions
- `api_scopes.md` - Required API scopes

Read these first - they cover 80% of common GAM operations.

**2. wiki/ folder (Complete Documentation - Bundled)**
The complete GAM wiki (165 pages, 4MB) is bundled with this skill for fast, offline access:
```
wiki/[PageName].md
```

Available pages cover all GAM functionality:
- **User management**: Collections-of-Users.md, user commands
- **Groups**: Groups.md, Groups-Membership.md, Cloud-Identity-Groups.md
- **Drive**: Drive-Items.md, Drive-File-Selection.md, Shared-Drives.md
- **Calendar**: Calendars.md, Calendars-Events.md, Calendars-Access.md
- **Chrome/ChromeOS**: ChromeOS-Devices.md, Chrome-Policies.md
- **Classroom**: Classroom-Courses.md, Classroom-Membership.md
- **Organization**: Organizational-Units.md, Administrators.md
- **Data formats**: CSV-Input-Filtering.md, CSV-Output-Filtering.md
- **Advanced**: Bulk-Processing.md, Command-Data-From-Google-Docs-Sheets-Storage.md

Claude uses progressive disclosure - files are only loaded when contextually relevant, so comprehensive documentation doesn't impact performance.

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
- Complete GAM wiki (165 pages) is bundled for offline access with progressive disclosure
- Be especially careful with delete operations - they are often irreversible
- Use `gam print` commands to preview data before modifying
- CSV files can reference Google Sheets using gdoc: syntax
- Regular expressions can be used for pattern matching in many commands
- The skill can read any file in the wiki/ folder - reference specific docs as needed
