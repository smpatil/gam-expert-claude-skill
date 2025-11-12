# GAM Expert Skill - Example Usage Scenarios

Real-world examples of using the GAM Expert skill to solve common Google Workspace administration tasks.

## Scenario 1: New Employee Onboarding

**Situation**: You need to onboard 25 new employees with accounts, group memberships, and calendar access.

**What you provide**:
- CSV file `new_hires.csv` with columns: email, firstname, lastname, department, manager

**How to use the skill**:
```
User: "I need to create accounts for the 25 new employees in new_hires.csv.
       Each should get a temporary password, be in their department OU,
       added to their department group, and given access to the company calendar."
```

**What the skill does**:
1. Reads `Collections-of-Users.md`, `Groups-Membership.md`, `Calendars.md`
2. Uses Python to validate the CSV file format
3. Constructs a multi-step plan:
   - Create user accounts with temp passwords
   - Move users to correct OUs based on department
   - Add users to department groups
   - Grant calendar access
4. Shows you the exact commands for review
5. Asks for confirmation before executing
6. Executes each step and reports progress
7. Provides summary report of what was completed

**Sample output**:
```
I'll help onboard these 25 employees. Let me first validate the CSV file...

✓ CSV validated: 25 rows, all required columns present

Here's my plan:
1. Create 25 user accounts with temporary passwords
2. Assign users to OUs based on department column
3. Add users to their department groups
4. Grant access to company calendar

Commands I'll run:
1. gam csvfile new_hires.csv:email:firstname:lastname create user ~email firstname ~firstname lastname ~lastname password "Welcome2024!" changepassword on

2. gam csvfile new_hires.csv:email:department update user ~email ou "/~department"

3. gam csvfile new_hires.csv:email:department update group ~department@example.com add member ~email

4. gam csvfile new_hires.csv:email add calendars company@example.com user ~email role reader

This will create 25 new accounts. Proceed? (yes/no)
```

---

## Scenario 2: Quarterly Group Membership Audit

**Situation**: You need to audit all groups, identify groups with external members, and export for review.

**How to use the skill**:
```
User: "Generate a report of all our Google Groups showing which ones have external members
       from outside our @example.com domain. I need it in a spreadsheet."
```

**What the skill does**:
1. Reads `Groups.md` and `Groups-Membership.md`
2. Constructs command to export all groups with members
3. Executes (read-only, no confirmation needed)
4. Uses Python to process the output and identify external members
5. Creates a formatted spreadsheet with findings
6. Provides summary statistics

**Sample interaction**:
```
I'll generate that audit report for you. This is a read-only operation.

Running: gam print groups members external internaldomains example.com

Processing output... Found 47 groups total.

Analysis:
- 12 groups have external members
- 35 groups are internal-only
- Total external members across all groups: 23 unique email addresses

Creating detailed spreadsheet... Done!

Saved to: group_external_members_audit.csv

Top groups with external members:
1. partners@example.com - 8 external members
2. vendors@example.com - 5 external members
3. board@example.com - 4 external members
```

---

## Scenario 3: Employee Department Transfer

**Situation**: 15 employees are moving from Sales to Marketing department. Need to update OUs, groups, and Drive access.

**CSV file** `transfers.csv`:
```
email,old_department,new_department,effective_date
alice@example.com,Sales,Marketing,2024-03-01
bob@example.com,Sales,Marketing,2024-03-01
...
```

**How to use the skill**:
```
User: "I have 15 employees transferring from Sales to Marketing in transfers.csv.
       They need to be moved to the Marketing OU, removed from Sales groups,
       added to Marketing groups, and given access to the Marketing shared drive."
```

**What the skill does**:
1. Reads relevant documentation
2. Validates CSV file
3. Shows detailed plan with all operations
4. **CRITICAL**: Asks for explicit confirmation since this affects many users
5. Executes step-by-step with progress updates
6. Verifies each change
7. Reports any issues

