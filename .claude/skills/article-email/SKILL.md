---
name: article-email
description: Generate an email-safe HTML version of a PythonMuse article using the MkDocs brand styling. Defaults to a teaser (content up to the first `---` divider) with a CTA back to the full article. Pass an article slug or "all". Output lands in /emails/ with timestamped filenames so reruns never overwrite prior versions.
argument-hint: <article-slug | all> [--mode teaser|full]
---

# Article Email Generator

Generates Gmail/Outlook-safe HTML for a PythonMuse article. Styling matches the MkDocs Material site palette (teal #0F7B6C, coral #E05C4D, slate #3D4F5F) but every style is inlined per element so mainstream email clients render correctly.

## How to invoke

The user passes a single argument (article slug or `all`) and optionally `--mode`:

```bash
.venv/bin/python3 .claude/skills/article-email/generate_email.py <slug|all> [--mode teaser|full]
```

- `--mode teaser` (default): content up to the first `---` divider in the markdown, followed by a "Read the full article →" CTA button.
- `--mode full`: the entire article inlined into the email.

Authors control teaser length by where they place the first `---` in the article. Move it earlier for a tighter hook; move it later to include more setup.

## Output

- Destination: `emails/` at the repo root (sibling of `articles/`). Created on first run.
- Filename: `{slug}__{mode}__{YYYYMMDD-HHMMSS}.html`. The timestamp is shared across one invocation so a single `all` run groups files under the same stamp while staying unique vs. prior runs.

## What the generator does

1. Reads `articles/<slug>/README.md` (also accepts `Readme.md`).
2. In teaser mode, slices the markdown at the first `---` divider.
3. Converts markdown → HTML via the `markdown` library (extras: admonition, tables, fenced_code, attr_list).
4. Inlines per-element styles matching `articles/stylesheets/extra.css` (h1 with teal underline, h2 with teal left bar, h3 in teal, coral blockquote bar, teal-tinted code background, branded tables).
5. Rewrites every relative `href`/`src` to an absolute URL under `https://pythonmuse.com/<slug>/...` so images and cross-article links work in an email client.
6. Wraps the body in a 640px centered table layout with a teal top border, PythonMuse wordmark, hidden preheader text, "Read the full article →" CTA (teaser mode), copyright + postal-address line, and an unsubscribe footer.

## CAN-SPAM footer

Every email includes:

- A copyright line with PythonMuse LLC.
- A **postal address line** — currently a placeholder (`[PythonMuse LLC mailing address — replace before sending]`). CAN-SPAM requires a real postal address (a PO Box is fine). Edit `POSTAL_ADDRESS` in `generate_email.py` before bulk sending, or hand-edit each generated file.
- An **unsubscribe link** — a `mailto:` to `svetlana@pythonmuse.com` with a pre-filled subject and body. CAN-SPAM compliance depends on someone actually processing those replies within 10 business days; the link itself only satisfies the law if honored.

If volume grows, an ESP (Mailchimp, Substack, ConvertKit, Beehiiv) handles unsubscribes, list hygiene, and headers automatically — this generator is intended for low-volume manual sends out of Gmail or similar.

## Argument handling

- Single slug: validate it exists as a directory under `articles/` before invoking. If unsure, list `articles/` and let the user pick.
- `all`: generates every article folder that contains a `README.md`. Expect ~25+ files.

## Preview after generation

Tell the user the absolute path(s). To paste into Gmail, they should open the HTML in a browser, `Ctrl+A` to select the rendered page, `Ctrl+C`, then `Ctrl+V` into the Gmail compose window. Copying from a text editor pastes raw markup — copying from a rendered browser tab preserves styling.
