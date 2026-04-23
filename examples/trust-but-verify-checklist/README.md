# PythonMuse Trust but Verify Checklist

Audit-friendly AI workflow checklist for accounting and finance teams.

---

## How to Use This Checklist

Use this before, during, and after working with AI on any accounting task:

- reconciliation
- payroll testing
- margin analysis
- audit support

If you can check every box, your workflow is controlled and reviewable.

Print it, paste it into Notion, attach it to a workpaper — use it however works for your team.

See [Article 13: AI in Accounting Isn't Just About Efficiency -- It's About Control](../../articles/13-zero-trust-ai-accounting/) for the full context.

---

## Section 1 -- Before Using AI: Data Control

- [ ] I am not using raw client or company data
- [ ] Sensitive fields (names, IDs, account numbers) are masked
- [ ] Dollar amounts are generalized or adjusted if needed
- [ ] I am only sharing the minimum data required
- [ ] I understand what data I am sending and where it is going

**If any box is unchecked -- stop here.**

Masking techniques are covered in [Article 06: How to Use AI in Accounting Without Sending the Wrong Data](../../articles/06-safe-ai-data-workflows/).

---

## Section 2 -- Define the Task: Do Not Let AI Guess

- [ ] I clearly described the task (reconcile, analyze variance, etc.)
- [ ] I asked AI to propose a plan before processing data
- [ ] I reviewed and approved the plan
- [ ] I confirmed assumptions and definitions

AI should not be deciding the approach on its own. This plan-first pattern is described in [Article 11: From One-Time Analysis to Repeatable Workflows](../../articles/11-one-time-to-repeatable-workflows/).

---

## Section 3 -- Processing: Controlled Execution

- [ ] Data provided matches the approved plan
- [ ] No additional or unintended data was included
- [ ] Steps performed by AI are clear and logical
- [ ] I can explain what AI is doing

**If you cannot explain it -- do not trust it.**

---

## Section 4 -- Output Review: Trust but Verify

- [ ] Results tie back to source data
- [ ] Calculations make sense independently of AI
- [ ] Any unusual items have been investigated
- [ ] Output is reviewed before sharing or posting

Clean output does not mean correct output.

---

## Section 5 -- Documentation: Make It Reproducible

- [ ] Inputs are saved (masked version)
- [ ] Outputs are saved in a defined location
- [ ] Steps are documented (`plan.md` or equivalent)
- [ ] Results can be recreated if needed
- [ ] Someone else could follow this process

**If it cannot be reproduced -- it is not audit-ready.**

The `plan.md` + `status_update.md` documentation pattern is described in [Article 08: Why Claude "Forgets"](../../articles/08-why-claude-forgets/). A starter template is available at [examples/ai-project-memory](../ai-project-memory/).

---

## Section 6 -- Final Check: Control Mindset

- [ ] I would be comfortable explaining this to an auditor
- [ ] I understand how the result was generated
- [ ] I did not rely solely on AI output
- [ ] The process follows trust but verify

---

## Quick Reference

| Section | Focus | Gate |
|---------|-------|------|
| 1. Before Using AI | Data Control | Stop if data is not masked |
| 2. Define the Task | Plan Before Processing | AI proposes, you approve |
| 3. Processing | Controlled Execution | You can explain every step |
| 4. Output Review | Trust but Verify | Results tie to source |
| 5. Documentation | Make It Reproducible | Someone else could repeat this |
| 6. Final Check | Control Mindset | You could explain it to an auditor |

---

## PythonMuse Reminder

AI in accounting should be:

- Controlled
- Repeatable
- Reviewable
- Explainable

Not:

- Ad hoc
- Opaque
- Dependent on a single chat session

---

*From [PythonMuse](https://github.com/PythonMuse/ai-ledger) -- Practical Python, AI, and automation for accounting and finance teams.*
