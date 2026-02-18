# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skill for managing Google Workspace using GAM7 (Google Apps Manager). It provides expert-level assistance with GAM commands through natural language interaction. The skill is distributed as a Claude Code plugin that can be installed via the marketplace or manually.

**Key characteristics:**
- This is a skill/plugin repository, not a traditional software project with compiled code
- No build process, tests, or compilation required
- The skill consists of markdown documentation files that Claude reads at runtime
- Uses progressive documentation loading (loads only what's needed when needed)

## Repository Structure

```
gam-expert-claude-skill/
├── .claude-plugin/         # Plugin marketplace metadata
│   └── marketplace.json
├── skills/
│   └── gam-expert/         # The actual skill directory
│       ├── SKILL.md        # Core skill instructions - lean workflow + wiki navigation
│       ├── references/     # Quick reference docs (7 curated guides)
│       │   ├── quick_reference.md     # Top 50 common GAM commands
│       │   ├── command_syntax.md      # Detailed command patterns
│       │   ├── common_patterns.md     # Frequently used templates
│       │   ├── safety_checklist.md    # Pre-execution safety checks
│       │   ├── api_scopes.md          # OAuth scope requirements
│       │   ├── troubleshooting.md     # Common issues and solutions
│       │   └── examples.md            # Real-world use case examples
│       └── wiki/            # Complete GAM documentation (166 pages, ~3.3MB)
│           └── *.md         # Full GAM wiki bundled for offline access
├── README.md               # Human-facing repository documentation
├── CLAUDE.md               # This file
└── LICENSE
```

## Architecture

### Skill Execution Model

When a user mentions GAM or Google Workspace tasks, Claude automatically invokes this skill by loading `skills/gam-expert/SKILL.md`. The skill then:

1. **Understands request** - Identifies what Google Workspace resource needs management
2. **Reads documentation** - Uses progressive loading:
   - First checks `references/` folder (covers 80% of common operations)
   - Falls back to `wiki/` folder for comprehensive documentation (166 pages)
3. **Constructs GAM command** - Builds proper command syntax from docs
4. **Validates safety** - Analyzes command risk level (LOW/MEDIUM/HIGH/CRITICAL)
5. **Confirms with user** - Always asks before destructive/bulk operations
6. **Executes via bash** - Runs GAM commands and reports results

### Progressive Documentation Loading

The skill uses a two-tier documentation approach optimized for performance:

**Tier 1: references/** - Quick reference (7 files, ~100KB total)
- Loaded first for common operations
- Curated content covering 80% of use cases
- Fast access for typical workflows

**Tier 2: wiki/** - Complete documentation (166 files, ~3.3MB)
- Loaded only when specific topics are needed
- Full GAM wiki bundled for offline access
- Progressive disclosure prevents context bloat

Claude only reads specific wiki pages when contextually relevant (e.g., `wiki/Groups.md` when managing groups).

### Safety System

The skill has built-in safety mechanisms:

1. **Risk assessment** - Analyzes every command before execution
2. **Confirmation prompts** - Required for:
   - Destructive operations (delete, suspend, modify permissions)
   - Bulk operations (affecting >5 resources)
   - Any operation the user hasn't explicitly confirmed
3. **Preview mode** - Uses `gam print` commands to show what will happen
4. **CSV validation** - Reads and validates CSV files before using in bulk ops

## Development Workflow

### Testing Changes to the Skill

Since this is a documentation-based skill, "testing" means validating that:

1. **Skill loads correctly** in Claude Code
2. **Documentation is accurate** and properly formatted
3. **Examples work** as described

To test locally:
```bash
# Install the skill locally
cp -r skills/gam-expert ~/.claude/skills/

# Start Claude Code and test
claude
```

Then ask GAM-related questions to verify the skill works.

### Editing Documentation

All skill behavior is defined in markdown files. Key files to edit:

- `skills/gam-expert/SKILL.md` - Core workflow and instructions (keep lean, <500 lines)
- `skills/gam-expert/references/*.md` - Quick reference guides (includes examples, command syntax, safety, etc.)
- `skills/gam-expert/wiki/*.md` - Comprehensive GAM documentation (usually don't edit - this is bundled from GAM project)

After editing, reinstall the skill to test changes:
```bash
rm -rf ~/.claude/skills/gam-expert
cp -r skills/gam-expert ~/.claude/skills/
```

### Creating Distribution Package

For distribution via Claude.ai (not Claude Code):
```bash
cd gam-expert-claude-skill
zip -r gam-expert.zip skills/gam-expert/
```

Users can then upload `gam-expert.zip` to Claude.ai (Settings > Capabilities > Skills).

## Git Workflow

Standard git workflow:
```bash
# Make changes
git add .
git commit -m "Description of changes"
git push origin main

# After push, users can install/update via:
# /plugin marketplace add c0webster/gam-expert-claude-skill
```

## Important Constraints

### Prerequisites
- This skill requires **GAM7 to be pre-installed** on the user's system
- GAM must be authenticated (`gam oauth create` completed)
- The skill assumes `gam` command is available in PATH
- Does not install or configure GAM - only helps use it

### Documentation Scope
- `references/` docs are maintained in this repo
- `wiki/` docs are bundled from the GAM project (https://github.com/GAM-team/GAM/wiki)
- When updating GAM wiki docs, re-clone from upstream: `git clone https://github.com/GAM-team/GAM.wiki.git`

## Key Design Decisions

### Why Bundle the Entire Wiki?
The complete GAM wiki (166 pages, ~3.3MB) is bundled to ensure:
- **Offline access** - No network calls to GitHub during skill execution
- **Version stability** - Documentation matches skill behavior
- **Performance** - Direct file reads faster than web fetches
- **Progressive loading** - Claude only reads files when contextually relevant

### Why Two-Tier Documentation?
The `references/` vs `wiki/` split optimizes for:
- **Quick access** - Common operations don't require reading large docs
- **Comprehensive coverage** - Advanced operations have full documentation
- **Token efficiency** - Progressive disclosure minimizes context usage

## Marketplace Distribution

The skill is distributed via Claude Code plugin marketplace:

Installation command:
```
/plugin marketplace add c0webster/gam-expert-claude-skill
```

Marketplace metadata is in `.claude-plugin/marketplace.json`.

## Related Resources

- GAM7 project: https://github.com/GAM-team/GAM
- GAM wiki: https://github.com/GAM-team/GAM/wiki
- Claude Code docs: https://docs.claude.com/en/docs/claude-code
- Skill development guide: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
