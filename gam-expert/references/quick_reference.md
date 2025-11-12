# GAM Quick Reference

Top 50 most commonly used GAM commands organized by category.

## Table of Contents
- [User Management](#user-management)
- [Group Management](#group-management)
- [Organizational Units](#organizational-units)
- [Drive Management](#drive-management)
- [Calendar Management](#calendar-management)
- [Gmail Management](#gmail-management)
- [Reports & Auditing](#reports--auditing)
- [Domain & Admin](#domain--admin)

---

## User Management

### Create User
```bash
gam create user <email> firstname <First> lastname <Last> password <Pass>
gam create user john@example.com firstname John lastname Smith password TempPass123! changepassword on
```

### Update User
```bash
gam update user <email> [options]
gam update user john@example.com ou "/Sales" phone type work primary value "555-1234"
```

### Delete User
```bash
gam delete user <email>
```

### Suspend/Unsuspend User
```bash
gam update user <email> suspended on
gam update user <email> suspended off
```

### Get User Info
```bash
gam info user <email>
gam user john@example.com show info
```

### List/Print Users
```bash
gam print users
gam print users query "orgUnitPath='/Sales'"
gam print users ou "/Engineering"
```

### Reset Password
```bash
gam update user <email> password <NewPassword> changepassword on
```

### Move User to Different OU
```bash
gam update user <email> ou "/New/OrgUnit"
```

### Add/Remove User Alias
```bash
gam create alias <alias@domain.com> user <email>
gam delete alias <alias@domain.com>
```

### Bulk User Operations (CSV)
```bash
gam csvfile users.csv:email gam user ~email update ou "/Marketing"
gam csvfile users.csv gam create user ~email firstname ~firstname lastname ~lastname password ~password
```

---

## Group Management

### Create Group
```bash
gam create group <email> name "Group Name" description "Description"
gam create group sales@example.com name "Sales Team"
```

### Delete Group
```bash
gam delete group <email>
```

### Get Group Info
```bash
gam info group <email>
```

### List/Print Groups
```bash
gam print groups
gam print groups domain example.com
```

### Add Member to Group
```bash
gam update group <group@domain.com> add member <user@domain.com>
gam update group <group@domain.com> add manager <user@domain.com>
gam update group <group@domain.com> add owner <user@domain.com>
```

### Remove Member from Group
```bash
gam update group <group@domain.com> remove member <user@domain.com>
```

### List Group Members
```bash
gam print group-members group <email>
gam info group <email> members
```

### Update Group Settings
```bash
gam update group <email> who_can_join INVITED_CAN_JOIN
gam update group <email> who_can_post_message ALL_MEMBERS_CAN_POST
```

### Bulk Add Members (CSV)
```bash
gam csvfile members.csv gam update group ~group add member ~email
```

---

## Organizational Units

### Create OU
```bash
gam create org "/ParentOU/NewOU" name "New Organizational Unit"
```

### Delete OU
```bash
gam delete org "/ParentOU/OldOU"
```

### List OUs
```bash
gam print ous
gam info org "/"
```

### Move Users to OU
```bash
gam update user <email> ou "/Target/OU"
gam ou_and_children "/Source/OU" update user ou "/Target/OU"
```

---

## Drive Management

### List Drive Files
```bash
gam user <email> show filelist
gam user <email> show filelist query "title contains 'Budget'"
```

### Print Drive File Permissions
```bash
gam user <email> print drivefileacls <fileID>
gam user <email> show drivefileacls <fileID>
```

### Add Drive Permission
```bash
gam user <email> add drivefileacl <fileID> user <email> role writer
gam user <email> add drivefileacl <fileID> domain example.com role reader
gam user <email> add drivefileacl <fileID> anyone role reader withlink
```

### Remove Drive Permission
```bash
gam user <email> delete drivefileacl <fileID> <permissionID>
```

### Transfer Drive Ownership
```bash
gam user <old-owner@domain.com> transfer drive <new-owner@domain.com>
```

### Shared Drive Management
```bash
gam print shareddrives
gam create shareddrive "Team Drive Name"
gam add drivefileacl <sharedDriveID> user <email> role organizer
```

---

## Calendar Management

### List Calendars
```bash
gam user <email> show calendars
gam calendar <calendar@domain.com> info
```

### Add Calendar ACL
```bash
gam calendar <calendar@domain.com> add owner <email>
gam calendar <calendar@domain.com> add editor <email>
gam calendar <calendar@domain.com> add reader <email>
```

### Create Calendar Event
```bash
gam calendar <calendar@domain.com> addevent start 2024-01-15T10:00:00 end 2024-01-15T11:00:00 summary "Meeting"
```

### List Calendar Events
```bash
gam calendar <calendar@domain.com> printevents after 2024-01-01
```

---

## Gmail Management

### Email Delegation
```bash
gam user <email> delegate to <delegate@domain.com>
gam user <email> show delegates
```

### Signatures
```bash
gam user <email> signature file signature.html
gam user <email> show signature
```

### Gmail Filters
```bash
gam user <email> filter from test@example.com label "Important"
gam user <email> show filters
```

### Send Email
```bash
gam user <email> sendemail recipient <to@domain.com> subject "Subject" message "Body"
```

### Search/Delete Messages
```bash
gam user <email> delete messages query "in:trash older_than:30d"
gam user <email> trash messages query "from:spam@example.com"
```

---

## Reports & Auditing

### Admin Audit Log
```bash
gam report admin start -7d
gam report admin user admin@example.com event USER_SETTINGS start -30d
```

### Login Activity
```bash
gam report logins start -7d
```

### Drive Audit
```bash
gam report drive start -7d user user@example.com
```

### Usage Reports
```bash
gam report usage customer parameters accounts:num_users
gam report usage user user@example.com
```

### Print Users with Details
```bash
gam print users allfields
gam print users fields email,name,suspended,ou
```

---

## Domain & Admin

### Domain Info
```bash
gam info domain
```

### OAuth Info
```bash
gam oauth info
gam oauth create
```

### Version & Configuration
```bash
gam version
gam config drive_dir /path/to/drive/files
```

### Check Service Account
```bash
gam user <admin@domain.com> check serviceaccount
```

### API Quotas
```bash
gam show apiservices
```

---

## Command Patterns

### Entity Selection
```bash
# Single user
gam user john@example.com <command>

# All users
gam all users <command>

# Users in OU
gam ou "/Sales" <command>

# Users in OU and sub-OUs
gam ou_and_children "/Sales" <command>

# Group members
gam group sales@example.com <command>

# CSV file
gam csvfile users.csv:email gam user ~email <command>

# Query
gam print users query "orgUnitPath='/Sales' suspended=false"
```

### Output Formats
```bash
# Print to CSV (stdout)
gam print users > users.csv

# Print to file
gam redirect csv users.csv print users

# JSON output
gam print users formatjson > users.json
```

### Batch Options
```bash
# Control batch size for API quota management
gam config batch_size 50 csvfile users.csv gam user ~email update ou "/New"

# Wait on API failures
gam config wait_on_fail csvfile users.csv gam user ~email show info
```

---

## Useful Filters & Queries

### User Queries
```bash
# Suspended users
gam print users query "isSuspended=true"

# Users in specific OU
gam print users query "orgUnitPath='/Sales'"

# External users (Cloud Identity)
gam print users query "isExternal=true"

# Recently created users
gam print users query "creationTime>2024-01-01T00:00:00"
```

### Drive Queries
```bash
# Files shared externally
query "visibility='anyoneWithLink' or visibility='anyoneCanFind'"

# Files modified recently
query "modifiedTime>2024-01-01"

# Files by owner
query "owner='user@example.com'"

# Files with specific name
query "title contains 'Budget'"
```

---

## Tips

1. **Always use quotes** for values with spaces: `ou "/Sales Team"`
2. **Test with small samples** before bulk operations
3. **Use `gam print`** to preview before modifying
4. **Check syntax** in GAM wiki before complex commands
5. **Monitor API quotas** with batch_size for large operations
6. **Save output** to files for large reports: `gam print users > users.csv`

For complete documentation, visit: https://github.com/GAM-team/GAM/wiki
