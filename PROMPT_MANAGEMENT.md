# Prompt Management Guide

## Overview

This system uses **file-based prompt storage** for easy editing and version control.

### Key Benefits

✅ **Easy to edit** - Just edit .txt files, no JSON formatting needed
✅ **Git-friendly** - Clean diffs, no escaping issues
✅ **97.5% smaller versions.json** - From 96KB → 2.4KB
✅ **Syntax highlighting** - IDEs recognize .txt files properly
✅ **No code needed** - Direct file edits automatically work

---

## File Structure

```
data/prompts/
├── versions.json                    # Metadata only (version numbers, dates, file paths)
├── primary_agent_v1.txt             # Prompt files
├── primary_agent_v2.txt
├── primary_agent_v3.txt             # ← Currently active (improved)
├── challenge_agent_v1.txt
├── challenge_agent_v2.txt
├── challenge_agent_v3.txt           # ← Currently active (improved)
├── decision_agent_v1.txt
├── decision_agent_v2.txt
├── decision_agent_v3.txt
├── decision_agent_v4.txt            # ← Currently active (improved)
└── versions_backup_*.json           # Backup of old embedded system
```

---

## How to Edit Prompts

### Option 1: Edit Active Version (Quick & Easy)

1. **Find the active prompt file:**
   - Primary Agent: `data/prompts/primary_agent_v3.txt`
   - Challenge Agent: `data/prompts/challenge_agent_v3.txt`
   - Decision Agent: `data/prompts/decision_agent_v4.txt`

2. **Edit the file directly** in any text editor

3. **That's it!** Changes take effect immediately on next evaluation

### Option 2: Create New Version (Recommended for Major Changes)

```python
from src.prompts.manager import PromptManager

pm = PromptManager()

# Read your updated prompt
with open('my_improved_prompt.txt', 'r', encoding='utf-8') as f:
    new_content = f.read()

# Save as new version
new_version = pm.save_new_version(
    prompt_type="primary_agent",
    content=new_content,
    notes="Description of changes",
    set_active=True  # Set to True to activate immediately
)

print(f"Created version {new_version}")
```

### Option 3: Switch Between Existing Versions

```python
from src.prompts.manager import PromptManager

pm = PromptManager()

# Activate a specific version
pm.set_active_version("primary_agent", "2")  # Roll back to v2
pm.set_active_version("primary_agent", "3")  # Back to improved v3
```

---

## Current Active Versions

| Agent | Active Version | File | Notes |
|-------|----------------|------|-------|
| **Primary Agent** | v3 | `primary_agent_v3.txt` | Improved: Removed hardcoded scoring, ~40% shorter output |
| **Challenge Agent** | v3 | `challenge_agent_v3.txt` | Improved: Streamlined format, ~35% shorter output |
| **Decision Agent** | v4 | `decision_agent_v4.txt` | Improved: Consolidated sections, ~20% shorter output |

---

## Quick Commands

### Activate Improved Versions (All Agents)

```bash
python activate_improved_prompts.py
```

### Check Active Versions

```python
from src.prompts.manager import PromptManager
pm = PromptManager()

data = pm._load_versions()
for agent_type in ["primary_agent", "challenge_agent", "decision_agent"]:
    active = data[agent_type]["active_version"]
    print(f"{agent_type}: v{active}")
```

### View Version History

```python
from src.prompts.manager import PromptManager
pm = PromptManager()

versions = pm.get_all_versions("primary_agent")
for v in versions:
    print(f"v{v['version']} - {v['notes']}")
```

---

## Version Control with Git

### Tracking Prompt Changes

Prompts are now perfect for git:

```bash
# See what changed in prompts
git diff data/prompts/*.txt

# Commit prompt changes
git add data/prompts/primary_agent_v3.txt
git commit -m "Improve primary agent prompt: remove hardcoded scoring"

# Track version metadata changes
git add data/prompts/versions.json
git commit -m "Activate improved prompts v3/v3/v4"
```

### Example Git Diff

Before (embedded in JSON):
```diff
- "content": "You are an evaluator...\\n\\n## SCORING\\n\\nUse 1-5...\"
+ "content": "You are an evaluator...\\n\\n## SCORING\\n\\nUse scale from rubric...\"
```

