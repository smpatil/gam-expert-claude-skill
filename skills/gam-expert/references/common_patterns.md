# Common GAM Patterns & Workflows

20 most common real-world use cases with complete examples.

---

## 1. Onboarding New Employees (Bulk)

**Scenario:** Create multiple new users from CSV file with standard settings.

**CSV File (new_hires.csv):**
```csv
email,firstname,lastname,password,orgunit,title
john.smith@example.com,John,Smith,TempPass123!,/Sales,Sales Representative
jane.doe@example.com,Jane,Doe,TempPass456!,/Marketing,Marketing Manager
```

**Commands:**
```bash
# Preview the data first
python3 scripts/spreadsheet_processor.py preview new_hires.csv

# Create users from CSV
gam csvfile new_hires.csv gam create user ~email firstname ~firstname lastname ~lastname password ~password changepassword on ou ~orgunit title ~title

# Verify creation
gam csvfile new_hires.csv gam info user ~email
```

---

## 2. Offboarding Departing Employees

**Scenario:** Secure user account when employee leaves.

**Complete Workflow:**
```bash
# 1. Transfer Drive ownership to manager
gam user departed@example.com transfer drive manager@example.com

# 2. Create Archive Google Group
gam create group departed-archive

# 3. Remove from all groups (except preserved ones)
gam user departed@example.com delete groups

# 4. Archive emails to Google Group
gam user departed@example.com archive messages departed-archive@example.com doit

# 5. Delete the user
gam delete user departed@example.com
```

---

## 3. Adding Users to Group from CSV

**Scenario:** Add multiple users to a group for project collaboration.

**CSV File (project_team.csv):**
```csv
email,role
alice@example.com,MEMBER
bob@example.com,MEMBER
carol@example.com,MANAGER
```

**Commands:**
```bash
# Validate CSV first
python3 scripts/csv_generator.py validate project_team.csv 'email,role'

# Add members
gam csvfile project_team.csv gam update group project-alpha@example.com add ~role ~email

# Verify membership
gam info group project-alpha@example.com members
```

---

## 4. Departmental Reorganization

**Scenario:** Move all users from one OU to another during company restructuring.

**Commands:**
```bash
# 1. Preview users to be moved
gam print users ou "/Sales/West Coast" fields email,name

# 2. Export to CSV for records
gam redirect csv west_coast_users.csv print users ou "/Sales/West Coast"

# 3. Move all users
gam ou "/Sales/West Coast" update user ou "/Sales/Enterprise"

# 4. Verify the move
gam print users query "orgUnitPath='/Sales/Enterprise'" | grep -c "@"
```

---

## 5. Bulk Password Reset

**Scenario:** Force password reset for security incident.

**CSV File (reset_users.csv):**
```csv
email
compromised1@example.com
compromised2@example.com
compromised3@example.com
```

**Commands:**
```bash
# Generate temporary passwords and force change
gam csvfile reset_users.csv gam update user ~email password $(uuidgen | cut -c1-12) changepassword on

# Send password reset emails
gam csvfile reset_users.csv gam user ~email sendemail recipient ~email subject "Password Reset Required" message "Your password has been reset for security reasons. You will be prompted to create a new password on next login."

# Revoke all OAuth tokens
gam csvfile reset_users.csv gam user ~email deprovision
```

---

## 6. External Sharing Audit

**Scenario:** Find all Drive files shared with external users.

**Commands:**
```bash
# Get all externally shared files for a user
gam user employee@example.com show filelist query "visibility='anyoneWithLink' or visibility='anyoneCanFind'" > external_shares.csv

# For entire domain (high API usage)
gam config batch_size 10 all users show filelist query "visibility='anyoneWithLink'" > all_external_shares.csv

# Remove external sharing from specific file
gam user employee@example.com update drivefile <fileID> visibility private
```

---

## 7. Creating Distribution Lists

**Scenario:** Create email distribution lists for departments.

