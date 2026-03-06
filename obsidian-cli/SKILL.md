---
name: obsidian-cli
description: Control Obsidian from terminal - create notes, append content, search, manage tasks
metadata:
  openclaw:
    requires:
      bins: ["obsidian"]
---

# Obsidian CLI Skill

Control Obsidian from terminal for automation and integration.

## Prerequisites

1. Obsidian 1.12.4+ installed
2. Enable CLI in Obsidian: Settings → General → Command line interface
3. Obsidian app must be running

## Common Commands

### Daily Notes
```bash
# Open today's daily note
obsidian daily

# Append to daily note
obsidian daily:append content="- [ ] New task"

# Prepend to daily note
obsidian daily:prepend content="# Important"
```

### Create & Edit Files
```bash
# Create new note
obsidian create name="Note Name" content="# Title\n\nContent"

# Create from template
obsidian create name="Meeting" template=Meeting

# Append to file
obsidian append file=README content="\n## New Section"

# Read file content
obsidian read file=README
```

### Search
```bash
# Search vault
obsidian search query="meeting notes"

# Search with context
obsidian search:context query="TODO"
```

### Tasks
```bash
# List all tasks
obsidian tasks

# List tasks from daily note
obsidian tasks daily

# Mark task as done
obsidian task file=README line=5 done
```

### Properties
```bash
# Set property
obsidian property:set name=status value=done file=README

# Read property
obsidian property:read name=status file=README
```

## Vault Targeting

```bash
# Target specific vault
obsidian vault="My Vault" daily

# Target by path (if cwd is vault folder, auto-detected)
obsidian daily
```

## Output Options

```bash
# Copy output to clipboard
obsidian read --copy

# JSON format
obsidian tasks format=json
```

## WSL Notes

Since Obsidian runs on Windows, WSL needs special handling:
- Use `obsidian.exe` or create alias
- Or use Windows path: `/mnt/c/Users/.../Obsidian.exe`

## Integration Examples

### Auto-append to daily note
```bash
# Add completion to daily note
obsidian daily:append content="✅ Completed task at $(date)"
```

### Create project document
```bash
obsidian create path="项目/新项目/需求文档.md" content="# 需求\n\n## 功能\n- 功能1\n- 功能2"
```
