#!/usr/bin/env python3
"""
preview_email.py

Converts a PythonMuse LLC markdown article to a branded HTML email preview.
Writes output to email-output/<article-slug>.html so you can open it in
a browser and review before sending via send-newsletter.js.

Usage:
    python scripts/preview_email.py articles/22-workings-layer-method/README.md

Requirements:
    pip install markdown

── HUMAN SETUP NOTES ────────────────────────────────────────────────────────

  1. INSTALL DEPENDENCY
     pip install markdown
     (Uses Python-Markdown for reliable GFM-compatible rendering.)

  2. FROM_NAME
     Update FROM_NAME below if the brand name changes.
     Search: "UPDATE_FROM_NAME"

  3. UNSUBSCRIBE / GITHUB LINKS
     Update the footer URLs before using the HTML in a real send.
     Search: "UPDATE_UNSUBSCRIBE_URL" and "UPDATE_GITHUB_URL"

  4. ARTICLE IMAGES
     Inline images (./visuals/...) are stripped by default because they
     won't render in most email clients unless hosted at a public URL.
     To keep images: remove the image-stripping block below and host
     visuals on a CDN or GitHub Pages first.

  5. RELATIVE LINKS
     Relative links (../other-article/, ../../examples/...) are automatically
     converted to absolute GitHub URLs so they work in email.
     Update GITHUB_REPO below if the repo URL changes.
     Search: "UPDATE_GITHUB_REPO"

─────────────────────────────────────────────────────────────────────────────
"""

import sys
import os
import re
import textwrap

try:
    import markdown
except ImportError:
    print("Error: 'markdown' package not found. Run: pip install markdown")
    sys.exit(1)

# ─── Configuration ─────────────────────────────────────────────────────────────

FROM_NAME       = "PythonMuse LLC"                                    # UPDATE_FROM_NAME
UNSUBSCRIBE_URL = "https://pythonmuse.com/unsubscribe"                # UPDATE_UNSUBSCRIBE_URL
GITHUB_REPO     = "https://github.com/PythonMuse/ai-ledger"           # UPDATE_GITHUB_REPO
GITHUB_URL      = GITHUB_REPO                                         # footer link

# ─── Parse article ─────────────────────────────────────────────────────────────

if len(sys.argv) < 2:
    print("Usage: python scripts/preview_email.py <path/to/README.md>")
    sys.exit(1)

article_path = sys.argv[1]
raw = open(article_path, encoding="utf-8").read()

# Article's directory relative to repo root (used for resolving relative links)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
abs_article_dir = os.path.dirname(os.path.abspath(article_path))
rel_article_dir = os.path.relpath(abs_article_dir, REPO_ROOT).replace("\\", "/")

# Strip H1 title (displayed in hero section instead)
h1_match = re.search(r"^# (.+)$", raw, re.MULTILINE)
title = h1_match.group(1) if h1_match else os.path.basename(abs_article_dir)
body = re.sub(r"^# .+$\n?", "", raw, count=1, flags=re.MULTILINE).strip()

# Strip local image references (won't render in email — see setup note 4)
body = re.sub(r"^!\[.*?\]\(\./visuals/.*?\)\s*$", "", body, flags=re.MULTILINE)

# Convert relative markdown links to absolute GitHub URLs (see setup note 5)
# Handles: [text](../other-article/), [text](../../examples/foo/), [text](./file.md)
# Skips:   [text](https://...), [text](#anchor)
def resolve_link(match):
    text = match.group(1)
    href = match.group(2)
    if href.startswith("http://") or href.startswith("https://") or href.startswith("#"):
        return match.group(0)  # leave external links and anchors as-is
    resolved = os.path.normpath(os.path.join(rel_article_dir, href)).replace("\\", "/")
    abs_url = f"{GITHUB_REPO}/tree/main/{resolved}"
    return f"[{text}]({abs_url})"

body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", resolve_link, body)

# Preview text: first substantive paragraph
preview = ""
for line in body.splitlines():
    line = line.strip()
    if (line and not line.startswith("#") and not line.startswith("!")
            and not line.startswith("---") and not line.startswith("**PythonMuse")
            and len(line) > 40):
        preview = re.sub(r"[*`>\[\]]", "", line)[:140]
        if len(line) > 140:
            preview += "…"
        break

# ─── Convert markdown to HTML ──────────────────────────────────────────────────

md = markdown.Markdown(extensions=["fenced_code", "tables", "attr_list"])
article_html = md.convert(body)

# ─── Email template ────────────────────────────────────────────────────────────
#
# Color palette — teal + navy:
#   Navy header:      #1e3a5f
#   Teal accent:      #0e7490
#   Dark teal code:   #0e6273
#   Light teal bg:    #e4f2f5
#   Cool page bg:     #f0f6f7
#   Cool footer bg:   #edf5f7
#   Teal border:      #b8d8de