**Commands:**
```bash
# Create the group
gam create group all-sales@example.com name "All Sales Staff" description "Distribution list for sales department" who_can_join INVITED_CAN_JOIN who_can_post_message ALL_IN_DOMAIN_CAN_POST

# Add all users from Sales OU
gam ou "/Sales" update group all-sales@example.com add member

# Verify membership count
gam info group all-sales@example.com | grep "Members:"
```

---

## 8. Delegate Calendar Access

**Scenario:** Give assistant access to executive calendars.

**Commands:**
```bash
# Add calendar editor permission
gam calendar exec1@example.com add editor assistant@example.com
gam calendar exec2@example.com add editor assistant@example.com
gam calendar exec3@example.com add editor assistant@example.com

# Alternative: Grant via CSV
# CSV: executive_email,assistant_email
gam csvfile calendar_access.csv gam calendar ~executive_email add editor ~assistant_email
```

---

## 9. License Management / Reporting

**Scenario:** Audit license usage and identify inactive users.

**Commands:**
```bash
# Get all users with license SKUs
gam print users allfields > all_users_licenses.csv

# Get last login time for all users
gam print users fields email,lastLoginTime > user_logins.csv

# Find users who haven't logged in for 90+ days
gam print users query "lastLoginTime<2023-10-01T00:00:00" fields email,lastLoginTime

# Suspend inactive users
gam print users query "lastLoginTime<2023-10-01T00:00:00" | gam csv - gam update user ~email suspended on
```

---

## 10. Shared Drive Management

**Scenario:** Create shared drive for team collaboration with proper permissions.

**Commands:**
```bash
# Create shared drive
gam create shareddrive "Marketing Team Drive" ou "/Marketing"

# Get the shared drive ID (from output or query)
gam print shareddrives | grep "Marketing Team Drive"

# Add organizers
gam add drivefileacl <sharedDriveID> user manager@example.com role organizer

# Add content managers
gam add drivefileacl <sharedDriveID> group marketing-leads@example.com role contentmanager

# Add contributors
gam add drivefileacl <sharedDriveID> group marketing-team@example.com role contributor

# Show permissions
gam show drivefileacl <sharedDriveID>
```

---

## 11. Email Signature Rollout

**Scenario:** Deploy standardized email signatures across organization.

**HTML Signature Template (signature.html):**
```html
<div>
  <strong>{{firstname}} {{lastname}}</strong><br>
  {{title}}<br>
  {{company}}<br>
  {{phone}}
</div>
```

**Commands:**
```bash
# For single user with template
gam user john@example.com signature file signature.html replace firstname "John" replace lastname "Smith" replace title "Sales Manager"

# For bulk (requires preprocessing CSV with full HTML)
# CSV should have: email,signature_html
gam csvfile signatures.csv gam user ~email signature "~signature_html"
```

---

## 12. Group Membership Sync

**Scenario:** Sync group membership with CSV file (add missing, remove extra).

**CSV File (current_members.csv):**
```csv
email
alice@example.com
bob@example.com
carol@example.com
```

**Commands:**
```bash
# Get current members
gam print group-members group team@example.com > existing_members.csv

# Sync: Add members from CSV
gam csvfile current_members.csv gam update group team@example.com add member ~email

# Sync: Remove members not in CSV (manual comparison needed)
# Use scripts/spreadsheet_processor.py to find differences
```

---

## 13. Vacation Responder Setup

**Scenario:** Enable out-of-office replies for users on leave.

**Commands:**
```bash
# Enable vacation responder
gam user employee@example.com vacation on subject "Out of Office" message "I am out of the office until January 20th. For urgent matters, please contact backup@example.com" startdate 2024-01-15 enddate 2024-01-20

# Disable vacation responder
gam user employee@example.com vacation off

# Check vacation status
gam user employee@example.com show vacation
```

---

## 14. Drive Folder Permissions Inheritance

**Scenario:** Apply permissions to folder and all contents.

