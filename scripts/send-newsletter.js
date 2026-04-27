#!/usr/bin/env node

/**
 * send-newsletter.js
 *
 * Converts a PythonMuse LLC markdown article to a branded HTML email
 * and optionally sends it to your subscriber list via Resend.
 *
 * Usage:
 *   Preview only (writes HTML to email-output/):
 *     node scripts/send-newsletter.js articles/22-workings-layer-method/README.md --preview
 *
 *   Send to subscribers:
 *     node scripts/send-newsletter.js articles/22-workings-layer-method/README.md
 *
 * Required env vars for sending:
 *   RESEND_API_KEY   — from resend.com (free tier: 3,000 emails/month)
 *   FROM_EMAIL       — e.g. "PythonMuse LLC <newsletter@pythonmuse.com>"
 *
 * Optional env vars:
 *   FROM_NAME        — defaults to "PythonMuse LLC"
 *   UNSUBSCRIBE_URL  — defaults to placeholder; update before live sends
 *
 * Note: relative links in articles are automatically converted to absolute
 * GitHub URLs so they work in email. Update GITHUB_REPO if the repo moves.
 *
 * ── HUMAN SETUP NOTES ────────────────────────────────────────────────────────
 *
 *  1. SUBSCRIBERS FILE
 *     Place subscribers.json in the project root (it is gitignored).
 *     Format: [{ "email": "name@example.com", "name": "First Last" }, ...]
 *     A sample file is created automatically on first run.
 *
 *  2. FROM EMAIL / DOMAIN
 *     Update FROM_EMAIL env var (or the default below) to match your
 *     verified sending domain in Resend. Free tier allows resend.dev subdomains.
 *     Search: "UPDATE_FROM_EMAIL" to find the line.
 *
 *  3. UNSUBSCRIBE LINK
 *     Replace the UNSUBSCRIBE_URL default with your actual unsubscribe page.
 *     Search: "UPDATE_UNSUBSCRIBE_URL" to find the line.
 *
 *  4. GITHUB LINK IN FOOTER
 *     The footer links to the ai-ledger repo. Update if the repo URL changes.
 *     Search: "UPDATE_GITHUB_URL" to find the line.
 *
 *  5. ARTICLE IMAGES
 *     Inline images (./visuals/...) will NOT render in most email clients
 *     unless hosted at a public URL. Either upload visuals to a CDN/GitHub
 *     Pages and update the paths in the article, or remove image lines for
 *     email sends. The --preview mode will show you exactly what renders.
 *
 *  5. RELATIVE LINKS
 *     Relative links (../other-article/, ../../examples/...) are converted
 *     to absolute GitHub URLs. Update GITHUB_REPO if the repo moves.
 *     Search: "UPDATE_GITHUB_REPO"
 *
 * ─────────────────────────────────────────────────────────────────────────────
 */

const fs   = require("fs");
const path = require("path");

const PREVIEW_MODE = process.argv.includes("--preview");
const articlePath  = process.argv.find(a => !a.startsWith("--") && a !== process.argv[0] && a !== process.argv[1]);

if (!articlePath) {
  console.error("Usage: node scripts/send-newsletter.js <path/to/README.md> [--preview]");
  process.exit(1);
}

// ─── Configuration ─────────────────────────────────────────────────────────────

const FROM_NAME       = process.env.FROM_NAME       || "PythonMuse LLC";
const FROM_EMAIL      = process.env.FROM_EMAIL      || "newsletter@pythonmuse.com"; // UPDATE_FROM_EMAIL
const UNSUBSCRIBE_URL = process.env.UNSUBSCRIBE_URL || "https://pythonmuse.com/unsubscribe"; // UPDATE_UNSUBSCRIBE_URL
const GITHUB_REPO     = "https://github.com/PythonMuse/ai-ledger"; // UPDATE_GITHUB_REPO
const GITHUB_URL      = GITHUB_REPO;

// ─── 1. Parse markdown article ────────────────────────────────────────────────

const raw = fs.readFileSync(articlePath, "utf8");

// Parse optional YAML front-matter
let frontMatter = {};
let body = raw;

if (raw.startsWith("---")) {
  const end = raw.indexOf("---", 3);
  if (end !== -1) {
    raw.slice(3, end).trim().split("\n").forEach(line => {
      const [k, ...v] = line.split(":");
      if (k) frontMatter[k.trim()] = v.join(":").trim();
    });
    body = raw.slice(end + 3).trim();
  }
}

// Pull title from front-matter or first H1
const h1Match = body.match(/^# (.+)$/m);
const title   = frontMatter.title   || (h1Match ? h1Match[1] : path.basename(articlePath, ".md").replace(/-/g, " "));
const subject = frontMatter.subject || `New article: ${title}`;

// Strip H1 (shown in hero instead)
body = body.replace(/^# .+$/m, "").trim();

// Strip local image references (won't render in email — host visuals publicly first)
body = body.replace(/^!\[.*?\]\(\.\/visuals\/.*?\)\s*$/gm, "");

// Convert relative markdown links to absolute GitHub URLs
// Skips external links (http/https) and anchors (#)
const repoRoot       = path.dirname(__dirname);
const absArticleDir  = path.dirname(path.resolve(articlePath));
const relArticleDir  = path.relative(repoRoot, absArticleDir).replace(/\\/g, "/");

body = body.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, href) => {
  if (href.startsWith("http://") || href.startsWith("https://") || href.startsWith("#")) {
    return match;
  }
  const resolved = path.posix.normalize(`${relArticleDir}/${href}`);
  return `[${text}](${GITHUB_REPO}/tree/main/${resolved})`;
});