After (file-based):
```diff
--- a/data/prompts/primary_agent_v3.txt
+++ b/data/prompts/primary_agent_v3.txt
@@ -21,17 +21,11 @@
 ## SCORING CALIBRATION

-Use the scoring scale provided in the rubric. If evaluating a level transition, calibrate scores relative to Current → Target level:
-
-**Lower scores (1-2):**
-...
+Use the scoring scale and definitions provided in the rubric. The rubric defines:
+- What scale to use (1-5, 1-4, Pass/Fail, etc.)
```

Much cleaner!

---

## Backup & Recovery

### Automatic Backup

The migration created a backup:
- `data/prompts/versions_backup_20260109_114043.json`

This contains the original embedded prompts in case you need to revert.

### Manual Backup

```bash
# Backup all prompts
cp -r data/prompts data/prompts_backup_$(date +%Y%m%d)

# Restore from backup
cp -r data/prompts_backup_20260109/* data/prompts/
```

---

## Architecture Details

### Old System (Embedded)

```json
{
  "primary_agent": {
    "active_version": "2",
    "versions": [
      {
        "version": "2",
        "content": "9,243 characters of prompt text embedded here..."
      }
    ]
  }
}
```

**Problems:**
- ❌ Hard to edit (JSON escaping)
- ❌ Poor git diffs (escaping changes)
- ❌ No syntax highlighting
- ❌ 96KB file size

### New System (File-Based)

**versions.json** (2.4KB - just metadata):
```json
{
  "primary_agent": {
    "active_version": "3",
    "versions": [
      {
        "version": "3",
        "created_at": "2026-01-09T11:40:43",
        "notes": "Improved version",
        "file": "primary_agent_v3.txt"
      }
    ]
  }
}
```

**primary_agent_v3.txt**:
```
You are an experienced evaluator conducting a comprehensive assessment...

## SCORING CALIBRATION

Use the scoring scale and definitions provided in the rubric...
```

**Benefits:**
- ✅ Easy to edit
- ✅ Clean git diffs
- ✅ Syntax highlighting
- ✅ 97.5% smaller metadata

---

## API Reference

### PromptManager Methods

```python
from src.prompts.manager import PromptManager
pm = PromptManager()

# Get active prompt content
content = pm.get_active_prompt("primary_agent")

# Get all version metadata (without content)
versions = pm.get_all_versions("primary_agent")

# Get specific version with content
version = pm.get_version("primary_agent", "2")
print(version["content"])

# Save new version
new_version = pm.save_new_version(
    prompt_type="primary_agent",
    content="...",
    notes="Description",
    set_active=True
)

# Switch active version
pm.set_active_version("primary_agent", "2")

# Update existing version content
pm.update_prompt_content("primary_agent", "3", "new content...")

# Delete version (cannot delete active)
pm.delete_version("primary_agent", "1", delete_file=True)
```

---

## Troubleshooting

### Prompt not found error

```
FileNotFoundError: Prompt file not found: data/prompts/primary_agent_v3.txt
```

**Solution:** The file is missing. Check versions.json and ensure file exists.

### Changes not taking effect

**Solution:** Make sure you edited the ACTIVE version. Check `versions.json` to see which version is active.

### Want to revert changes

**Option 1:** Edit the file back to previous content

**Option 2:** Switch to previous version:
```python
pm.set_active_version("primary_agent", "2")
```

**Option 3:** Restore from backup:
```bash
cp data/prompts/versions_backup_*.json data/prompts/versions.json
```

---

## Best Practices

1. **Test changes on sample evaluations** before deploying to production

2. **Create new versions for major changes** rather than editing active version directly

3. **Use descriptive notes** when creating versions:
   ```python
   notes="Fix rubric alignment issues in scoring section"
   ```

4. **Commit prompts to git** with meaningful commit messages:
   ```bash
   git commit -m "Improve challenge agent: streamline output format"
   ```

5. **Keep old versions** for rollback capability (don't delete unless disk space is critical)

---

## Migration Notes

**From Embedded System:**
- Original versions.json backed up to `versions_backup_*.json`
- All prompts extracted to separate .txt files
- versions.json reduced from 96KB → 2.4KB (97.5% reduction)
- All version history preserved
- Improved prompts added as v3/v3/v4

**No Breaking Changes:**
- Same PromptManager API
- Same behavior
- Same evaluation flow
- Just better storage format