**Commands:**
```bash
# Add permission to folder (recursive to contents)
gam user owner@example.com add drivefileacl <folderID> user collaborator@example.com role writer

# Remove external access from folder and contents
gam user owner@example.com delete drivefileacl <folderID> domain anyone
```

---

## 15. Alias Management

**Scenario:** Create email aliases for users (department addresses, nicknames).

**CSV File (aliases.csv):**
```csv
user_email,alias
john.smith@example.com,jsmith@example.com
john.smith@example.com,john@example.com
jane.doe@example.com,jdoe@example.com
```

**Commands:**
```bash
# Create aliases
gam csvfile aliases.csv gam create alias ~alias user ~user_email

# List all aliases for user
gam user john.smith@example.com show aliases

# Remove alias
gam delete alias jsmith@example.com
```

---

## 16. ChromeOS Device Management

**Scenario:** Manage Chromebooks for returning/new students or employees.

**Commands:**
```bash
# List all Chrome devices
gam print cros

# Get device info
gam info cros <deviceID>

# Disable device (lost/stolen)
gam update cros <deviceID> action disable

# Re-enable device
gam update cros <deviceID> action reenable

# Deprovision device (wipe and unenroll)
gam update cros <deviceID> action deprovision_same_model_replacement
```

---

## 17. Security Alert: Suspend All Users in Compromised OU

**Scenario:** Immediate response to security incident affecting specific department.

**Commands:**
```bash
# 1. Get list of affected users (for records)
gam redirect csv affected_users.csv print users ou "/Compromised/Department" fields email,name

# 2. Suspend all users in OU
gam ou "/Compromised/Department" update user suspended on

# 3. Revoke all active OAuth tokens
gam ou "/Compromised/Department" user deprovision

# 4. Verify suspension
gam print users query "orgUnitPath='/Compromised/Department' isSuspended=true"

# 5. Later: Unsuspend after resolution
gam csvfile affected_users.csv gam update user ~email suspended off
```

---

## 18. Gmail Filter Deployment

**Scenario:** Deploy spam filter or organizational rule across users.

**Commands:**
```bash
# Create filter for all users
gam all users filter from "spam-domain.com" label "Spam" trash

# Create filter for specific OU
gam ou "/Sales" filter subject "EXTERNAL:" label "External Email" markimportant

# Show existing filters
gam user employee@example.com show filters
```

---

## 19. Report: Users Without 2FA

**Scenario:** Identify users who haven't enabled 2-factor authentication.

**Commands:**
```bash
# Get all users with 2FA status
gam print users fields email,isEnrolledIn2Sv,isEnforcedIn2Sv > 2fa_status.csv

# Filter users without 2FA (query not supported, use CSV filtering)
gam print users | grep "False,False" > users_without_2fa.csv

# Send reminder email
gam csvfile users_without_2fa.csv gam user ~email sendemail recipient ~email subject "Enable 2-Factor Authentication" message "Please enable 2FA for security"
```

---

## 20. Classroom Course Setup

**Scenario:** Create Google Classroom course and add students/teachers.

**Commands:**
```bash
# Create course
gam create course alias "math-101-2024" name "Mathematics 101" section "Spring 2024" teacher teacher@example.com

# Get course ID from output or query
gam print courses teacher teacher@example.com

# Add students from CSV
# CSV: email
gam csvfile students.csv gam course <courseID> add student ~email

# Add co-teachers
gam course <courseID> add teacher assistant@example.com

# List course membership
gam print course-participants course <courseID>
```

---

## Workflow Tips

### Before Large Operations
1. **Preview with print/info commands**
2. **Test with 2-3 entities first**
3. **Export current state to CSV** (for rollback)
4. **Use batch_size** for API quota management

### During Operations
1. **Monitor output for errors**
2. **Save logs:** `gam ... 2>&1 | tee operation.log`
3. **Use progress tracking** (batch_planner.py script)

### After Operations
1. **Verify with print/info commands**
2. **Check for failed entities**
3. **Document changes**
4. **Retain CSV files for records**

For more complex workflows, combine commands with shell scripts or use Python scripts for data processing.
