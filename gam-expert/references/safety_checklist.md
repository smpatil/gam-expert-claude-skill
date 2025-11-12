# GAM Safety Checklist

Best practices and safety procedures for GAM operations.

---

## Risk Assessment

### Operation Risk Levels

**CRITICAL (Always Confirm)**
- `delete user`
- `delete group`
- `wipe` (ChromeOS/mobile devices)
- `deprovision`
- Bulk suspensions (>10 users)
- Bulk deletions (any count)

**HIGH (Confirm for Bulk)**
- `suspend user`
- `update user` (bulk >10)
- `remove member` (bulk)
- Drive permission changes (bulk)
- Password resets (bulk)

**MEDIUM (Review Command)**
- `create user`
- `update user` (individual)
- `add member`
- OU moves
- Alias changes

**LOW (Generally Safe)**
- `print` commands
- `info` commands
- `show` commands
- Read-only reports

---

## Pre-Flight Checklist

### Before ANY Destructive Operation

- [ ] **Understand the full impact** - What will this command do?
- [ ] **Test environment** - Is this the correct domain?
- [ ] **Backup data** - Export current state to CSV
- [ ] **Small test first** - Run on 1-2 entities
- [ ] **Preview with print** - Use read-only equivalent first
- [ ] **Verify entity selection** - Double-check email addresses/queries
- [ ] **Have rollback plan** - How to undo if needed?
- [ ] **Approval obtained** - Manager/security team aware?
- [ ] **Maintenance window** - Is this scheduled/announced?
- [ ] **Monitor ready** - Can you watch for errors in real-time?

### Before Bulk Operations (>50 entities)

- [ ] **CSV validated** - Check with csv_generator.py
- [ ] **Batch size set** - API quotas won't be exceeded
- [ ] **Timing planned** - Off-peak hours for large ops
- [ ] **Progress tracking** - Script to monitor completion
- [ ] **Error handling** - What happens if some fail?
- [ ] **Communication sent** - Users notified if applicable
- [ ] **Backup admin available** - Someone to help if issues arise

---

## Safety Commands

### Use Preview Commands First

Before executing, run preview equivalent:

| **Instead of this:** | **First run this:** |
|----------------------|---------------------|
| `gam update user ...` | `gam info user ...` |
| `gam delete user ...` | `gam info user ...` |
| `gam update group ... add member` | `gam info group ...` |
| `gam ou "/Source" update ...` | `gam print users ou "/Source"` |
| `gam csvfile X update ...` | `gam csvfile X info ...` or preview CSV |

### Export Current State

Always export before modifying:

```bash
# Before user changes
gam info user john@example.com > john_before.txt

# Before group changes
gam print group-members group team@example.com > team_members_before.csv

# Before bulk user changes
gam print users ou "/Sales" allfields > sales_users_before.csv

# Before Drive permission changes
gam user owner@example.com print drivefileacls <fileID> > permissions_before.csv
```

### Test with Small Sample

```bash
# Instead of this dangerous command:
gam ou "/Sales" update user suspended on

# Do this first (just 2 users):
gam print users ou "/Sales" maxresults 2 | gam csv - gam update user ~email suspended on

# Then verify
gam print users query "orgUnitPath='/Sales' isSuspended=true"

# If good, proceed with full command
```

---

## Bulk Operation Safety

### Use Batch Size

```bash
# Prevents API quota exhaustion
gam config batch_size 50 csvfile large_file.csv gam user ~email update ou "/New"
```

### Wait on Failure

```bash
# Automatically retries on transient errors
gam config wait_on_fail csvfile file.csv gam create user ~email ...
```

### Split Large CSVs

```bash
# Use batch_planner.py to split
python3 scripts/batch_planner.py split users.csv batch_ 100

# Process one batch at a time
for file in batch_*.csv; do
  echo "Processing $file"
  gam csvfile $file gam user ~email update ...
  sleep 5
done
```

### Progress Tracking

```bash
# Generate shell script with progress tracking
python3 scripts/batch_planner.py script 'gam csvfile {csv_file}:email ...' batch_*.csv

# Run the generated script
./run_batches.sh
```

---

## Common Safety Mistakes

### ❌ DON'T: Run destructive commands without testing
```bash
# DANGEROUS - no preview
gam all users delete messages query "subject:Test"
```

### ✅ DO: Test scope first
```bash
# Safe - check count first
gam all users print messages query "subject:Test" | wc -l

# Test on one user
gam user test@example.com delete messages query "subject:Test"

# If good, proceed carefully
```

---

### ❌ DON'T: Use "all users" for modifications
```bash
# DANGEROUS - affects everyone
gam all users update user suspended on
```

### ✅ DO: Use specific selection
```bash
# Safe - specific OU
gam ou "/Contractors" update user suspended on

# Or CSV with explicit list
gam csvfile users_to_suspend.csv gam update user ~email suspended on
```

---