**Sample confirmation prompt**:
```
⚠️  IMPORTANT: This operation will affect 15 user accounts

Changes to be made:
- Move 15 users from /Sales OU to /Marketing OU
- Remove 15 users from sales@example.com group
- Remove 15 users from sales-team@example.com group
- Add 15 users to marketing@example.com group
- Add 15 users to marketing-team@example.com group
- Grant access to Marketing Shared Drive (ID: 0ABC...) for 15 users

Commands:
1. gam csvfile transfers.csv:email update user ~email ou "/Marketing"
2. gam csvfile transfers.csv:email update group sales@example.com remove member ~email
3. gam csvfile transfers.csv:email update group sales-team@example.com remove member ~email
4. gam csvfile transfers.csv:email update group marketing@example.com add member ~email
5. gam csvfile transfers.csv:email update group marketing-team@example.com add member ~email
6. gam csvfile transfers.csv:email add shareddrive <driveId> user ~email role writer

Please review carefully. Type CONFIRM to proceed:
```

---

## Scenario 4: Emergency User Suspension

**Situation**: Security incident requires immediate suspension of compromised accounts.

**How to use the skill**:
```
User: "URGENT: I need to immediately suspend these accounts due to security incident:
       john@example.com
       alice@example.com
       bob@example.com

       Also revoke their Drive file access and delegate their email to security@example.com"
```

**What the skill does**:
1. Recognizes urgency but still prioritizes safety
2. Shows exactly what will happen
3. Requests confirmation (faster than normal but still required)
4. Executes immediately upon confirmation
5. Provides step-by-step progress
6. Confirms completion of each critical step

**Sample interaction**:
```
I understand this is urgent. I'll prepare the commands immediately.

CRITICAL SECURITY OPERATION
Will suspend 3 accounts and secure their data:

Immediate actions:
1. Suspend users (revokes all sessions immediately)
2. Revoke Drive file access for external shares
3. Delegate Gmail to security@example.com for investigation
4. Generate access report for review

Commands:
gam users john@example.com,alice@example.com,bob@example.com update user suspended on
gam users john@example.com,alice@example.com,bob@example.com update user signoutuser
gam users john@example.com,alice@example.com,bob@example.com delegate to security@example.com

This is a major security operation affecting 3 accounts.
Type YES to execute immediately:
```

---

## Scenario 5: Shared Drive Permission Cleanup

**Situation**: Need to audit and clean up a Shared Drive with 500+ files that has accumulated permissions over time.

**How to use the skill**:
```
User: "Our 'Projects' shared drive has gotten messy with permissions.
       Can you generate a report of all files and their permissions,
       identify any files shared with 'anyone', and help me fix those?"
```

**What the skill does**:
1. Reads `Drive-Items.md` and `Shared-Drives.md`
2. Exports all files and permissions (read-only)
3. Uses Python to analyze the data
4. Identifies security issues
5. Generates actionable report
6. Offers to create cleanup commands

**Sample interaction**:
```
I'll audit the Projects shared drive permissions.

Step 1: Exporting file list...
Running: gam user admin@example.com print filelist select <SharedDriveID> fields id,name,permissions

Found 547 files.

Step 2: Analyzing permissions...

🔍 Analysis Results:

Security Issues Found:
- 23 files shared with "Anyone with the link"
- 15 files shared with external domains
- 8 files with 10+ individual permissions (permission sprawl)

Summary:
- Total files: 547
- Files with security issues: 38 (7%)
- Unique external email addresses with access: 12
- Most common permission level: Editor (could be reduced to Viewer)

Generated reports:
1. files_anyone_access.csv - Files shared publicly
2. files_external_access.csv - Files shared externally
3. files_permission_sprawl.csv - Files with too many permissions
4. permission_summary.xlsx - Full analysis with pivot tables

Would you like me to:
A) Generate commands to remove 'Anyone' access from those 23 files
B) Review external access for approval
C) Both
```

---

## Scenario 6: Bulk User Update from HR System Export

**Situation**: HR system exported updated employee data. Need to update titles, departments, managers, and phone numbers in Google Workspace.

**CSV file** `hr_export.csv` with 300 rows:
```
email,title,department,manager_email,phone,building
alice@example.com,Senior Manager,Marketing,ceo@example.com,555-0123,Building A
...
```