// Preview text: first substantive non-heading paragraph
const previewText = body.split("\n")
  .filter(l => l.trim() && !l.startsWith("#") && !l.startsWith("!") && !l.startsWith("---") && !l.startsWith("**PythonMuse"))
  .map(l => l.replace(/[*`>\[\]]/g, "").trim())
  .find(l => l.length > 40) || "";
const preview = frontMatter.preview || previewText.slice(0, 140) + (previewText.length > 140 ? "…" : "");

// ─── 2. Markdown → HTML ───────────────────────────────────────────────────────
//
// Minimal in-house parser sufficient for PythonMuse article structure.
// For full GFM support install `marked` and replace markdownToHtml(body)
// with marked(body):  npm install marked  →  const { marked } = require("marked");

function markdownToHtml(md) {
  return md
    // Fenced code blocks
    .replace(/```[\w]*\n([\s\S]*?)```/g, (_, code) =>
      `<pre style="background:#e4f2f5;padding:16px;border-radius:4px;overflow-x:auto;font-size:13px;line-height:1.6;"><code style="color:#0e6273;">${code.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>`)
    // Headings
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm,  "<h2>$1</h2>")
    .replace(/^# (.+)$/gm,   "<h1>$1</h1>")
    // Bold / italic
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g,     "<em>$1</em>")
    // Inline code
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    // Images (kept if not already stripped)
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width:100%;border-radius:6px;margin:16px 0;">')
    // Links (already resolved to absolute URLs above)
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:#0e7490;text-decoration:underline;">$1</a>')
    // Blockquotes
    .replace(/^> (.+)$/gm, "<blockquote>$1</blockquote>")
    // Horizontal rules
    .replace(/^---+$/gm, "<hr>")
    // List items
    .replace(/^\* (.+)$/gm,    "<li>$1</li>")
    .replace(/^- (.+)$/gm,     "<li>$1</li>")
    .replace(/^\d+\. (.+)$/gm, "<li>$1</li>")
    // Paragraphs
    .split(/\n{2,}/)
    .map(block => {
      block = block.trim();
      if (!block) return "";
      if (/^<(h[1-6]|pre|ul|ol|li|blockquote|hr|img)/.test(block)) return block;
      if (block.startsWith("<li>")) return `<ul>${block}</ul>`;
      return `<p>${block.replace(/\n/g, " ")}</p>`;
    })
    .join("\n");
}

const articleHtml = markdownToHtml(body);

// ─── 3. HTML email template ───────────────────────────────────────────────────

function buildEmailHtml({ title, preview, articleHtml, fromName, unsubscribeUrl, githubUrl }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light">
  <!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
  <title>${title}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #f0f6f7; font-family: Georgia, 'Times New Roman', serif; -webkit-text-size-adjust: 100%; }
    .wrapper { width: 100%; background: #f0f6f7; padding: 40px 16px; }
    .card { max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 4px; overflow: hidden; border: 1px solid #b8d8de; }
    .header { background: #1e3a5f; padding: 28px 40px; display: flex; align-items: center; justify-content: space-between; }
    .header-brand { color: #ffffff; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 13px; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; }
    .header-issue { color: #7fb3c8; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 12px; letter-spacing: 0.06em; }
    .hero { padding: 44px 40px 32px; border-bottom: 1px solid #b8d8de; }
    .hero-label { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: #0e7490; margin-bottom: 16px; }
    .hero-title { font-size: 32px; line-height: 1.22; font-weight: normal; color: #0f0f0f; letter-spacing: -0.02em; margin-bottom: 16px; }
    .hero-preview { font-size: 16px; line-height: 1.6; color: #555; font-style: italic; }
    .body { padding: 36px 40px; }
    .body p  { font-size: 17px; line-height: 1.75; color: #1a1a1a; margin-bottom: 22px; }
    .body h1 { font-size: 26px; line-height: 1.3; color: #1e3a5f; margin: 36px 0 16px; font-weight: normal; letter-spacing: -0.02em; }
    .body h2 { font-size: 21px; line-height: 1.35; color: #1e3a5f; margin: 32px 0 14px; font-weight: normal; letter-spacing: -0.01em; }
    .body h3 { font-size: 17px; line-height: 1.4; color: #1e3a5f; margin: 28px 0 12px; font-weight: bold; }
    .body ul, .body ol { margin: 0 0 22px 24px; }
    .body li { font-size: 17px; line-height: 1.75; color: #1a1a1a; margin-bottom: 6px; }
    .body strong { font-weight: bold; color: #0f0f0f; }
    .body em { font-style: italic; }
    .body code { font-family: 'Courier New', Courier, monospace; font-size: 14px; background: #e4f2f5; color: #0e6273; padding: 2px 6px; border-radius: 3px; }
    .body pre { margin-bottom: 22px; }
    .body blockquote { border-left: 3px solid #0e7490; padding: 4px 0 4px 20px; margin: 24px 0; color: #555; font-style: italic; font-size: 18px; line-height: 1.6; }
    .body hr { border: none; border-top: 1px solid #b8d8de; margin: 36px 0; }
    .body a { color: #0e7490; }
    .divider { border: none; border-top: 1px solid #b8d8de; margin: 0; }
    .footer { padding: 28px 40px; background: #edf5f7; }
    .footer p { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 12px; color: #6b8fa0; line-height: 1.6; margin-bottom: 6px; }
    .footer a { color: #0e7490; text-decoration: underline; }
    @media (max-width: 480px) {
      .header, .hero, .body, .footer { padding-left: 24px; padding-right: 24px; }
      .hero-title { font-size: 26px; }
      .body p, .body li { font-size: 16px; }
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="card">

      <div class="header">
        <span class="header-brand">${fromName}</span>
        <span class="header-issue">New article</span>
      </div>

      <div class="hero">
        <div class="hero-label">Just published</div>
        <h1 class="hero-title">${title}</h1>
        <p class="hero-preview">${preview}</p>
      </div>

      <div class="body">
        ${articleHtml}
      </div>

      <hr class="divider">

      <div class="footer">
        <p>You're receiving this because you subscribed to <strong>${fromName}</strong>.</p>
        <!-- UPDATE_UNSUBSCRIBE_URL: replace href with your actual unsubscribe page URL -->
        <!-- UPDATE_GITHUB_URL: replace href if the repo URL ever changes -->
        <p><a href="${unsubscribeUrl}">Unsubscribe</a> &nbsp;·&nbsp; <a href="${githubUrl}">View on GitHub</a></p>
      </div>

    </div>
  </div>
</body>
</html>`;
}

// ─── 4. Preview mode (--preview) ─────────────────────────────────────────────
//
// Writes the HTML to email-output/<article-slug>.html so you can open it
// in a browser before sending to any subscribers.

if (PREVIEW_MODE) {
  const outputDir  = path.join(__dirname, "..", "email-output");
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

  const slug       = path.basename(path.dirname(path.resolve(articlePath)));
  const outputFile = path.join(outputDir, `${slug}.html`);

  const html = buildEmailHtml({ title, preview, articleHtml, fromName: FROM_NAME, unsubscribeUrl: UNSUBSCRIBE_URL, githubUrl: GITHUB_URL });
  fs.writeFileSync(outputFile, html, "utf8");

  console.log(`\nPreview written to: ${outputFile}`);
  console.log(`Open in your browser to review before sending.\n`);
  process.exit(0);
}

// ─── 5. Load subscribers ──────────────────────────────────────────────────────
//
// subscribers.json is gitignored. Format:
//   [{ "email": "name@example.com", "name": "First Last" }, ...]

const subscribersPath = path.join(__dirname, "..", "subscribers.json");
let subscribers = [];

if (fs.existsSync(subscribersPath)) {
  subscribers = JSON.parse(fs.readFileSync(subscribersPath, "utf8"));
} else {
  console.warn("No subscribers.json found. Creating a sample file.");
  subscribers = [{ email: "you@example.com", name: "Test Subscriber" }];
  fs.writeFileSync(subscribersPath, JSON.stringify(subscribers, null, 2));
  console.warn("Edit subscribers.json then re-run to send.\n");
  process.exit(0);
}

// ─── 7. Send via Resend API ───────────────────────────────────────────────────

const RESEND_API_KEY = process.env.RESEND_API_KEY;

if (!RESEND_API_KEY) {
  console.error("RESEND_API_KEY env var is required. Get one free at https://resend.com");
  process.exit(1);
}

async function sendEmail(to) {
  const html = buildEmailHtml({ title, preview, articleHtml, fromName: FROM_NAME, unsubscribeUrl: UNSUBSCRIBE_URL, githubUrl: GITHUB_URL });

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from:    `${FROM_NAME} <${FROM_EMAIL}>`,
      to:      [to],
      subject,
      html,
    }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(data));
  return data;
}

async function main() {
  console.log(`\nSending "${title}" to ${subscribers.length} subscriber(s)...\n`);
  let sent = 0, failed = 0;

  for (const sub of subscribers) {
    try {
      await sendEmail(sub.email);
      console.log(`  sent: ${sub.email}`);
      sent++;
      await new Promise(r => setTimeout(r, 200)); // avoid Resend rate limits
    } catch (err) {
      console.error(`  failed: ${sub.email} — ${err.message}`);
      failed++;
    }
  }

  console.log(`\nDone. Sent: ${sent}  Failed: ${failed}\n`);
  if (failed > 0) process.exit(1);
}

main();