### ❌ DON'T: Forget to quote values with spaces
```bash
# WRONG - will fail or behave unexpectedly
gam update user john@example.com ou /Sales Team
```

### ✅ DO: Quote properly
```bash
# Correct
gam update user john@example.com ou "/Sales Team"
```

---

### ❌ DON'T: Ignore errors in bulk operations
```bash
# Dangerous - keeps running even if errors occur
gam csvfile users.csv gam create user ~email ... > /dev/null 2>&1
```

### ✅ DO: Capture and review errors
```bash
# Good - saves all output
gam csvfile users.csv gam create user ~email ... 2>&1 | tee operation.log

# Review errors
grep -i error operation.log
```

---

## Rollback Procedures

### User Suspension (Undo)
```bash
# Restore from backup CSV
gam csvfile suspended_users.csv gam update user ~email suspended off
```

### OU Move (Undo)
```bash
# Restore from backup
gam csvfile original_locations.csv gam update user ~email ou ~orgunitpath
```

### Group Membership (Undo)
```bash
# Remove members
gam csvfile added_members.csv gam update group ~group remove member ~email

# Re-add members
gam csvfile removed_members.csv gam update group ~group add member ~email
```

### Drive Permissions (Undo)
```bash
# Remove added permissions (need permission IDs from backup)
gam user owner@example.com delete drivefileacl <fileID> <permissionID>
```

### User Deletion (CANNOT UNDO EASILY)
⚠️ **User deletion is NOT easily reversible!**
- Deleted users go to "Deleted Users" for 20 days
- Can be restored but loses some settings/data
- Prevention is key - always confirm twice

```bash
# To restore deleted user (within 20 days)
gam undelete user john@example.com
```

---

## Emergency Procedures

### Stop Running Operation

```bash
# Press Ctrl+C to interrupt GAM command
# For background jobs: find PID and kill
ps aux | grep gam
kill <PID>
```

### Rapid Verification Check

```bash
# Quick count of suspended users
gam print users query "isSuspended=true" | wc -l

# Quick OU member count
gam print users ou "/Sales" | wc -l

# Quick group member count
gam info group team@example.com | grep "Members:"
```

### When Things Go Wrong

1. **STOP** - Don't make it worse with hasty fixes
2. **ASSESS** - What exactly happened?
3. **DOCUMENT** - Save all output/logs immediately
4. **ROLLBACK** - Use backup CSVs to restore
5. **NOTIFY** - Alert affected users and management
6. **INVESTIGATE** - Analyze what went wrong
7. **PREVENT** - Update procedures to prevent recurrence

---

## Security Best Practices

### Authentication & Authorization

- ✅ Use dedicated admin account for GAM operations
- ✅ Enable 2FA on admin accounts
- ✅ Rotate OAuth tokens periodically
- ✅ Use service account for automated operations
- ✅ Limit who has GAM access
- ❌ Never share oauth2.txt or service account keys
- ❌ Don't run GAM with production admin during testing

### Data Protection

- ✅ Store CSV files in secure location
- ✅ Encrypt sensitive CSV files (passwords, etc.)
- ✅ Delete temporary CSV files after use
- ✅ Use secure file transfer for CSV files
- ❌ Don't email CSV files with passwords
- ❌ Don't commit CSV files with real data to git
- ❌ Don't leave backups on shared drives

### Audit Trail

- ✅ Log all GAM operations: `gam ... 2>&1 | tee logs/operation_$(date +%Y%m%d).log`
- ✅ Keep CSV files used for operations
- ✅ Document who ran what and when
- ✅ Review Admin Console Audit logs regularly
- ✅ Set up alerts for sensitive operations

---

## Validation Tools

Use the provided helper scripts:

```bash
# Analyze command safety
python3 scripts/gam_helper.py analyze "gam delete user test@example.com"

# Check environment readiness
python3 scripts/config_checker.py

# Validate CSV format
python3 scripts/csv_generator.py validate users.csv 'email,firstname,lastname'

# Plan bulk operation
python3 scripts/batch_planner.py analyze update_user 500 users.csv
```

---

## When to Seek Help

**STOP and consult before proceeding if:**
- Operation affects >100 users
- Deleting anything (users, groups, files)
- Changing domain-wide settings
- Unsure about command syntax
- Getting unexpected errors
- Testing new complex workflow

**Resources:**
- GAM Wiki: https://github.com/GAM-team/GAM/wiki
- GAM Google Group: https://groups.google.com/g/google-apps-manager
- Your organization's IT/Security team

---

## Checklist Summary

Before running ANY command:
1. ✅ Read and understand what it does
2. ✅ Test with dry-run/preview
3. ✅ Backup current state
4. ✅ Test with small sample (1-2 entities)
5. ✅ Have rollback plan ready
6. ✅ Monitor output for errors
7. ✅ Verify results after completion
8. ✅ Document what was done

**Remember: It's better to be slow and safe than fast and sorry!**
