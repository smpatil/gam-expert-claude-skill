# GAM Command Syntax Guide

Complete guide to GAM command structure and syntax patterns.

---

## Basic Command Structure

```
gam <entity-selection> <command> <resource> <options>
```

**Components:**
- `gam` - The GAM command itself
- `<entity-selection>` - Which users/groups to operate on (optional for some commands)
- `<command>` - Action to perform (create, update, delete, print, etc.)
- `<resource>` - What to act upon (user, group, calendar, etc.)
- `<options>` - Additional parameters and flags

---

## Entity Selection

Entity selection determines which users, groups, or resources the command operates on.

### Single User
```bash
gam user john@example.com <command>
gam user john@example.com show info
```

### All Users in Domain
```bash
gam all users <command>
gam all users show info
```

### Organizational Unit
```bash
# Users in specific OU (not including sub-OUs)
gam ou "/Sales" <command>
gam ou "/Sales" update user title "Sales Representative"

# OU and all sub-OUs
gam ou_and_children "/Sales" <command>
gam ou_and_children "/Sales" show info
```

### Group Members
```bash
# All members of a group
gam group sales@example.com <command>
gam group sales@example.com show info
```

### Query Selection
```bash
# Users matching specific criteria
gam print users query "<query>" | gam csv - <command>

# Example: All suspended users
gam print users query "isSuspended=true" | gam csv - gam user ~email show info
```

### CSV File
```bash
# Iterate over CSV file
gam csvfile users.csv gam user ~email <command>

# Specify column for email
gam csvfile users.csv:EmailColumn gam user ~email <command>
```

### Multiple Entities (Comma-Separated)
```bash
# Not officially supported, use CSV instead
# For just 2-3, run separate commands
gam user alice@example.com show info
gam user bob@example.com show info
```

---

## Command Types

### Information Commands (Read-Only)

**Print** - Output to CSV format
```bash
gam print users
gam print groups
gam print ous
```

**Info** - Detailed information about entity
```bash
gam info user john@example.com
gam info group team@example.com
gam info domain
```

**Show** - Display entity data
```bash
gam user john@example.com show info
gam user john@example.com show calendars
gam user john@example.com show filelist
```

### Modification Commands

**Create** - Create new entity
```bash
gam create user john@example.com firstname John lastname Smith password TempPass123!
gam create group team@example.com name "Team Group"
```

**Update** - Modify existing entity
```bash
gam update user john@example.com ou "/Sales"
gam update group team@example.com add member alice@example.com
```

**Delete** - Remove entity
```bash
gam delete user john@example.com
gam delete group team@example.com
```

---

## Quoting Rules

### When to Use Quotes

**Required for:**
- Values with spaces
- Organizational unit paths
- Email signatures with HTML
- Queries with special characters

```bash
# Correct with quotes
gam update user john@example.com ou "/Sales Team"
gam update user john@example.com title "Senior Manager"
gam print users query "orgUnitPath='/Sales' isSuspended=false"

# Wrong without quotes (will fail or misinterpret)
gam update user john@example.com ou /Sales Team  # Only sees "/Sales"
gam update user john@example.com title Senior Manager  # "Senior" only
```

### Quote Types

**Double quotes** (preferred for most cases)
```bash
gam update user john@example.com ou "/Sales"
gam print users query "orgUnitPath='/Sales'"
```

**Single quotes** (shell dependent)
```bash
gam update user john@example.com ou '/Sales'
```

**Nested quotes**
```bash
# Use different quote types
gam print users query "orgUnitPath='/Sales'"

# Or escape inner quotes
gam print users query "orgUnitPath=\"/Sales\""
```

---

## CSV File Operations

### Basic CSV Usage

**CSV Format:**
```csv
email,firstname,lastname
john@example.com,John,Smith
jane@example.com,Jane,Doe
```

**Command:**
```bash
gam csvfile users.csv gam create user ~email firstname ~firstname lastname ~lastname password TempPass123!
```

### Column Substitution

Use `~columnname` to reference CSV columns:

```bash
# CSV columns: email,ou,title
gam csvfile employees.csv gam update user ~email ou ~ou title ~title
```

### Specifying Column for Entity

