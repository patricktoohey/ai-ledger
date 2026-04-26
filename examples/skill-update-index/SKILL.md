---
name: update-index
description: Audit articles/index.md against all README.md files in the articles/ directory and update the index table to include every article, in order, with accurate title and topic tags.
---

# Purpose

This skill keeps the site index current.

It is designed to:
- scan all subdirectories inside `articles/` for `README.md` files
- extract the article number (from the folder name), title (from the first `#` heading), and key topics
- compare what exists on disk to what is listed in `articles/index.md`
- add any missing rows to the index table in the correct sorted position
- flag any index rows whose folder no longer exists on disk

This skill is **assistive only**.

It does **not** rewrite article content, change article titles, or modify the site navigation in `mkdocs.yml`.

---

# Allowed Inputs

- `articles/` directory tree (read-only scan)
- `articles/index.md` (read + write)
- `mkdocs.yml` (read-only, for cross-reference)

---

# Required Working Method

1. Glob `articles/**/README.md` to get the full list of articles on disk.
2. For each result, extract:
   - **Article number** — from the folder name prefix (e.g., `10`, `17b`)
   - **Title** — from the first `# ` heading in the file
   - **Topics** — a short comma-separated phrase list inferred from the article's subtitle, opening paragraph, or section headings (2–5 terms)
   - **Relative path** — from the `articles/` root (e.g., `10-ai-use-cases-and-structure/README.md`)
3. Read `articles/index.md` and parse the existing table rows.
4. Identify:
   - articles on disk **not in the index** (missing rows)
   - index rows whose folder **does not exist** on disk (stale rows)
5. Insert missing rows into the table in sorted order by article number. Use the same Markdown table format as existing rows.
6. Report stale rows to the user but do **not** delete them without confirmation.
7. Write the updated `articles/index.md`.
8. Print a confirmation summary.

---

# Output Format

After editing the file, return:

## Index Update Summary

**Articles found on disk:** N  
**Articles already in index:** N  
**Rows added:** N  
**Stale rows flagged (folder missing):** N  

### Added
- list each added row with article number and title

### Stale (not removed — confirm before deleting)
- list each stale row, if any

### Final index table
Paste the complete updated table.

---

# Example Invocation

"Use the update-index skill to sync articles/index.md with everything in the articles/ folder."

---

# Human Review

Spot-check that:
- article numbers are sorted correctly (00, 00.5, 01 … 17, 17b, 21)
- titles match the actual `# ` heading in each README
- topic tags are accurate and consistent in length with surrounding rows
- no articles were accidentally omitted or duplicated
