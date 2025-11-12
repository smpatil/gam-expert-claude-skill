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

## When to Use This Skill

Use this skill when the user needs to:
- Manage Google Workspace users, groups, calendars, drive files, or organizational units
- Execute bulk operations from CSV files
- Generate reports or exports from Google Workspace
- Troubleshoot GAM commands or understand GAM syntax

This skill assumes GAM7 is already installed and authenticated on the user's system.

## Workflow

### 1. Understand the Request
Identify:
- What Google Workspace resource(s) need management (users, groups, drive, calendars, etc.)
- Operation type: create, update, delete, read/print, bulk operation
- Whether CSV files or spreadsheets are involved
- Urgency and risk level of the operation

### 2. Read Relevant Documentation

Use progressive documentation loading:

**Start with `references/` folder** (quick access for common operations):
- Check these curated reference files first as they cover 80% of typical GAM use cases
- Files available: quick_reference.md, command_syntax.md, common_patterns.md, safety_checklist.md, troubleshooting.md, api_scopes.md, examples.md

**Load from `wiki/` folder** (comprehensive documentation, 165 pages):
- Read specific wiki pages only when needed for detailed/advanced operations
- Complete GAM wiki is bundled for offline access
- Use progressive disclosure - load only contextually relevant pages
- Key pages: Collections-of-Users.md, Groups.md, Drive-Items.md, Calendars.md, Organizational-Units.md, Bulk-Processing.md, CSV-Input-Filtering.md

**Documentation Strategy**: References first for speed, wiki for depth. Claude automatically determines which files to load based on context.

### 3. Construct GAM Commands
Based on documentation:
- Build correct GAM command syntax
- Handle entity selections (users, groups, OUs)
- Apply filters and options appropriately
- Plan CSV input/output for bulk operations

### 4. Validate and Assess Safety

**Analyze every command before execution:**
- Assess risk level: LOW (read-only), MEDIUM (individual changes), HIGH (bulk changes), CRITICAL (deletions/suspensions)
- Validate CSV files using Read tool when bulk operations are involved
- Generate preview commands when available (e.g., `gam print` before modifying)
- Check command syntax against documentation

**Risk Assessment Guidelines:**
- CRITICAL: delete operations, bulk suspensions (>10), wipe commands
- HIGH: bulk updates (>10), permission changes (bulk), password resets (bulk)
- MEDIUM: individual user/group updates, OU moves, alias changes
- LOW: print/info/show commands, read-only reports

### 5. Confirm Before Executing

**Always confirm before:**
- Modifying or deleting resources
- Operations affecting multiple users/groups (>5)
- Changing permissions or security settings
- Performing bulk operations from CSV files
- Any CRITICAL or HIGH risk operations

**Confirmation process:**
1. Show the exact command(s) to be executed
2. Explain what the command will do and estimated impact
3. Highlight any risks or irreversible actions
4. Request explicit user approval
5. Wait for user confirmation before proceeding

**Read-only operations** (print, info, show) may execute without confirmation unless specifically requested by the user.

### 6. Execute and Report Results
- Run GAM commands using Bash tool
- Capture and parse command output
- Report success/failure clearly with relevant details
- If errors occur, consult troubleshooting.md and suggest fixes
- For CSV output, offer to analyze or summarize results
- Generate follow-up reports or validation checks as needed

## Safety Rules

**Core Safety Principles:**
1. **Preview before modifying** - Use `gam print` or `gam info` to preview impact
2. **Test with small samples** - For bulk operations, test with 1-2 entities first
3. **Backup current state** - Export data before major changes
4. **Validate CSV files** - Read and verify CSV data before using in commands
5. **Batch size for large operations** - Use `config batch_size` to manage API quotas
6. **No "all users" modifications** - Use specific selections (OU, CSV, query)

**For detailed safety procedures, pre-flight checklists, and rollback strategies**, reference `references/safety_checklist.md`.

## Progressive Disclosure Architecture

This skill uses a two-tier documentation system optimized for efficient context usage:

**Tier 1: references/** - Quick reference (7 files, ~66KB total)
- Loaded first for common operations
- Curated content covering 80% of typical use cases
- Fast access for standard workflows

**Tier 2: wiki/** - Complete documentation (165 files, ~4MB)
- Loaded progressively only when specific topics are needed
- Full GAM wiki bundled for offline access
- Claude determines relevance and loads files contextually

This architecture ensures comprehensive documentation without context bloat.

## Inputs

**Required:**
- User's task description or goal
- Access to `references/` folder (bundled in skill)
- Access to `wiki/` folder (bundled in skill)

**Optional:**
- CSV or Excel files for bulk operations
- Specific identifiers (emails, group names, file IDs)
- Filter criteria (domains, queries, date ranges)
- Output format preferences

## Outputs

**Commands:**
- Properly formatted GAM commands
- Terminal output from command execution
- Success/failure status with details

**Data:**
- CSV exports from GAM operations
- Summary reports and analysis
- Error logs and troubleshooting guidance

## Constraints

- **GAM7 must be pre-installed** - Assumes `gam` command is in PATH
- **Authentication required** - Assumes GAM OAuth is configured (oauth2.txt exists)
- **Network access required** - GAM operations require internet connectivity to Google APIs
- **Admin privileges needed** - GAM requires appropriate Google Workspace admin permissions
- **Destructive operations are irreversible** - Always confirm and backup before deletions

## Error Handling Strategy

When errors occur:
1. **Capture the exact error message** from GAM output
2. **Identify the error category**: authentication, syntax, permissions, API quota, or resource not found
3. **Consult** `references/troubleshooting.md` for common error solutions
4. **Suggest corrective action** based on error type
5. **Offer to retry** with corrected command or parameters

**Common error categories:**
- **Command not found** → Verify GAM installation and PATH
- **Authentication errors** → Check oauth2.txt, suggest re-authorization
- **Syntax errors** → Re-read relevant documentation, verify command structure
- **Permission errors** → Verify API scopes and admin privileges
- **API quota exceeded** → Suggest batch_size parameter or retry timing

For detailed troubleshooting procedures and solutions, reference `references/troubleshooting.md`.

## Additional Resources

For detailed examples of real-world GAM workflows and use cases, reference `references/examples.md`.

For complete command syntax patterns and detailed command options, reference `references/command_syntax.md` and `references/common_patterns.md`.

For API scope requirements when setting up GAM, reference `references/api_scopes.md`.