```bash
# If email column isn't named "email"
gam csvfile users.csv:EmailAddress gam user ~EmailAddress show info

# Still use ~ for other columns
gam csvfile users.csv:EmailAddress gam user ~EmailAddress firstname ~FirstName
```

### CSV with Standard Input

```bash
# Pipe CSV output to another command
gam print users ou "/Sales" | gam csv - gam user ~email update ou "/Marketing"
```

### CSV Filtering

```bash
# Print specific columns
gam print users fields email,name,ou

# Filter with matchfield
gam csvfile users.csv matchfield ou "/Sales" gam user ~email show info
```

---

## Output Redirection

### Save to File

```bash
# Redirect stdout
gam print users > users.csv

# Use redirect command
gam redirect csv users.csv print users

# Redirect both stdout and stderr
gam print users > users.csv 2> errors.txt

# Combine stdout and stderr
gam print users > output.txt 2>&1
```

### Format Options

**CSV output** (default for print commands)
```bash
gam print users
```

**JSON output**
```bash
gam print users formatjson > users.json
```

**Pretty print for terminal**
```bash
gam info user john@example.com
```

---

## Query Syntax

Queries filter entities based on criteria.

### User Queries

```bash
# Suspended users
gam print users query "isSuspended=true"

# Users in specific OU
gam print users query "orgUnitPath='/Sales'"

# External users
gam print users query "isExternal=true"

# Multiple conditions (AND)
gam print users query "orgUnitPath='/Sales' isSuspended=false"

# Date comparisons
gam print users query "creationTime>2024-01-01T00:00:00"
gam print users query "lastLoginTime<2023-10-01T00:00:00"
```

### Drive Queries

```bash
# Files modified after date
gam user john@example.com show filelist query "modifiedTime>2024-01-01"

# Files by owner
gam user john@example.com show filelist query "owner='john@example.com'"

# Files with specific name
gam user john@example.com show filelist query "title contains 'Budget'"

# Shared externally
gam user john@example.com show filelist query "visibility='anyoneWithLink'"

# Multiple conditions
gam user john@example.com show filelist query "mimeType='application/pdf' and modifiedTime>2024-01-01"
```

---

## Field Selection

Limit output to specific fields for efficiency.

### User Fields

```bash
# Specific fields
gam print users fields email,name,suspended

# All fields
gam print users allfields

# Primary email only
gam print users fields primaryEmail
```

### Common Field Names

**Users:**
- `primaryEmail`, `name`, `givenName`, `familyName`
- `suspended`, `archived`, `orgUnitPath`
- `creationTime`, `lastLoginTime`
- `isAdmin`, `isDelegatedAdmin`, `isEnrolledIn2Sv`

**Groups:**
- `email`, `name`, `description`
- `directMembersCount`

**Drive:**
- `id`, `title`, `mimeType`, `owners`, `permissions`
- `createdTime`, `modifiedTime`, `size`

---

## Batch Operations

### Batch Size (API Quota Management)

```bash
# Process 50 entities at a time
gam config batch_size 50 all users show info

# With CSV file
gam config batch_size 100 csvfile users.csv gam user ~email update ou "/Sales"
```

### Wait on Failure

```bash
# Retry on transient failures
gam config wait_on_fail all users show info
```

### Continue on Error

```bash
# Don't stop on individual failures
gam config continue_on_error csvfile users.csv gam create user ~email ...
```

---

## Regular Expressions

Some commands support regex patterns.

### Group Membership Patterns

```bash
# Add users matching pattern to group
gam update group team@example.com add pattern ".*@sales.example.com"
```

### Drive File Selection

```bash
# Regex in queries (API dependent)
gam user john@example.com show filelist query "title contains 'Report'"
```

---

## Multi-Step Commands

Chain operations together.

### Update Multiple Attributes

```bash
gam update user john@example.com \
  ou "/Sales" \
  title "Senior Manager" \
  phone type work primary value "555-1234" \
  suspended false
```

### Group with Multiple Settings

```bash
gam create group team@example.com \
  name "Team Group" \
  description "Project team" \
  who_can_join INVITED_CAN_JOIN \
  who_can_post_message ALL_MEMBERS_CAN_POST
```

---

## Special Syntax Elements

### Organizational Units

**Format:** Must start with `/`

```bash
gam update user john@example.com ou "/"              # Root
gam update user john@example.com ou "/Sales"         # Top-level
gam update user john@example.com ou "/Sales/West"    # Nested
```

