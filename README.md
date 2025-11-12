# GAM Expert - Claude Code Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue.svg)](https://claude.ai/code)
[![GAM7](https://img.shields.io/badge/GAM-7-green.svg)](https://github.com/GAM-team/GAM)

> A comprehensive Claude Code skill for managing Google Workspace using GAM7

## What is This?

GAM Expert is a Claude Code skill that provides expert-level assistance with GAM (Google Apps Manager) commands for Google Workspace administration. It combines Claude's natural language understanding with GAM's powerful command-line capabilities to help you manage your Google Workspace domain efficiently and safely.

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

1. **Construct proper GAM commands** by consulting comprehensive reference documentation
2. **Process CSV files** for bulk operations when needed
3. **Execute commands safely** by always confirming before destructive operations
4. **Troubleshoot errors** by analyzing output and suggesting fixes
5. **Analyze results** by parsing GAM output and generating reports

## Prerequisites

- **Claude Code** must be installed ([Installation Guide](https://docs.claude.com/en/docs/claude-code))
- **GAM7** must be installed and configured on your system
  - Verify with: `gam version`
  - Installation: https://github.com/GAM-team/GAM
- GAM must be authenticated with your Google Workspace domain

## Installation

### Claude Code (Recommended)

You can register this repository as a Claude Code Plugin marketplace by running the following command in Claude Code:

```
/plugin marketplace add c0webster/gam-expert-claude-skill
```

Then, to install the GAM Expert skill:

1. Select **Browse and install plugins**
2. Select **gam-expert-claude-skill**
3. Select **gam-expert**
4. Select **Install now**

Alternatively, directly install the plugin via:

```
/plugin install gam-expert@gam-expert-claude-skill
```

After installing the plugin, you can use the skill by just mentioning GAM or Google Workspace tasks. For example: "Help me list all users in the Marketing OU using GAM"

### Manual Installation from GitHub

If you prefer to install manually:

#### Clone the Repository

```bash
git clone https://github.com/c0webster/gam-expert-claude-skill.git
cd gam-expert-claude-skill
```

#### Install the Skill

```bash
cp -r gam-expert ~/.claude/skills/
```

#### Verify Installation

Start Claude Code and simply ask about GAM or Google Workspace:
```bash
claude
```

Then ask naturally:
```
"Help me list all users in the Marketing OU using GAM"
```

Claude will automatically invoke the GAM Expert skill when you ask about Google Workspace administration tasks.

### Claude.ai

You can use this skill in Claude.ai by uploading it as a ZIP file:

1. Create a ZIP file of the `gam-expert` folder:
   ```bash
   cd gam-expert-claude-skill
   zip -r gam-expert.zip gam-expert/
   ```

2. In Claude.ai, go to **Settings > Capabilities**

3. Ensure **Code execution and file creation** is enabled

4. Scroll to the **Skills** section and click **Upload skill**

5. Upload the `gam-expert.zip` file

**Requirements:**
- Available on Pro, Max, Team, and Enterprise plans
- Code execution must be enabled
- Custom skills are private to your individual account

For detailed instructions, see [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### Claude API

You can use custom skills via the Claude API. See the [Agent Skills API Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart) for implementation details.

## How It Works

This is a **Claude Code skill** - Claude automatically detects when you need GAM assistance and invokes the skill for you. You don't need to use any special commands; just describe what you want to do naturally.

## Quick Start

Simply describe what you want to do with Google Workspace in natural language:

### User Management
```
"List all users in the Marketing OU"
"Create a new user account for john@example.com"
"Suspend the users listed in terminated.csv"
```

### Group Management
```
"Create a new group called team@example.com"
"Add all users from users.csv to the sales@example.com group"
"Show me all members of the executive@example.com group"
```

### Drive Management
```
"List all files owned by alice@example.com"
"Generate a report of who has access to the Shared Drive"
"Transfer ownership of all files from old.user@example.com to new.user@example.com"
```

### Bulk Operations
```
"Update all users in the CSV file with their new OUs"
"Create groups from the list in groups.csv with the specified settings"
"Export all group memberships to a spreadsheet for audit"
```

## Safety Features

The skill includes multiple safety mechanisms:

1. **Confirmation prompts** for all destructive operations
2. **Preview mode** - uses `gam print` commands to show what will happen
3. **Data validation** - checks CSV files before using them
4. **Documentation-first approach** - consults reference docs before executing
5. **Error recovery** - suggests fixes when commands fail

## Skill Components

### Core Files
- **SKILL.md** - Main skill instructions with comprehensive workflow
- **EXAMPLES.md** - Detailed use case examples
- **README.md** - Installation and usage guide

### Reference Documentation (6 guides)
- **quick_reference.md** - Common commands cheat sheet
- **command_syntax.md** - GAM command structure
- **common_patterns.md** - Frequently used patterns
- **safety_checklist.md** - Pre-execution safety checks
- **api_scopes.md** - OAuth scope requirements
- **troubleshooting.md** - Common issues and solutions

### Complete GAM Wiki (165 pages, bundled)
- **wiki/** - Full GAM documentation for offline access (4MB)
- Loaded progressively only when needed
- Covers all GAM functionality comprehensively

## Common Workflows

### 1. Simple Read Operation
User asks → Skill reads docs → Constructs command → Executes → Reports results

### 2. Bulk Operation with CSV
User provides CSV → Skill validates file → Constructs command → **Confirms with user** → Executes → Reports results

### 3. Complex Multi-Step Operation
User describes goal → Skill breaks into steps → **Confirms plan** → Executes each step → **Confirms before destructive steps** → Reports results

## Documentation

For detailed documentation, see:
- [Skill README](gam-expert/README.md) - Complete usage guide
- [Examples](gam-expert/EXAMPLES.md) - Detailed use cases
- [Official GAM Wiki](https://github.com/GAM-team/GAM/wiki) - Complete GAM documentation

## Troubleshooting

### "Command not found: gam"
- Ensure GAM7 is installed: https://github.com/GAM-team/GAM
- Check your PATH includes the GAM directory
- Try providing full path to gam executable

### Authentication Errors
- Run `gam oauth create` to re-authenticate
- Check that oauth2.txt exists in your GAM config directory
- Verify service account is properly authorized

### Permission Errors
- Ensure you have admin privileges for the operation
- Check API scopes are properly configured
- May need to re-run `gam oauth create` with additional scopes

## Tips for Best Results

1. **Be specific** - Include email addresses, group names, OU paths
2. **Provide context** - Mention if you're working with a CSV file
3. **Ask questions** - The skill will explain what commands do
4. **Review before confirming** - Always check the command before approving
5. **Start small** - Test with 1-2 items before bulk operations

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Links

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [GAM GitHub Repository](https://github.com/GAM-team/GAM)
- [GAM Wiki](https://github.com/GAM-team/GAM/wiki)
- [GAM Google Group](https://groups.google.com/group/google-apps-manager)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

GAM itself is maintained by Jay Lee and Ross Scroggs and is licensed separately.

## Acknowledgments

- GAM7 project by Jay Lee and Ross Scroggs
- Claude Code by Anthropic
- The Google Workspace admin community
