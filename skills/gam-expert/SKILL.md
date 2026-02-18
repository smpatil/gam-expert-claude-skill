---
name: gam-expert
description: |
  Expert at executing GAM (Google Apps Manager) commands for Google Workspace administration.
  Use this skill when the user needs to manage Google Workspace users, groups, calendars, drive files,
  organizational units, or other Google Workspace resources. Make sure to use this skill whenever the
  user mentions GAM, Google Workspace admin tasks, bulk user operations, Google group management,
  OU management, Chrome device management, Google Drive permissions, email delegation, license
  management, or any task involving the `gam` command-line tool — even if they don't explicitly
  say "GAM." If someone asks to create users, manage groups, pull a report from Google Workspace,
  or do anything that sounds like Google Workspace administration, this is the right skill.
  Assumes GAM7 is already installed and configured.
---

# GAM Expert

Google Workspace administration expert using GAM7. Understand the request, look up the right command, verify safety, confirm with the user, and execute.

Prerequisite: GAM7 installed and authenticated (`gam` in PATH, `oauth2.txt` exists).

## Workflow

### 1. Understand the Request

Identify the resource (users, groups, drive, calendars, Chrome, etc.), operation type (create, update, delete, read/print, bulk), whether CSV files are involved, and how many resources will be affected.

### 2. Look Up the Right Command

**Check `references/` first** — 7 curated guides covering ~80% of common operations:

| File | Use when |
|------|----------|
| `quick_reference.md` | Need a common command fast (top 50 by category) |
| `command_syntax.md` | Need entity selection, filters, or option details |
| `common_patterns.md` | Building a multi-step workflow (onboarding, offboarding, audits) |
| `examples.md` | Want a full walkthrough of a real-world scenario |
| `safety_checklist.md` | Assessing risk or planning a destructive/bulk operation |
| `troubleshooting.md` | A command failed and you need to diagnose it |
| `api_scopes.md` | User hits permission errors or needs to configure scopes |

**Fall back to `wiki/` for advanced or uncommon operations** — 166 pages of complete GAM documentation. Read only the specific page needed. Key pages by topic:

| Topic | Wiki page(s) |
|-------|-------------|
| User management | `Users.md`, `Users-Tokens.md` |
| Targeting users | `Collections-of-Users.md` |
| Groups & membership | `Groups.md`, `Groups-Membership.md` |
| Cloud Identity groups | `Cloud-Identity-Groups.md`, `Cloud-Identity-Groups-Membership.md` |
| Drive files & permissions | `Drive-Items.md`, `Users-Drive-Files-Manage.md`, `Users-Drive-Permissions.md` |
| Shared Drives | `Shared-Drives.md`, `Users-Shared-Drives.md` |
| Drive file selection | `Drive-File-Selection.md` |
| Calendars & events | `Calendars.md`, `Calendars-Events.md`, `Users-Calendars.md` |
| Gmail settings | `Users-Gmail-Send-As-Signature-Vacation.md`, `Users-Gmail-Delegates.md` |
| Gmail messages | `Users-Gmail-Messages-Threads.md`, `Users-Gmail-Labels.md` |
| Organizational Units | `Organizational-Units.md` |
| Chrome/ChromeOS | `ChromeOS-Devices.md`, `Chrome-Policies.md`, `Chrome-Printers.md` |
| Classroom | `Classroom-Courses.md`, `Classroom-Membership.md` |
| Bulk operations | `Bulk-Processing.md`, `CSV-Input-Filtering.md`, `CSV-Output-Filtering.md` |
| Reports & auditing | `Reports.md` |
| Aliases | `Aliases.md` |
| Licenses | `Licenses.md` |
| OAuth & auth | `Authorization.md` |
| Config options | `gam.cfg.md` |

### 3. Build the Command

Construct correct GAM syntax from the documentation. Handle entity selections (individual users, groups, OUs, CSV lists), apply filters and options, and plan CSV input/output for bulk operations.

### 4. Assess Risk and Confirm

GAM operates at the domain level — a single bad command can affect every user in the organization. Before executing any write operation:

1. Classify risk level per `references/safety_checklist.md`
2. For bulk operations, preview with `gam print` first and validate any CSV files using the Read tool
3. Show the user the exact command(s), explain impact, flag anything irreversible
4. Wait for explicit approval before executing

Read-only operations (`print`, `info`, `show`) can run without confirmation.

### 5. Execute and Report

Run the command via Bash, report results clearly. If errors occur, consult `references/troubleshooting.md`. For CSV output, offer to analyze or summarize. Suggest follow-up commands when appropriate (e.g., verify a change took effect).