**How to use the skill**:
```
User: "I have the latest HR data in hr_export.csv with 300 employees.
       Need to update their titles, departments, managers, phone numbers, and building locations in Google."
```

**What the skill does**:
1. Validates CSV format and data quality
2. Identifies what fields map to GAM properties
3. Shows sample of changes to be made
4. Requests confirmation for bulk update
5. Executes with progress tracking
6. Reports success/failure for each update
7. Generates error report if any updates fail

**Sample interaction**:
```
Validating HR export data...

✓ CSV file valid: 300 rows
✓ All required columns present
✓ Email format valid for all rows
✓ Manager emails verified as existing users

Field mapping:
- hr_export.title → orgTitle
- hr_export.department → orgDepartment
- hr_export.manager_email → manager
- hr_export.phone → phoneNumber
- hr_export.building → orgCostCenter (using building as cost center)

Sample changes (first 3 rows):
1. alice@example.com: Update title to "Senior Manager", department to "Marketing"
2. bob@example.com: Update title to "Engineer", department to "Engineering"
3. carol@example.com: Update title to "Director", department to "Sales"

Command to execute:
gam csvfile hr_export.csv:email:title:department:manager_email:phone:building \
  update user ~email \
  organization title ~title department ~department costcenter ~building \
  relation manager ~manager_email \
  phone work ~phone

This will update 300 user accounts with new HR data. Proceed? (yes/no)

[After confirmation]

Processing updates...
[Progress bar: 50/300 completed]

Update complete!
- Successfully updated: 298 users
- Failed: 2 users (see error_log.txt)
  - john@example.com: Manager not found
  - jane@example.com: Invalid phone format

Would you like me to help fix the 2 failed updates?
```

---

## Scenario 7: Automated Weekly Group Report

**Situation**: Need a recurring report of all group memberships for compliance.

**How to use the skill**:
```
User: "I need to generate our weekly group membership report.
       Show all groups, their members, and highlight any changes from last week's report."
```

**What the skill does**:
1. Generates current group membership export
2. Compares with previous week's report (if provided)
3. Identifies changes (additions, removals)
4. Creates formatted report with change highlights
5. Saves with timestamp for next week's comparison

**Sample interaction**:
```
Generating weekly group membership report...

Export current group memberships:
gam print groups members > group_report_2024-03-15.csv

Processing data... Found 85 groups, 1,247 total memberships.

Comparing with last week's report (group_report_2024-03-08.csv)...

📊 Weekly Changes:

New Groups (2):
- contractors-2024@example.com (5 members)
- project-phoenix@example.com (12 members)

Membership Changes:
Groups with additions: 15 groups, 23 new members total
Groups with removals: 8 groups, 11 members removed
Groups unchanged: 60 groups

Top 5 Most Active Groups This Week:
1. engineering@example.com (+5 members, -2 members)
2. marketing@example.com (+4 members, -1 member)
3. sales@example.com (+3 members, -0 members)
4. hr@example.com (+3 members, -0 members)
5. executives@example.com (+0 members, -1 member)

Reports generated:
1. group_report_2024-03-15.csv - Current snapshot
2. group_changes_week_2024-03-15.csv - Just the changes
3. group_report_summary_2024-03-15.txt - This summary

Files saved for next week's comparison.
```

---

## Tips for Using These Examples

1. **Start simple** - Try read-only operations first to get comfortable
2. **Provide context** - Mention if it's urgent, compliance-related, or testing
3. **Have data ready** - CSV files, email addresses, group names
4. **Review carefully** - Always review the commands before confirming
5. **Save outputs** - Keep CSV reports for historical comparison
6. **Ask questions** - The skill can explain any command or option

## Common Patterns Across Examples

1. **Validation first** - Skill always validates inputs before executing
2. **Show the plan** - You see exactly what will happen
3. **Confirm dangerous ops** - Explicit confirmation for modifications
4. **Progress tracking** - Real-time updates for long operations
5. **Error handling** - Clear reporting of what succeeded and what failed
6. **Documentation** - Results saved as CSV/reports for records