def build_email_html(title, preview, article_html, from_name, unsubscribe_url, github_url):
    return textwrap.dedent(f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="color-scheme" content="light">
      <title>{title}</title>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: #f0f6f7; font-family: Georgia, 'Times New Roman', serif; -webkit-text-size-adjust: 100%; }}
        .wrapper {{ width: 100%; background: #f0f6f7; padding: 40px 16px; }}
        .card {{ max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 4px; overflow: hidden; border: 1px solid #b8d8de; }}
        .header {{ background: #1e3a5f; padding: 28px 40px; display: flex; align-items: center; justify-content: space-between; }}
        .header-brand {{ color: #ffffff; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 13px; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; }}
        .header-issue {{ color: #7fb3c8; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 12px; letter-spacing: 0.06em; }}
        .hero {{ padding: 44px 40px 32px; border-bottom: 1px solid #b8d8de; }}
        .hero-label {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: #0e7490; margin-bottom: 16px; }}
        .hero-title {{ font-size: 32px; line-height: 1.22; font-weight: normal; color: #0f0f0f; letter-spacing: -0.02em; margin-bottom: 16px; }}
        .hero-preview {{ font-size: 16px; line-height: 1.6; color: #555; font-style: italic; }}
        .body {{ padding: 36px 40px; }}
        .body p  {{ font-size: 17px; line-height: 1.75; color: #1a1a1a; margin-bottom: 22px; }}
        .body h1 {{ font-size: 26px; line-height: 1.3; color: #1e3a5f; margin: 36px 0 16px; font-weight: normal; letter-spacing: -0.02em; }}
        .body h2 {{ font-size: 21px; line-height: 1.35; color: #1e3a5f; margin: 32px 0 14px; font-weight: normal; letter-spacing: -0.01em; }}
        .body h3 {{ font-size: 17px; line-height: 1.4; color: #1e3a5f; margin: 28px 0 12px; font-weight: bold; }}
        .body ul, .body ol {{ margin: 0 0 22px 24px; }}
        .body li {{ font-size: 17px; line-height: 1.75; color: #1a1a1a; margin-bottom: 6px; }}
        .body strong {{ font-weight: bold; color: #0f0f0f; }}
        .body em {{ font-style: italic; }}
        .body code {{ font-family: 'Courier New', Courier, monospace; font-size: 14px; background: #e4f2f5; color: #0e6273; padding: 2px 6px; border-radius: 3px; }}
        .body pre {{ background: #e4f2f5; padding: 16px; border-radius: 4px; overflow-x: auto; margin-bottom: 22px; font-size: 13px; line-height: 1.6; }}
        .body pre code {{ background: none; color: #0e6273; padding: 0; }}
        .body blockquote {{ border-left: 3px solid #0e7490; padding: 4px 0 4px 20px; margin: 24px 0; color: #555; font-style: italic; font-size: 18px; line-height: 1.6; }}
        .body hr {{ border: none; border-top: 1px solid #b8d8de; margin: 36px 0; }}
        .body a {{ color: #0e7490; }}
        .body table {{ border-collapse: collapse; width: 100%; margin-bottom: 22px; font-size: 15px; }}
        .body th, .body td {{ border: 1px solid #b8d8de; padding: 8px 12px; text-align: left; }}
        .body th {{ background: #e4f2f5; color: #1e3a5f; font-weight: bold; }}
        .divider {{ border: none; border-top: 1px solid #b8d8de; margin: 0; }}
        .footer {{ padding: 28px 40px; background: #edf5f7; }}
        .footer p {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 12px; color: #6b8fa0; line-height: 1.6; margin-bottom: 6px; }}
        .footer a {{ color: #0e7490; text-decoration: underline; }}
        @media (max-width: 480px) {{
          .header, .hero, .body, .footer {{ padding-left: 24px; padding-right: 24px; }}
          .hero-title {{ font-size: 26px; }}
          .body p, .body li {{ font-size: 16px; }}
        }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="card">
          <div class="header">
            <span class="header-brand">{from_name}</span>
            <span class="header-issue">New article</span>
          </div>
          <div class="hero">
            <div class="hero-label">Just published</div>
            <h1 class="hero-title">{title}</h1>
            <p class="hero-preview">{preview}</p>
          </div>
          <div class="body">
            {article_html}
          </div>
          <hr class="divider">
          <div class="footer">
            <p>You're receiving this because you subscribed to <strong>{from_name}</strong>.</p>
            <!-- UPDATE_UNSUBSCRIBE_URL: replace href with your actual unsubscribe page URL -->
            <!-- UPDATE_GITHUB_URL: replace href if the repo URL ever changes -->
            <p><a href="{unsubscribe_url}">Unsubscribe</a> &nbsp;·&nbsp; <a href="{github_url}">View on GitHub</a></p>
          </div>
        </div>
      </div>
    </body>
    </html>""")

# ─── Write output ──────────────────────────────────────────────────────────────

output_dir = os.path.join(REPO_ROOT, "email-output")
os.makedirs(output_dir, exist_ok=True)

slug = os.path.basename(abs_article_dir)
output_file = os.path.join(output_dir, f"{slug}.html")

html = build_email_html(title, preview, article_html, FROM_NAME, UNSUBSCRIBE_URL, GITHUB_URL)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nPreview written to: {output_file}")
print("Open in your browser to review before sending.\n")
