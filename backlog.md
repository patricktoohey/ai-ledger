# Backlog — Article 07 + Companion Repo

Source material: `StatusUpdate.md` lines 112–2463 + `docs/To review/`
Last updated: 2026-03-16

---

## Status: Phase 1 COMPLETE — Article 07 published

---

## Phase 1: Article 07 in ai-ledger

**Status: COMPLETE**

**Goal:** Publish `articles/07-ai-governance-for-controllers/README.md` in PythonMuse standard format.

### Task 1.1 — Write Article 07 README.md
- Source: ChatGPT article draft (StatusUpdate.md lines 1395–1607)
- Apply PythonMuse standard format:
  - `# Title` + `*italic subtitle*` + `---` + `**By Svetlana Toohey**` + `*Published March 2026*`
  - Section separators with `---`
  - No bottom byline
  - `*Related:` footer with 2–4 links (articles 04, 05, 06 are natural fits)
- Tone pass: slightly soften academic phrasing to match Svetlana's practical, conversational voice
- Add image references for visuals (placeholders until 1.2 is done)
- **Can run as subagent:** Yes — self-contained write task

### Task 1.2 — Generate Article 07 Visuals
- Create `articles/07-ai-governance-for-controllers/generate_visuals.py`
- Produce 3 PNGs in `./visuals/`:
  - `07_visual_front.png` — hero/header graphic
  - `07_governance_flow.png` — Policy → Inventory → Risk → Controls → Skills → Agents → Evidence
  - `07_repo_architecture.png` — the folder structure diagram
- Follow naming convention: `07_snake_case.png`
- Style: match existing PythonMuse visuals (matplotlib, clean, professional)
- **Can run as subagent:** Yes — independent of 1.1 content (just needs titles/concepts)

### Task 1.3 — Update Root README.md
- Add row for Article 07 in the article index table
- Format: `| 07 | [AI Governance for Controllers](articles/07-ai-governance-for-controllers/) | COSO, governance, controls, skills, agents, VS Code |`
- **Can run as subagent:** No — quick edit, do inline

### Task 1.4 — Update Cross-References
- Add Article 07 to Related links in articles 04, 05, 06 (where appropriate, max 4 links per article)
- **Can run as subagent:** No — quick edits, do inline

### Task 1.5 — Review & Publish
- Run `/publish-article` skill to audit against checklist
- Verify all image paths resolve
- Commit and push

---

## Phase 2: Companion Repo — finance-ai-governance (SEPARATE SESSION)

**Goal:** Create `PythonMuse/finance-ai-governance` GitHub repo with full starter governance structure.

> This is a **separate repo**, not a folder in ai-ledger.
> Defer to a future session to avoid context overload.

### Task 2.1 — Create repo structure
```
finance-ai-governance/
├── README.md
├── CLAUDE.md
├── docs/
│   ├── ai-policy.md
│   ├── data-classification.md
│   ├── approved-use-cases.md
│   ├── risk-methodology.md
│   ├── control-matrix.md
│   ├── review-and-signoff.md
│   └── change-management.md
├── inventory/
│   ├── genai-use-case-register.md
│   └── genai-use-case-register.csv
├── assessments/
│   ├── UC-001-bank-rec-risk.md
│   └── templates/
│       ├── risk-template.md
│       └── control-template.md
├── toolkit/
│   ├── controller-ai-governance-toolkit.md
│   ├── controller-implementation-checklist.md
│   ├── genai-use-case-register-template.csv
│   ├── risk-assessment-template.md
│   └── finance-ai-skill-template.md
├── skills/
│   ├── bank-rec-review/SKILL.md
│   └── variance-analysis/SKILL.md
├── agents/
│   └── reconciliations-agent.md
├── examples/
│   ├── sample-bank-reconciliation.md
│   └── demo-data/
│       ├── README.md
│       ├── bank_statement_masked.csv
│       ├── gl_cash_activity.csv
│       └── variance_demo_pnl.csv
├── evidence/
│   ├── run-logs/
│   ├── review-notes/
│   └── testing/
└── .claude/
    └── settings.json
```

### Task 2.2 — Write all markdown files
- Source: StatusUpdate.md lines 640–2463 + `docs/To review/` files
- Apply consistent tone (practical, controller-friendly)

### Task 2.3 — Write repo README with Mermaid diagram
- Source: `docs/To review/github-readme-diagram-mermaid.md`

### Task 2.4 — Write CLAUDE.md with controller operating rules
- Source: StatusUpdate.md lines 286–310

### Task 2.5 — Create GitHub repo and push
- `gh repo create PythonMuse/finance-ai-governance --public`
- Push all files
- Update Article 07 links to point to live repo

---

## Execution Plan for This Session

**Focus: Phase 1 only (Article 07)**

| Step | Task | Method | Parallel? |
|------|------|--------|-----------|
| 1 | Write Article 07 README.md | Subagent (write) | Yes |
| 2 | Generate visuals script | Subagent (write) | Yes, with Step 1 |
| 3 | Run generate_visuals.py | Bash | After Step 2 |
| 4 | Update root README.md | Inline edit | After Step 1 |
| 5 | Update cross-references | Inline edits | After Step 1 |
| 6 | Run /publish-article | Skill | After all above |
| 7 | Commit and push | Inline | After Step 6 |

Phase 2 deferred to a later session to keep context clean.

---

## Restart Instructions

> **Next session prompt:** "Read backlog.md and execute Phase 1 — Article 07. Run Tasks 1.1 and 1.2 as parallel subagents, then do 1.3–1.5 inline."

### What Claude needs to know on restart

1. **MEMORY.md** has project standards (byline, format, article index)
2. **backlog.md** (this file) has the full plan and source references
3. **StatusUpdate.md lines 1395–1607** has the ChatGPT article draft to adapt
4. **docs/To review/** has visuals and data files from ChatGPT
5. **Existing visuals pattern:** `generate_visuals.py` in article folder produces PNGs to `./visuals/07_name.png`, referenced as `![Alt](./visuals/07_name.png)` with `*Figure: caption*` on next line
6. **Existing article for style reference:** `articles/06-safe-ai-data-workflows/README.md` is the most recent standard-format article

### Subagent breakdown to avoid context crashes

| Subagent | Task | Input | Output |
|----------|------|-------|--------|
| **Agent A** | Write Article 07 README.md | StatusUpdate.md lines 1395–1607, MEMORY.md format rules, article 06 for tone reference | `articles/07-ai-governance-for-controllers/README.md` |
| **Agent B** | Write generate_visuals.py | Existing scripts (article 04 or 06) for style, 3 visual concepts from backlog Task 1.2 | `articles/07-ai-governance-for-controllers/generate_visuals.py` |
| **Main thread** | After agents complete: run visuals script, update root README, update cross-refs, run /publish-article, commit | Agent outputs | Published article |

---

## Files consumed from ChatGPT (docs/To review/)

| File | Used in |
|------|---------|
| `SKILL.md` | Phase 2 — variance-analysis skill |
| `sample-bank-reconciliation-example.md` | Phase 2 — examples/ |
| `bank_statement_masked.csv` | Phase 2 — demo-data/ |
| `gl_cash_activity.csv` | Phase 2 — demo-data/ |
| `variance_demo_pnl.csv` | Phase 2 — demo-data/ |
| `README.md` | Phase 2 — demo-data README |
| `github-readme-diagram-mermaid.md` | Phase 2 — repo README |
| `github-readme-diagram.png` | Phase 2 — repo README (fallback) |
| Duplicate `(1)` files | Ignore — same content |
