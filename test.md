# How I Use Claude Code Skills to Run My Personal Wiki

---
We are entering an era where AI assistants can integrate with our personal systems, not just cloud services with APIs, but local files, desktop applications, and the idiosyncratic workflows we have built over years.

Claude Code skills are one piece of this puzzle. They let you teach an AI about your specific environment, your file organization, your preferred formats, and your tools.

I have used Zim, a lightweight desktop wiki that stores everything as text files in markup format, for many years. I want to keep using it while taking advantage of the new capabilities Claude Code offers.

So I built a Claude Code skill that lets me create notes in my Zim wiki without ever leaving the command line.

## What Are Claude Code Skills?

Claude Code recently introduced skills, Markdown files that extend Claude’s capabilities within specific contexts. Think of them as reusable prompts with superpowers: they can request tool permissions, define workflows, and provide domain-specific instructions that Claude follows.

Skills live in:

~/.claude/commands/ for global availability

.claude/commands/ within a project for project-specific functionality

Once created, you invoke them with a simple slash command.

## Creating the Skill File

I even used Claude Code itself to help create the file for my `zim-note` skill.

The skill file (`~/.claude/commands/zim-note.md`) contains three key sections:

### 1. Tool Permissions

```yaml
---
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---
```

This grants Claude the minimum permissions needed to read existing notes, create new ones, and check directory structures.

### 2. Context and Configuration

The skill tells Claude where my notebook lives, how Zim organizes files, and the exact format Zim expects:

- **Journal entries**: `~/notebook/Journal/YYYY/MM/DD.txt`
- **Regular notes**: Spaces become underscores, stored in specified folders
- **Headers**: Three-line format with Content-Type, Wiki-Format, and Creation-Date

### 3. Workflow Logic

The skill includes branching logic:
- If it's a journal entry and one exists for that date, append a new section
- If it's a journal entry with no existing file, create with proper date heading
- If it's a regular note, transform the title and create in the specified folder

## The Zim Wiki Format

One challenge was teaching Claude the specific formatting Zim expects. The skill includes a reference table:

| Syntax | Purpose |
|--------|---------|
| `====== Title ======` | Level 1 heading (6 equals signs) |
| `**bold**` | Bold text |
| `//italic//` | Italic text |
| `[ ] task` | Unchecked checkbox |
| `[*] done` | Checked checkbox |
| `[[PageName]]` | Internal wiki link |

Code blocks use a special syntax:
```
{{{code: lang="python3" linenumbers="True"
def hello():
    print("Hello!")
}}}
```

## Creating the Skill File

Here is the complete skill file I created at `~/.claude/commands/zim-note.md`:

```markdown
---
description: Create a note in the Zim wiki notebook. Use for journal entries or general notes.
allowed-tools: Bash, Write, Read, Glob
---

# Zim Notebook Note Creator

Create notes in the user's Zim wiki notebook located at `~/notebook/`.

## Arguments

The user will provide: $ARGUMENTS

Parse the arguments to determine:
1. **Note type**: "journal" (default) or a specific folder path like "Stuff_to_try" or "Code_snippets"
2. **Title**: The note title or topic
3. **Content**: The actual note content

## Zim Wiki Format

**Journal entries** format:
\`\`\`
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.6
Creation-Date: YYYY-MM-DDTHH:MM:SS-08:00

====== DayName DD Mon YYYY ======

Content here...
\`\`\`

**Regular notes** format (includes "Created" line):
\`\`\`
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.6
Creation-Date: YYYY-MM-DDTHH:MM:SS-08:00

====== Note Title Here ======
Created DayName DD MonthName YYYY

Content here...
\`\`\`

## Formatting Reference

- **Headings**: `====== H1 ======`, `===== H2 =====`, `==== H3 ====`, `=== H4 ===`
- **Bold**: `**bold text**`
- **Italic**: `//italic text//`
- **Strikethrough**: `~~strikethrough~~`
- **Links**: `[[Page Name]]` or `[[Page Name|Display Text]]`
- **External links**: `https://example.com` (auto-linked)
- **Bullet lists**: `* item` (use tabs for nesting)
- **Numbered lists**: `1. item`
- **Checkboxes**: `[ ] unchecked`, `[*] checked`, `[x] crossed`
- **Code blocks**:
  \`\`\`
  {{{code: lang="python3" linenumbers="True"
  code here
  }}}
  \`\`\`
- **Inline code**: `''monospace''`

## File Paths

- **Journal entries**: `~/notebook/Journal/YYYY/MM/DD.txt`
  - Create parent directories if needed
  - Use current date if not specified
  - Title format: `====== DayName DD Mon YYYY ======` (e.g., "Tuesday 13 Jan 2026")

- **Regular notes**: `~/notebook/FolderName/NoteName.txt`
  - Replace spaces with underscores in filename (e.g., "My Note" → "My_Note.txt")
  - Replace commas with commas followed by underscores if needed
  - Also create `FolderName.txt` index file if the folder is new

## Workflow

1. Determine if this is a journal entry or a regular note
2. Generate the appropriate file path
3. Create any needed parent directories with `mkdir -p`
4. **For journal entries**: Check if file exists
   - If exists: Read current content and append new content under a new subheading
   - If new: Create with proper header and title
5. **For regular notes**: Create new file with proper header, title, and "Created" line
6. Write the file
7. Confirm creation to the user with the full path

## Examples

**Journal entry for today:**
\`\`\`
/zim-note Had a productive meeting about the ML pipeline
\`\`\`
Creates `~/notebook/Journal/2026/01/15.txt`

**Note in specific folder:**
\`\`\`
/zim-note folder:Code_snippets Python decorator for timing functions
\`\`\`
Creates `~/notebook/Code_snippets/Python_decorator_for_timing_functions.txt`

**Journal with specific date:**
\`\`\`
/zim-note date:2026-01-10 Remembered something from last week
\`\`\`
Creates `~/notebook/Journal/2026/01/10.txt`

**Append to existing journal (if today's entry exists):**
\`\`\`
/zim-note Another thought to add to today's journal
\`\`\`
Appends a new section to existing `~/notebook/Journal/2026/01/15.txt`
```

## New claude code command: `/zim-note`

After restarting Claude Code, a new command `/zim-note` is available.

Now I can ask claude to create a note like this:

```bash
/zim-note Document the /zim-note skill in todays note
```

Claude creates a properly formatted journal entry for today, complete with Zim headers and timestamps. If an entry already exists, it appends instead of overwriting.

For topical notes, I can specify a folder:

```bash
/zim-note folder:Code_snippets Python decorator for timing functions
```

Or for a specific date:
```bash
/zim-note date:2026-01-10 Remembered something from last week
```

---

## Conclusion
The new /zim-note command significantly streamlines the process of capturing thoughts, meeting notes, and technical ideas directly into my Zim-based knowledge system. By supporting natural-language commands for dates, folders, and appending behavior, it bridges the gap between quick idea capture and structured note-taking.

The result is a workflow that is faster, more consistent, and far better aligned with how I already think and work.

---

**Tags**: #AI #Productivity #NoteTaking #ClaudeCode #PersonalKnowledgeManagement