**Case sensitive!**
```bash
gam ou "/Sales"        # Correct
gam ou "/sales"        # Wrong if OU is named "Sales"
```

### Date/Time Format

**ISO 8601 format:** `YYYY-MM-DDTHH:MM:SS`

```bash
gam print users query "creationTime>2024-01-01T00:00:00"
gam calendar cal@example.com addevent start 2024-01-15T10:00:00 end 2024-01-15T11:00:00
```

### Boolean Values

```bash
# Accepted: true, false, on, off, yes, no, 1, 0
gam update user john@example.com suspended true
gam update user john@example.com suspended on
gam update user john@example.com changepassword false
```

---

## Command Chaining (Shell)

Combine GAM with shell commands.

### Pipe Output

```bash
# Count users in OU
gam print users ou "/Sales" | wc -l

# Filter with grep
gam print users | grep "suspended,false"

# Sort output
gam print users fields email,name | sort
```

### Sequential Operations

```bash
# AND operator (stops on failure)
gam info user john@example.com && gam update user john@example.com suspended on

# OR operator (runs if first fails)
gam info user john@example.com || echo "User not found"

# Run regardless
gam info user john@example.com; gam info user jane@example.com
```

### Loops

```bash
# Loop over users
for user in alice@example.com bob@example.com; do
  gam user $user update ou "/Sales"
done

# Loop over CSV (without gam csvfile)
while IFS=, read -r email name; do
  gam create user $email firstname $name
done < users.csv
```

---

## Configuration Options

Set GAM behavior with config command.

### Common Config Options

```bash
# Set batch size
gam config batch_size 50 <command>

# Wait and retry on failures
gam config wait_on_fail <command>

# Continue even if some operations fail
gam config continue_on_error <command>

# Set Drive directory for file operations
gam config drive_dir /path/to/files <command>

# Auto-refresh
gam config auto_refresh true <command>

# Debug level
gam config debug_level info <command>
```

### Persistent Configuration

Edit `gam.cfg` file:

```ini
batch_size = 50
num_threads = 5
debug_level = error
drive_dir = /path/to/drive/files
```

---

## Common Syntax Mistakes

### ❌ Missing Quotes
```bash
# Wrong
gam update user john@example.com ou /Sales Team

# Right
gam update user john@example.com ou "/Sales Team"
```

### ❌ Wrong Entity Selection
```bash
# Wrong - "user" is the entity type, not selection
gam user update ou "/Sales"

# Right - specify which user
gam user john@example.com update ou "/Sales"
```

### ❌ Incorrect OU Path
```bash
# Wrong - missing leading /
gam update user john@example.com ou "Sales"

# Right
gam update user john@example.com ou "/Sales"
```

### ❌ CSV Column Mismatch
```bash
# CSV header: EmailAddress,FirstName,LastName
# Wrong - column names must match
gam csvfile users.csv gam create user ~email firstname ~firstname

# Right
gam csvfile users.csv gam create user ~EmailAddress firstname ~FirstName
```

---

## Syntax Quick Reference

| **Pattern** | **Example** |
|------------|-------------|
| Single user | `gam user john@example.com <cmd>` |
| All users | `gam all users <cmd>` |
| OU | `gam ou "/Sales" <cmd>` |
| CSV | `gam csvfile file.csv gam user ~email <cmd>` |
| Query | `gam print users query "..."` |
| Batch | `gam config batch_size 50 <cmd>` |
| Fields | `gam print users fields email,name` |
| Redirect | `gam print users > out.csv` |
| Quotes | `ou "/Sales Team"` |
| Date | `2024-01-15T10:00:00` |

---

## Resources

- **Full command reference:** https://github.com/GAM-team/GAM/wiki
- **CSV operations:** https://github.com/GAM-team/GAM/wiki/CSV-Input-Filtering
- **Query syntax:** https://developers.google.com/admin-sdk/directory/v1/guides/search-users

---

## Tips

1. **Test syntax** with `info` or `print` commands first
2. **Use quotes** liberally - better safe than sorry
3. **Start small** - test with 1-2 entities before bulk operations
4. **Check documentation** when unsure about syntax
5. **Use helper scripts** - `gam_helper.py validate "<command>"`
