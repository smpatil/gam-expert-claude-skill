# GAM Expert Skill

A Claude Code skill that provides expert-level assistance with GAM (Google Apps Manager) commands for Google Workspace administration.

## What is GAM?

GAM7 is a free, open-source command-line tool for Google Workspace administrators to manage domain and user settings. It provides powerful automation capabilities for:

- User management (create, update, suspend, delete)
- Group management and membership
- Google Drive files and permissions
- Calendar sharing and events
- Organizational Units
- Chrome/ChromeOS device management
- Classroom courses and membership
- And much more...

## What This Skill Does

The GAM Expert skill helps you:

1. **Construct proper GAM commands** by reading the comprehensive GAM wiki documentation
2. **Process spreadsheets** with Python when bulk operations require CSV/Excel files
3. **Execute commands safely** by always confirming before destructive operations
4. **Troubleshoot errors** by consulting documentation and suggesting fixes
5. **Analyze results** by parsing GAM output and generating reports

## Prerequisites

- **GAM7 must be installed and configured** on your system
- Verify with: `gam version`
- GAM must be authenticated with your Google Workspace domain
- Python 3 for spreadsheet processing (optional but recommended)

## Installation

This skill should be placed in your Claude Code skills directory:

```bash
# Copy the gam-expert folder to your Claude Code skills directory
cp -r gam-expert ~/.claude/skills/
```

Or if using the Agent SDK, place it in your `.claude/skills/` directory.

## How to Use

Simply describe what you want to do with Google Workspace in natural language:

### Examples

**User Management:**
- "List all users in the Marketing OU"
- "Create a new user account for john@example.com"
- "Suspend the users listed in terminated.csv"

**Group Management:**
- "Create a new group called team@example.com"
- "Add all users from users.csv to the sales@example.com group"
- "Show me all members of the executive@example.com group"

**Drive Management:**
- "List all files owned by alice@example.com"
- "Generate a report of who has access to the Shared Drive"
- "Transfer ownership of all files from old.user@example.com to new.user@example.com"

**Bulk Operations:**
- "Update all users in the CSV file with their new OUs"
- "Create groups from the list in groups.csv with the specified settings"
- "Export all group memberships to a spreadsheet for audit"

## Safety Features

The skill includes multiple safety mechanisms:

1. **Confirmation prompts** for all destructive operations
2. **Preview mode** - uses `gam print` commands to show what will happen
3. **Data validation** - checks CSV files before using them
4. **Documentation-first approach** - always reads GAM docs before executing
5. **Error recovery** - suggests fixes when commands fail

## Skill Components

### SKILL.md
Main skill instructions with:
- Comprehensive workflow for GAM operations
- Documentation references
- Safety guidelines
- Example use cases

### scripts/spreadsheet_processor.py
Python helper for:
- Reading and validating CSV files
- Transforming data for GAM
- Analyzing GAM output
- Merging multiple CSV files

### GAM.wiki/
Complete GAM documentation (provided by user):
- 100+ documentation files
- Detailed command syntax
- Examples and use cases
- Best practices

## Common Workflows

### 1. Simple read operation
User asks → Skill reads docs → Constructs command → Executes → Reports results

### 2. Bulk operation with CSV
User provides CSV → Skill validates file → Constructs command → **Confirms with user** → Executes → Reports results

### 3. Complex multi-step operation
User describes goal → Skill breaks into steps → **Confirms plan** → Executes each step → **Confirms before destructive steps** → Reports results

## Documentation Structure

The skill has access to comprehensive GAM documentation organized by topic:

- **Users**: Collections-of-Users.md, user commands
- **Groups**: Groups.md, Groups-Membership.md
- **Drive**: Drive-Items.md, Shared-Drives.md
- **Calendar**: Calendars.md, Calendars-Events.md
- **Organization**: Organizational-Units.md, Administrators.md
- **Bulk operations**: Bulk-Processing.md, CSV processing

The skill automatically reads the relevant documentation for each request.

## Troubleshooting

### "Command not found: gam"
- Ensure GAM7 is installed: https://github.com/GAM-team/GAM
- Check your PATH includes the GAM directory
- Try providing full path to gam executable

### Authentication errors
- Run `gam oauth create` to re-authenticate
- Check that oauth2.txt exists in your GAM config directory
- Verify service account is properly authorized

### Permission errors
- Ensure you have admin privileges for the operation
- Check API scopes are properly configured
- May need to re-run `gam oauth create` with additional scopes

## Tips for Best Results

1. **Be specific** - Include email addresses, group names, OU paths
2. **Provide context** - Mention if you're working with a CSV file
3. **Ask questions** - The skill will explain what commands do
4. **Review before confirming** - Always check the command before approving
5. **Start small** - Test with 1-2 items before bulk operations

## Links

- GAM GitHub: https://github.com/GAM-team/GAM
- GAM Wiki: https://github.com/GAM-team/GAM/wiki
- Google Groups Discussion: https://groups.google.com/group/google-apps-manager

## License

This skill is provided as-is for use with Claude Code. GAM itself is maintained by Jay Lee and Ross Scroggs.
