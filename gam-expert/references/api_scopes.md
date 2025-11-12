# GAM API Scopes Reference

Understanding Google API scopes required for GAM operations.

---

## What Are API Scopes?

API scopes define what actions GAM is authorized to perform on your Google Workspace. When you run `gam oauth create`, you're granting GAM permission to use specific Google APIs on your behalf.

### Scope Types

1. **OAuth Scopes** - Used for admin operations (gam oauth create)
2. **Service Account Scopes** - Used for user-specific operations (domain-wide delegation)

---

## Core Admin Directory Scopes

### `https://www.googleapis.com/auth/admin.directory.user`
**Required for:** User management operations

**Operations:**
- Create, read, update, delete users
- Manage user profiles and settings
- Suspend/unsuspend users
- Password management
- User aliases

**Commands:**
```bash
gam create user ...
gam update user ...
gam delete user ...
gam info user ...
gam print users
```

---

### `https://www.googleapis.com/auth/admin.directory.group`
**Required for:** Group management operations

**Operations:**
- Create, read, update, delete groups
- Manage group membership
- View group information

**Commands:**
```bash
gam create group ...
gam update group ... add/remove member ...
gam info group ...
gam print groups
```

---

### `https://www.googleapis.com/auth/admin.directory.orgunit`
**Required for:** Organizational unit management

**Operations:**
- Create, read, update, delete OUs
- Move users between OUs
- View OU structure

**Commands:**
```bash
gam create org ...
gam print ous
gam update user ... ou "/New/OU"
```

---

### `https://www.googleapis.com/auth/admin.directory.domain`
**Required for:** Domain management

**Operations:**
- View domain information
- Manage domain aliases
- Domain verification

**Commands:**
```bash
gam info domain
gam print domains
```

---

### `https://www.googleapis.com/auth/admin.directory.device.chromeos`
**Required for:** ChromeOS device management

**Operations:**
- List ChromeOS devices
- Update device settings
- Deprovision devices

**Commands:**
```bash
gam print cros
gam info cros ...
gam update cros ... action disable
```

---

### `https://www.googleapis.com/auth/admin.directory.device.mobile`
**Required for:** Mobile device management

**Operations:**
- List mobile devices
- Manage mobile device policies
- Wipe devices

**Commands:**
```bash
gam print mobile
gam update mobile ... action wipe
```

---

## Group Settings Scope

### `https://www.googleapis.com/auth/apps.groups.settings`
**Required for:** Advanced group settings

**Operations:**
- Configure who can post/join
- Set group visibility
- Email delivery preferences

**Commands:**
```bash
gam update group ... who_can_join ...
gam update group ... who_can_post_message ...
gam info group ... settings
```

---

## Drive & Docs Scopes

### `https://www.googleapis.com/auth/drive`
**Required for:** Full Drive access

**Operations:**
- List files and folders
- Manage file permissions
- Transfer ownership
- Create/delete files
- Access Shared Drives

**Commands:**
```bash
gam user ... show filelist
gam user ... add/update/delete drivefileacl
gam user ... transfer drive
gam print shareddrives
```

---

### `https://www.googleapis.com/auth/drive.readonly`
**Required for:** Read-only Drive access

**Operations:**
- List files (read-only)
- View permissions (read-only)

**Commands:**
```bash
gam user ... show filelist
gam user ... print drivefileacls
```

**Note:** Use this for auditing when modification isn't needed.

---

## Gmail Scopes

### `https://www.googleapis.com/auth/gmail.settings.basic`
**Required for:** Gmail settings management

**Operations:**
- Email signatures
- Vacation responders
- Email forwarding
- POP/IMAP settings

**Commands:**
```bash
gam user ... signature ...
gam user ... vacation ...
gam user ... forward ...
```

---

### `https://www.googleapis.com/auth/gmail.settings.sharing`
**Required for:** Delegation and send-as settings

**Operations:**
- Email delegation
- Send-as addresses

**Commands:**
```bash
gam user ... delegate to ...
gam user ... show delegates
gam user ... sendasaddress ...
```

---

### `https://www.googleapis.com/auth/gmail.modify`
**Required for:** Gmail message operations

**Operations:**
- Read, modify, delete messages
- Apply labels
- Manage filters

**Commands:**
```bash
gam user ... delete messages ...
gam user ... show messages ...
gam user ... filter ...
```

---

## Calendar Scopes

### `https://www.googleapis.com/auth/calendar`
**Required for:** Full calendar access

**Operations:**
- Create/update/delete events
- Manage calendar ACLs
- Access calendar resources

**Commands:**
```bash
gam calendar ... addevent ...
gam calendar ... add owner/editor/reader ...
gam user ... show calendars
```

---

### `https://www.googleapis.com/auth/calendar.readonly`
**Required for:** Read-only calendar access

**Operations:**
- View calendars and events

**Commands:**
```bash
gam calendar ... printevents
gam user ... show calendars
```

---

## Reports & Audit Scopes

### `https://www.googleapis.com/auth/admin.reports.audit.readonly`
**Required for:** Audit log access

**Operations:**
- Admin audit logs
- Login reports
- Activity reports

**Commands:**
```bash
gam report admin ...
gam report logins ...
gam report drive ...
```

---

### `https://www.googleapis.com/auth/admin.reports.usage.readonly`
**Required for:** Usage reports

**Operations:**
- User usage reports
- Domain usage statistics

**Commands:**
```bash
gam report usage customer ...
gam report usage user ...
```

---

## Classroom Scopes

