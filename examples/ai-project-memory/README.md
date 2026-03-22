# AI Project Memory Starter Template

A reusable folder structure for AI-assisted accounting projects that survive session resets.

---

## What This Is

When working with Claude on accounting workflows, long sessions can lose context -- and new sessions start with no memory of prior work. This template solves that problem with three simple Markdown files that act as your project's external memory.

See [Article 08: Why Claude "Forgets"](../../articles/08-why-claude-forgets/) for the full explanation.

---

## Structure

```
ai-project-memory/
  CLAUDE.md             instructions for Claude
  plan.md               project blueprint
  status_update.md      rolling progress tracker

  data/
    raw/                original source files (never modified)
    processed/          cleaned or transformed data

  src/                  scripts and logic files

  outputs/              generated reports and results

  docs/                 notes, memos, reference material
```

---

## How to Use

1. Copy this folder into your own project
2. Edit `plan.md` with your project objective, rules, and steps
3. Edit `CLAUDE.md` with any project-specific instructions
4. Start a Claude session and say: *"Read plan.md and status_update.md. Summarize current state and confirm next step."*

---

## The Three Memory Files

| File | Purpose | When to Update |
|------|---------|----------------|
| `plan.md` | Defines the project scope, rules, and steps | At project start; revise as scope changes |
| `status_update.md` | Tracks completed work, outputs, issues, next steps | After each major milestone |
| `CLAUDE.md` | Instructions for how Claude should behave | At project start; adjust as needed |

---

## Example Prompts

**Start a session:**
> Read plan.md and status_update.md. Summarize where we left off and what the next steps are.

**Save progress:**
> Update status_update.md with what was completed, output file locations, any issues, and next steps.

**End a session:**
> Before we stop, update status_update.md with a full summary of today's session.

---

*From [PythonMuse](https://github.com/PythonMuse/ai-ledger) -- Practical Python, AI, and automation for accounting and finance teams.*
