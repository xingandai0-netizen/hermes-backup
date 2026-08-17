---
name: apple-productivity
description: "Apple productivity apps via CLI: Notes (memo), Reminders (remindctl). macOS-only, iCloud-synced."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Apple, macOS, Notes, Reminders, productivity, CLI, iCloud]
    related_skills: [obsidian]
---

# Apple Productivity

Manage Apple Notes and Reminders from the terminal. Both sync across all Apple devices via iCloud.

## When to Use

- User asks to create, view, or search Apple Notes
- User mentions "reminder" or "Reminders app"
- Saving information to Notes.app for cross-device access
- Creating personal to-dos with due dates that sync to iOS
- User wants tasks to appear on their iPhone/iPad

## When NOT to Use

- Obsidian vault management → use the `obsidian` skill
- Scheduling agent alerts → use the `cronjob` tool instead
- Calendar events → use Apple Calendar or Google Calendar
- Project task management → use GitHub Issues, Notion, etc.
- Quick agent-only notes → use the `memory` tool instead
- If user says "remind me" but means an agent alert → clarify first

---

## Section: Apple Notes (memo CLI)

### Prerequisites

- **macOS** with Notes.app
- Install: `brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- Grant Automation access to Notes.app when prompted (System Settings → Privacy → Automation)

### Quick Reference

```bash
memo notes                        # List all notes
memo notes -f "Folder Name"       # Filter by folder
memo notes -s "query"             # Search notes (fuzzy)
memo notes -a                     # Interactive editor
memo notes -a "Note Title"        # Quick add with title
memo notes -e                     # Interactive selection to edit
memo notes -d                     # Interactive selection to delete
memo notes -m                     # Move note to folder (interactive)
memo notes -ex                    # Export to HTML/Markdown
```

### Limitations

- Cannot edit notes containing images or attachments
- Interactive prompts require terminal access (use pty=true if needed)

### Fallback: AppleScript (when memo not installed)

If `memo` is not installed (brew fails, network issues, etc.), use osascript directly:

**Step 1: Discover available accounts** (CRITICAL — don't assume "iCloud")
```bash
osascript -e 'tell application "Notes" to get name of every account'
```
Common account names: "iCloud", "我的Mac", "谷歌" (Google), or custom names.

**Step 2: Create note via AppleScript**
```bash
osascript -e '
tell application "Notes"
    tell account "ACCOUNT_NAME_HERE"
        make new note with properties {name:"NOTE_TITLE", body:"NOTE_CONTENT"}
    end tell
end tell
'
```

**Pitfall**: If you guess the account name wrong (e.g. assume "iCloud" when it's "我的Mac"), you get error `-1728: cannot get account`. Always run Step 1 first.

**Pitfall**: The `body` property uses basic text only — no rich formatting. For formatted content, use HTML body instead:
```bash
osascript -e '
tell application "Notes"
    tell account "我的Mac"
        make new note with properties {name:"Title", body:"<h1>Title</h1><p>Content with <b>bold</b></p>"}
    end tell
end tell
'
```

**Opening a specific note**:
```bash
osascript -e '
tell application "Notes"
    activate
    set theNote to note "NOTE_TITLE"
    show theNote
end tell
'
```

**Pitfall — `computer_use` screen capture fails on Notes app**: The screen capture tool returns black/empty when Notes is the active app. Workaround: use `screencapture -x /tmp/shot.png` + `vision_analyze` to verify note content visually.

**Limitation**: AppleScript can create notes but cannot search, list, or edit existing notes easily. For those operations, install memo CLI.

### Rules

1. Prefer Apple Notes when user wants cross-device sync (iPhone/iPad/Mac)
2. Use the `memory` tool for agent-internal notes that don't need to sync
3. Use the `obsidian` skill for Markdown-native knowledge management

---

## Section: Apple Reminders (remindctl CLI)

### Prerequisites

- **macOS** with Reminders.app
- Install: `brew install steipete/tap/remindctl`
- Grant Reminders permission when prompted
- Check: `remindctl status` / Request: `remindctl authorize`

### Quick Reference

#### View Reminders

```bash
remindctl                    # Today's reminders
remindctl today              # Today
remindctl tomorrow           # Tomorrow
remindctl week               # This week
remindctl overdue            # Past due
remindctl all                # Everything
remindctl 2026-01-04         # Specific date
```

#### Manage Lists

```bash
remindctl list               # List all lists
remindctl list Work          # Show specific list
remindctl list Projects --create    # Create list
remindctl list Work --delete        # Delete list
```

#### Create Reminders

```bash
remindctl add "Buy milk"
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Meeting prep" --due "2026-02-15 09:00"
```

#### Due Time vs Alarm / Early Nudge

`--due` and `--alarm` are different fields:

- `--due` sets the reminder's due date/time.
- `--alarm` sets the EventKit alarm/notification trigger.

For a reminder due at 2:00 PM with a notification 30 minutes earlier:

```bash
remindctl add --title "Hairdresser" --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
```

Verify with JSON instead of assuming the due time moved:

```bash
remindctl today --json
```

Expected shape: `dueDate` (actual due time), `alarmDate` (notification time).

#### Complete / Delete

```bash
remindctl complete 1 2 3          # Complete by ID
remindctl delete 4A83 --force     # Delete by ID
```

#### Output Formats

```bash
remindctl today --json       # JSON for scripting
remindctl today --plain      # TSV format
remindctl today --quiet      # Counts only
```

### Date Formats

Accepted by `--due` and date filters:
- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 (`2026-01-04T12:34:56Z`)

### Rules

1. When user says "remind me", clarify: Apple Reminders (syncs to phone) vs agent cronjob alert
2. Always confirm reminder content and due date before creating
3. Use `--json` for programmatic parsing
