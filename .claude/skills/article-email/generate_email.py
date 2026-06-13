#!/usr/bin/env python3
"""Generate email-safe HTML versions of PythonMuse articles.

Reads markdown from articles/<slug>/README.md (or Readme.md), converts to
HTML using the PythonMuse brand palette, and writes a timestamped file into
the repo's emails/ directory. Designed for paste-into-Gmail / ESP delivery:
all styles are inlined on elements and relative URLs are rewritten to
absolute pythonmuse.com links.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
import sys
from pathlib import Path

import markdown


REPO_ROOT = Path(__file__).resolve().parents[3]
ARTICLES_DIR = REPO_ROOT / "articles"
EMAILS_DIR = REPO_ROOT / "emails"
SITE_HOST = "https://www.pythonmuse.com"
# Path prefix under SITE_HOST where articles live. Today the live site is
# the raw repo via GitHub Pages, so articles are at /articles/<slug>/.
# Once MkDocs deploy is enabled (Pages source -> gh-pages branch), set this
# to "" and articles will be at /<slug>/.
SITE_ARTICLE_PREFIX = "/articles"
SITE_BASE = SITE_HOST + SITE_ARTICLE_PREFIX
UNSUBSCRIBE_EMAIL = "svetlana@pythonmuse.com"
POSTAL_ADDRESS = "PythonMuse LLC · 6421 N. Florida Ave., Suite D-1089, Tampa, FL 33604"

BRAND = {
    "teal": "#0F7B6C",
    "teal_light": "#1a9e8a",
    "teal_dark": "#0a5a50",
    "coral": "#E05C4D",
    "slate": "#3D4F5F",
    "gold": "#E8A838",
    "gray": "#7A8694",
    "bg": "#ffffff",
    "page_bg": "#f4f1ec",
    "code_bg": "rgba(15, 123, 108, 0.08)",
    "rule": "rgba(15, 123, 108, 0.3)",
    "row_alt": "rgba(15, 123, 108, 0.05)",
}

FONT_STACK = (
    "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
    "'Helvetica Neue', Arial, sans-serif"
)
MONO_STACK = "'JetBrains Mono', Menlo, Consolas, 'Courier New', monospace"


def read_article(slug: str) -> tuple[str, Path]:
    folder = ARTICLES_DIR / slug
    for name in ("README.md", "Readme.md", "readme.md"):
        path = folder / name
        if path.exists():
            return path.read_text(encoding="utf-8"), path
    raise FileNotFoundError(f"No README.md found in {folder}")


def extract_title(md_text: str, slug: str) -> str:
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return slug.replace("-", " ").title()


def md_to_html(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "admonition",
            "sane_lists",
            "tables",
            "fenced_code",
            "attr_list",
        ],
        output_format="html5",
    )


def style(*pairs: str) -> str:
    return "; ".join(p for p in pairs if p)


STYLES = {
    "h1": style(
        f"color:{BRAND['slate']}",
        f"border-bottom:3px solid {BRAND['teal']}",
        "padding-bottom:8px",
        "font-size:28px",
        "line-height:1.25",
        "margin:0 0 16px 0",
        "font-weight:700",
    ),
    "h2": style(
        f"color:{BRAND['slate']}",
        f"border-left:4px solid {BRAND['teal']}",
        "padding:2px 0 2px 12px",
        "font-size:22px",
        "line-height:1.3",
        "margin:32px 0 12px 0",
        "font-weight:700",
    ),
    "h3": style(
        f"color:{BRAND['teal']}",
        "font-size:18px",
        "line-height:1.3",
        "margin:24px 0 10px 0",
        "font-weight:700",
    ),
    "h4": style(
        f"color:{BRAND['slate']}",
        "font-size:16px",
        "margin:20px 0 8px 0",
        "font-weight:700",
    ),
    "p": style(
        f"color:{BRAND['slate']}",
        "font-size:16px",
        "line-height:1.65",
        "margin:0 0 16px 0",
    ),
    "byline": style(
        f"color:{BRAND['gray']}",
        "font-size:16px",
        "line-height:1.5",
        "font-style:italic",
        "margin:0 0 24px 0",
    ),
    "ul": style(
        f"color:{BRAND['slate']}",
        "font-size:16px",
        "line-height:1.65",
        "margin:0 0 16px 0",
        "padding-left:22px",
    ),
    "ol": style(
        f"color:{BRAND['slate']}",
        "font-size:16px",
        "line-height:1.65",
        "margin:0 0 16px 0",
        "padding-left:22px",
    ),
    "li": style("margin:0 0 6px 0"),
    "a": style(f"color:{BRAND['teal']}", "text-decoration:underline"),
    "hr": style(
        "border:0",
        f"border-top:1px solid {BRAND['rule']}",
        "margin:28px 0",
    ),
    "blockquote": style(
        f"color:{BRAND['slate']}",
        f"border-left:4px solid {BRAND['coral']}",
        f"background:{BRAND['row_alt']}",
        "margin:0 0 16px 0",
        "padding:12px 16px",
        "font-style:italic",
    ),
    "code_inline": style(
        f"background:{BRAND['code_bg']}",
        f"color:{BRAND['slate']}",
        f"font-family:{MONO_STACK}",
        "padding:1px 5px",
        "border-radius:3px",
        "font-size:14px",
    ),
    "pre": style(
        f"background:{BRAND['code_bg']}",
        f"color:{BRAND['slate']}",
        f"font-family:{MONO_STACK}",
        "padding:12px 14px",
        "border-radius:4px",
        "font-size:14px",
        "line-height:1.5",
        "overflow:auto",
        "margin:0 0 16px 0",
        f"border-left:3px solid {BRAND['teal']}",
    ),
    "table": style(
        "border-collapse:collapse",
        "width:100%",
        "margin:0 0 16px 0",
        "font-size:15px",
    ),
    "th": style(
        f"background:{BRAND['teal']}",
        "color:#ffffff",
        "padding:8px 12px",
        "text-align:left",
        "font-weight:700",
    ),
    "td": style(
        f"color:{BRAND['slate']}",
        "padding:8px 12px",
        f"border-bottom:1px solid {BRAND['rule']}",
        "vertical-align:top",
    ),
    "img": style(
        "max-width:100%",
        "height:auto",
        "display:block",
        "margin:16px auto",
        "border-radius:4px",
    ),
}


def apply_inline_styles(html_body: str) -> str:
    """Inline style attributes onto each rendered tag.

    Email clients (Gmail in particular) strip <style> blocks; styles must
    live on the elements themselves. We do this as targeted regex passes
    rather than pulling in a full CSS-inliner dependency.
    """

    # First-paragraph byline (italics-only paragraph right after h1)
    # Apply this before generic <p> styling, then mark so it isn't overridden.
    html_body = re.sub(
        r"<p>(\s*<em>[^<]+</em>\s*)</p>",
        lambda m: f'<p style="{STYLES["byline"]}" data-pm-byline>{m.group(1)}</p>',
        html_body,
        count=1,
    )

    def add_style(tag: str, css: str, attrs: str = "") -> str:
        # Replace opening tags that don't already have a style attribute.
        pattern = rf"<{tag}(\s[^>]*)?>"

        def repl(m: re.Match) -> str:
            existing = m.group(1) or ""
            if "style=" in existing:
                return m.group(0)
            if "data-pm-byline" in existing:
                return m.group(0)
            return f'<{tag}{existing} style="{css}"{attrs}>'

        return re.sub(pattern, repl, html_body)

    for tag in ("h1", "h2", "h3", "h4", "p", "ul", "ol", "li", "a", "blockquote", "table", "th", "td", "img"):
        html_body = add_style(tag, STYLES[tag])

    html_body = re.sub(r"<hr\s*/?>", f'<hr style="{STYLES["hr"]}" />', html_body)
    html_body = re.sub(r"<pre>", f'<pre style="{STYLES["pre"]}">', html_body)

    # Inline <code> (only those not inside <pre>). Replace any <code> without a
    # style attribute; preformatted blocks get their styling from <pre>.
    def code_repl(m: re.Match) -> str:
        attrs = m.group(1) or ""
        if "style=" in attrs:
            return m.group(0)
        return f'<code{attrs} style="{STYLES["code_inline"]}">'

    html_body = re.sub(r"<code(\s[^>]*)?>", code_repl, html_body)

    # Reset code styling when inside <pre> — let <pre> own the look.
    html_body = re.sub(
        r"(<pre[^>]*>)\s*<code[^>]*>",
        r"\1<code>",
        html_body,
    )

    return html_body


def absolutize_links(html_body: str, slug: str) -> str:
    """Rewrite relative href/src to absolute URLs on pythonmuse.com."""

    article_base = f"{SITE_BASE}/{slug}/"

    def make_absolute(url: str) -> str:
        if not url:
            return url
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            return url
        if url.startswith("//"):
            return "https:" + url
        if url.startswith("/"):
            # Absolute site paths anchor at the host, not the articles prefix.
            return SITE_HOST + url
        # Relative path. Normalize ../ traversal against article_base.
        from urllib.parse import urljoin
        return urljoin(article_base, url)

    def repl_attr(attr: str):
        def inner(m: re.Match) -> str:
            quote = m.group(1)
            url = m.group(2)
            return f'{attr}={quote}{make_absolute(url)}{quote}'
        return inner

    html_body = re.sub(r'href=(["\'])([^"\']+)\1', repl_attr("href"), html_body)
    html_body = re.sub(r'src=(["\'])([^"\']+)\1', repl_attr("src"), html_body)
    return html_body


def split_teaser(md_text: str) -> str:
    """Return content up to (but not including) the first `---` divider.

    Authors control teaser length by where they place the first horizontal
    rule. If no divider is found, the full article is returned (caller
    should typically only invoke this in teaser mode).
    """

    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 0:
            return "\n".join(lines[:i]).rstrip()
    return md_text


def build_email(slug: str, mode: str = "teaser") -> tuple[str, str]:
    md_text, _ = read_article(slug)
    title = extract_title(md_text, slug)

    if mode == "teaser":
        body_md = split_teaser(md_text)
    else:
        body_md = md_text

    body_html = md_to_html(body_md)
    body_html = apply_inline_styles(body_html)
    body_html = absolutize_links(body_html, slug)

    canonical = f"{SITE_BASE}/{slug}/"
    preheader = f"From PythonMuse — {title}"

    page_bg = BRAND["page_bg"]
    card_bg = BRAND["bg"]
    slate = BRAND["slate"]
    teal = BRAND["teal"]
    gray = BRAND["gray"]

    head_css_min = (
        "body{margin:0;padding:0;background:" + page_bg + ";} "
        "a{color:" + teal + ";} "
        "img{border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;} "
        "table{border-collapse:collapse;} "
    )

    cta_html = ""
    if mode == "teaser":
        cta_html = f"""
        <tr>
          <td align="center" style="padding:8px 36px 28px 36px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="background:{teal};border-radius:4px;">
                  <a href="{canonical}" style="display:inline-block;padding:12px 24px;color:#ffffff;font-family:{FONT_STACK};font-size:15px;font-weight:700;text-decoration:none;letter-spacing:0.02em;">Read the full article &rarr;</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>"""

    unsub_subject = "Unsubscribe from PythonMuse"
    unsub_body = "Please remove me from the PythonMuse list."
    unsub_href = (
        f"mailto:{UNSUBSCRIBE_EMAIL}"
        f"?subject={unsub_subject.replace(' ', '%20')}"
        f"&body={unsub_body.replace(' ', '%20')}"
    )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" />
<title>{html.escape(title)}</title>
<style>{head_css_min}</style>
</head>
<body style="margin:0;padding:0;background:{page_bg};font-family:{FONT_STACK};">
<span style="display:none !important;visibility:hidden;opacity:0;color:transparent;height:0;width:0;overflow:hidden;mso-hide:all;">{html.escape(preheader)}</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{page_bg};">
  <tr>
    <td align="center" style="padding:24px 12px;">
      <table role="presentation" width="640" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:640px;background:{card_bg};border-top:6px solid {teal};box-shadow:0 1px 3px rgba(0,0,0,0.06);">
        <tr>
          <td style="padding:28px 36px 12px 36px;">
            <a href="{SITE_BASE}/" style="text-decoration:none;color:{teal};font-family:{FONT_STACK};font-weight:700;font-size:14px;letter-spacing:0.08em;text-transform:uppercase;">PythonMuse</a>
          </td>
        </tr>
        <tr>
          <td style="padding:0 36px 8px 36px;font-family:{FONT_STACK};color:{slate};">
            {body_html}
          </td>
        </tr>{cta_html}
        <tr>
          <td style="padding:24px 36px 28px 36px;border-top:1px solid {BRAND['rule']};font-family:{FONT_STACK};color:{gray};font-size:13px;line-height:1.6;">
            Read this article on the web:
            <a href="{canonical}" style="color:{teal};text-decoration:underline;">{canonical}</a><br />
            <span style="color:{gray};">&copy; PythonMuse LLC &middot; Practical Python &amp; AI for accounting and finance.</span><br />
            <span style="color:{gray};">{html.escape(POSTAL_ADDRESS)}</span>
          </td>
        </tr>
        <tr>
          <td style="padding:0 36px 28px 36px;font-family:{FONT_STACK};color:{gray};font-size:12px;line-height:1.6;">
            You're receiving this email because you subscribed to updates from PythonMuse.
            <a href="{unsub_href}" style="color:{teal};text-decoration:underline;">Unsubscribe</a>
            (replies to {UNSUBSCRIBE_EMAIL} are processed within 10 business days).
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""
    return title, document


def output_filename(slug: str, when: _dt.datetime) -> Path:
    stamp = when.strftime("%Y%m%d-%H%M%S")
    return EMAILS_DIR / f"{slug}__{stamp}.html"


def discover_slugs() -> list[str]:
    slugs = []
    for child in sorted(ARTICLES_DIR.iterdir()):
        if not child.is_dir():
            continue
        if any((child / n).exists() for n in ("README.md", "Readme.md", "readme.md")):
            slugs.append(child.name)
    return slugs


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate email-safe HTML from a PythonMuse article."
    )
    parser.add_argument(
        "target",
        help="Article slug (folder name under articles/) or 'all'.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(EMAILS_DIR),
        help="Output directory (defaults to repo /emails).",
    )
    parser.add_argument(
        "--mode",
        choices=("teaser", "full"),
        default="teaser",
        help="teaser (default): cut at first --- divider and add CTA. full: entire article.",
    )
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.target == "all":
        slugs = discover_slugs()
    else:
        slugs = [args.target]

    when = _dt.datetime.now()
    written: list[Path] = []
    suffix = "teaser" if args.mode == "teaser" else "full"
    for slug in slugs:
        try:
            title, doc = build_email(slug, mode=args.mode)
        except FileNotFoundError as e:
            print(f"skip {slug}: {e}", file=sys.stderr)
            continue
        path = out_dir / f"{slug}__{suffix}__{when.strftime('%Y%m%d-%H%M%S')}.html"
        path.write_text(doc, encoding="utf-8")
        written.append(path)
        print(f"wrote {path}  ({title})")

    print(f"\n{len(written)} file(s) written to {out_dir}")
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