### `https://www.googleapis.com/auth/classroom.courses`
**Required for:** Classroom course management

**Operations:**
- Create/update/delete courses
- Manage course membership

**Commands:**
```bash
gam create course ...
gam course ... add student/teacher ...
gam print courses
```

---

## Cloud Identity Scopes

### `https://www.googleapis.com/auth/cloud-identity.groups`
**Required for:** Cloud Identity group operations

**Operations:**
- Manage Cloud Identity groups (different from Google Groups)

**Commands:**
```bash
gam create cigroup ...
gam info cigroup ...
```

---

## Service Account Domain-Wide Delegation

For automated operations without user interaction, configure service account with domain-wide delegation.

### Setting Up Service Account Scopes

1. **Create service account in Google Cloud Console**
2. **Download service account key (JSON)**
3. **Enable domain-wide delegation**
4. **In Admin Console:**
   - Navigate to: Security > API controls > Domain-wide delegation
   - Add service account Client ID
   - Add required scopes

### Common Service Account Scope Combinations

**For user management automation:**
```
https://www.googleapis.com/auth/admin.directory.user
https://www.googleapis.com/auth/admin.directory.group
https://www.googleapis.com/auth/admin.directory.orgunit
```

**For Drive operations automation:**
```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/admin.directory.user
```

**For Gmail operations automation:**
```
https://www.googleapis.com/auth/gmail.settings.basic
https://www.googleapis.com/auth/gmail.settings.sharing
https://www.googleapis.com/auth/gmail.modify
```

---

## Checking Current Scopes

### View Authorized OAuth Scopes
```bash
gam oauth info
```

**Output shows:**
- Currently authorized scopes
- When authorization was created
- Which account is authorized

### View Service Account Authorization
```bash
gam user admin@example.com check serviceaccount
```

**Output shows:**
- Service account status
- Authorized scopes for service account
- Any authorization issues

---

## Re-Authorizing with New Scopes

### When You Need New Scopes

If you get errors like:
- `insufficient permission`
- `does not have required scope`
- `Access denied`

### Re-Authorize OAuth

```bash
# Re-create OAuth with all scopes
gam oauth create

# During browser flow, grant ALL requested permissions

# Verify new scopes
gam oauth info
```

### Update Service Account Scopes

1. **Admin Console > Security > API controls > Domain-wide delegation**
2. **Find your service account (by Client ID)**
3. **Edit and add missing scopes**
4. **Save changes**
5. **Test:** `gam user admin@example.com check serviceaccount`

---

## Scope Troubleshooting

### Error: "Access denied" even with correct scope

**Possible causes:**
1. **Admin role insufficient** - Need Super Admin or specific delegated admin role
2. **Scope not in service account delegation** - Check Admin Console settings
3. **OAuth token stale** - Re-run `gam oauth create`
4. **API not enabled in GCP project** - Enable in Cloud Console

**Solutions:**
```bash
# Check what's authorized
gam oauth info
gam user admin@example.com check serviceaccount

# Re-authorize
gam oauth create

# Verify admin role
gam info user admin@example.com | grep isAdmin
```

---

### Error: "Insufficient scope" for specific API

**Solution:**
```bash
# Authorize specific scope
gam oauth create scope https://www.googleapis.com/auth/admin.directory.user

# Or re-authorize with all scopes
gam oauth create
```

---

## Scope Security Best Practices

### Principle of Least Privilege

✅ **Do:**
- Grant only scopes needed for your operations
- Use read-only scopes when possible
- Separate service accounts for different purposes
- Document which scopes are used and why

❌ **Don't:**
- Grant all scopes "just in case"
- Share service account keys
- Use production service account for testing

### Scope Combinations for Common Use Cases

**Read-Only Auditing:**
```
https://www.googleapis.com/auth/admin.directory.user.readonly
https://www.googleapis.com/auth/admin.directory.group.readonly
https://www.googleapis.com/auth/drive.readonly
https://www.googleapis.com/auth/admin.reports.audit.readonly
```

**User Provisioning:**
```
https://www.googleapis.com/auth/admin.directory.user
https://www.googleapis.com/auth/admin.directory.group
https://www.googleapis.com/auth/admin.directory.orgunit
```

**Drive Management:**
```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/admin.directory.user.readonly
```

**Gmail Administration:**
```
https://www.googleapis.com/auth/gmail.settings.basic
https://www.googleapis.com/auth/gmail.settings.sharing
https://www.googleapis.com/auth/admin.directory.user.readonly
```

---

## Quick Reference Table

| **Operation** | **Required Scope** |
|---------------|-------------------|
| Create users | `admin.directory.user` |
| Manage groups | `admin.directory.group` |
| Group settings | `apps.groups.settings` |
| Manage OUs | `admin.directory.orgunit` |
| Drive files | `drive` |
| Gmail settings | `gmail.settings.basic` |
| Gmail delegation | `gmail.settings.sharing` |
| Gmail messages | `gmail.modify` |
| Calendar events | `calendar` |
| Audit logs | `admin.reports.audit.readonly` |
| Usage reports | `admin.reports.usage.readonly` |
| ChromeOS devices | `admin.directory.device.chromeos` |
| Mobile devices | `admin.directory.device.mobile` |
| Classroom | `classroom.courses` |

---

## Resources

- **Full scope list:** https://developers.google.com/identity/protocols/oauth2/scopes
- **GAM authorization guide:** https://github.com/GAM-team/GAM/wiki/Authorization
- **Service account setup:** https://github.com/GAM-team/GAM/wiki/Service-Accounts
