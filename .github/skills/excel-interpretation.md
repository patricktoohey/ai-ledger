---
name: excel-interpretation
description: Interpret complex multi-tab Excel workbooks by providing AI with a structured instruction layer for the file layout, tab roles, and analysis rules
---

# Approved Use Case

Use Case ID: UC-004

---

# Purpose

This skill teaches AI how to read and interpret a specific complex Excel workbook.

It is designed to:
- document which tabs contain source data vs. summaries vs. visuals
- define rules for which data to trust and which to recalculate
- map column layouts so AI reads the correct fields
- specify supported analyses that can be performed from the source data
- eliminate misinterpretation caused by pivot tables, merged cells, and dashboard formatting

This skill is **assistive only**.

It does **not** replace human review of analysis results or authorize any posting, adjustment, or reporting action.

---

# When to Use This Skill

Use this skill when:
- an Excel workbook has multiple tabs with different purposes (data, summaries, dashboards)
- AI needs to know which tab is the source of truth
- pivot tables or formatted summaries exist that could mislead AI
- the same workbook structure is reused monthly or quarterly

Create one Skill per workbook type. Reuse it every period.

---

# Allowed Inputs

Use only approved source files such as:

- the Excel workbook matching this Skill's documented structure
- masked or sample versions of the workbook for testing
- prior period versions of the same workbook (for trend analysis)

All files should be located in the approved project directory (e.g., `/data/raw/`).

---

# Prohibited Inputs

Never process:

- real employee names, SSNs, or tax IDs (must be masked)
- bank account numbers or routing numbers
- login credentials or tokens
- unmasked customer PII in production data
- files outside the approved project directory

If prohibited data is detected, stop and ask for a masked or approved version.

---

# File Structure Map

Document each tab's role clearly. This section is the core of the Skill.

## Tab: Raw_Data

- **Role**: Source of truth -- transaction-level detail
- **Use**: Primary data source for all analyses
- **Layout**: Row 1 = headers, data starts row 2
- **Columns**:
  - A = Date (MM/DD/YYYY)
  - B = Department
  - C = Category
  - D = Vendor
  - E = Description
  - F = Amount (USD, always positive for expenses)
  - G = GL Account (4-digit code)

## Tab: Pivot_Summary

- **Role**: Validation reference only
- **Use**: Do NOT rely on for analysis -- totals may not match Raw_Data
- **Rule**: Always recalculate aggregations from Raw_Data instead of trusting this tab
- **Reason**: Pivot tables may exclude filtered rows, use stale caches, or contain manual overrides

## Tab: Dashboard

- **Role**: Visual presentation only
- **Use**: Ignore entirely for data extraction
- **Rule**: Contains merged cells, chart placeholders, and formatted headers that provide no analytical value
- **Reason**: Dashboard formatting confuses data extraction and contains no source data

## Tab: Notes

- **Role**: Internal team comments
- **Use**: Skip during analysis
- **Rule**: May contain context for human reviewers but is not structured data

---

# Required Working Method

1. Confirm the workflow is approved under Use Case ID UC-004.
2. Confirm all files are sample, masked, or approved internal finance data.
3. Read only the tabs designated as data sources (Raw_Data in this example).
4. Ignore tabs marked as visual-only, validation-only, or notes.
5. Use the column map from the File Structure section to locate fields.
6. Recalculate all totals from the source tab -- never trust pre-built summaries.
7. Perform the requested analysis using only source data.
8. If a tab's structure does not match this Skill, stop and report the discrepancy.
9. Produce output in the format below.
10. Save all outputs to the designated evidence folder.

---

# Output Format

Return the result using the following structure:

## File Validation

| Check | Result |
|-------|--------|
| Workbook matches Skill structure | Yes / No |
| Expected tabs present | list tabs found vs. expected |
| Source tab row count | number of data rows |
| Date range covered | earliest to latest date |

## Analysis Results

Present the requested analysis clearly:

- Use tables for numeric summaries
- Show calculations, not just results
- Compare to prior period if data is available
- Flag any anomalies or items requiring review

## Data Quality Notes

- list any missing values, formatting issues, or unexpected data found
- flag any rows that could not be classified

## Assumptions

- list assumptions made (date range, department groupings, etc.)

## Reviewer Checklist

- confirm source file matches the period under review
- confirm analysis used only the designated source tab
- confirm totals were recalculated (not pulled from pivot)
- confirm no posting or reporting action has been taken

---

# Style Rules

- Write in clear, factual language suitable for workpaper documentation
- State amounts precisely (do not round unless instructed)
- Always show which tab and columns were used for each calculation
- If the file structure does not match this Skill, report it immediately
- Keep the summary concise and audit-ready

---

# Example Invocation

Use this skill when the user provides an Excel workbook and asks for analysis.

Example prompts:

"Use the excel-interpretation skill on the monthly financial workbook in /data/raw. Calculate variance by department between January and February."

"Load the excel-interpretation skill and analyze the workbook. Summarize total spend by category for the most recent month."

"Using the excel-interpretation skill, verify whether the Pivot_Summary tab matches the Raw_Data totals."

---

# Evidence

Save outputs to:

`evidence/run-logs/`

Suggested file naming pattern:

`YYYY-MM-DD_UC-004_excel-interpretation.md`

---

# Human Review

Required reviewer:
- Controller
- Accounting Manager
- Senior Accountant (if delegated)

All output must be reviewed and signed off before results are used in reporting, reconciliation, or management review. This output documents what AI found -- it does not authorize any action.
