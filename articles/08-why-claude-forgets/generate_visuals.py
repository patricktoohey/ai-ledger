"""
Generate Article 08 visuals — Why Claude "Forgets".

Visual 01: Hero / front image
  Branded title card: "Why Claude 'Forgets'".

Visual 02: Context Window Problem
  Diagram showing how the context window fills and loses earlier information.

Visual 03: External Memory System
  Three-file system (plan.md, status_update.md, CLAUDE.md) diagram.

Saved to articles/08-why-claude-forgets/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# ── Output directory ──────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "visuals")
os.makedirs(OUT_DIR, exist_ok=True)

# ── PythonMuse brand colors ──────────────────────────────────────────────────
DEEP_NAVY     = "#002639"
MIDNIGHT_TEAL = "#003144"
BRIGHT_TEAL   = "#3ABFB9"
GOLDEN_YELLOW = "#FFD75E"
WARM_GLOW     = "#F5D384"
OCEAN_TEAL    = "#005F6F"
SOFT_SAGE     = "#91BE8E"
SEA_GREEN     = "#2BA19A"
WHITE         = "#FFFFFF"
ALERT_RED     = "#E05252"
GRAY_BG       = "#F4F6F7"
GRAY_LINE     = "#CCCCCC"
LIGHT_RED_BG  = "#FDE8E8"


# ─────────────────────────────────────────────────────────────────────────────
# Visual 01 – Hero / Front Image
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(12, 6))
fig1.patch.set_facecolor(DEEP_NAVY)
ax1.set_facecolor(DEEP_NAVY)
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 6)
ax1.axis("off")

# Title
ax1.text(6, 3.8, 'Why Claude "Forgets"',
         ha="center", va="center",
         fontsize=28, fontweight="bold", color=BRIGHT_TEAL,
         linespacing=1.3)

# Subtitle
ax1.text(6, 2.6, "And How to Fix It with\nSimple Project Files",
         ha="center", va="center",
         fontsize=16, color=GOLDEN_YELLOW, fontstyle="italic",
         linespacing=1.3)

# Divider line
ax1.plot([3, 9], [1.7, 1.7], color=OCEAN_TEAL, linewidth=2)

# Byline
ax1.text(6, 1.0, "PythonMuse  |  By Svetlana Toohey",
         ha="center", va="center",
         fontsize=11, color=WHITE, alpha=0.7)

out_path1 = os.path.join(OUT_DIR, "08_visual_front.png")
plt.savefig(out_path1, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 08_visual_front.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 02 – The Context Window Problem
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(12, 8))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(0, 12)
ax2.set_ylim(0, 8)
ax2.axis("off")

# Title
ax2.text(6, 7.5, "The Context Window Problem",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax2.text(6, 7.0, "What happens as your conversation grows",
         ha="center", va="center",
         fontsize=11, color=OCEAN_TEAL, fontstyle="italic")

# Draw the context window as a long horizontal bar with segments
bar_y = 4.5
bar_height = 1.6
bar_left = 1.0
bar_right = 11.0
bar_width = bar_right - bar_left

# Background bar (the full window)
bg_box = FancyBboxPatch(
    (bar_left, bar_y - bar_height / 2), bar_width, bar_height,
    boxstyle="round,pad=0.08",
    facecolor=GRAY_BG, edgecolor=DEEP_NAVY,
    linewidth=2, zorder=1
)
ax2.add_patch(bg_box)

# Segment 1: Early decisions (faded/lost)
seg1_width = bar_width * 0.3
seg1_box = FancyBboxPatch(
    (bar_left + 0.05, bar_y - bar_height / 2 + 0.05),
    seg1_width, bar_height - 0.1,
    boxstyle="round,pad=0.06",
    facecolor=LIGHT_RED_BG, edgecolor=ALERT_RED,
    linewidth=1.5, linestyle="--", zorder=2, alpha=0.7
)
ax2.add_patch(seg1_box)
ax2.text(bar_left + seg1_width / 2 + 0.05, bar_y + 0.2,
         "Early Decisions",
         ha="center", va="center",
         fontsize=10, fontweight="bold", color=ALERT_RED, zorder=3)
ax2.text(bar_left + seg1_width / 2 + 0.05, bar_y - 0.2,
         "Fading from context",
         ha="center", va="center",
         fontsize=9, color=ALERT_RED, alpha=0.8, zorder=3)

# Segment 2: Middle work (still visible but compressed)
seg2_left = bar_left + seg1_width + 0.1
seg2_width = bar_width * 0.3
seg2_box = FancyBboxPatch(
    (seg2_left, bar_y - bar_height / 2 + 0.05),
    seg2_width, bar_height - 0.1,
    boxstyle="round,pad=0.06",
    facecolor="#FFF9EC", edgecolor=GOLDEN_YELLOW,
    linewidth=1.5, zorder=2
)
ax2.add_patch(seg2_box)
ax2.text(seg2_left + seg2_width / 2, bar_y + 0.2,
         "Middle Work",
         ha="center", va="center",
         fontsize=10, fontweight="bold", color=DEEP_NAVY, zorder=3)
ax2.text(seg2_left + seg2_width / 2, bar_y - 0.2,
         "Losing detail",
         ha="center", va="center",
         fontsize=9, color=OCEAN_TEAL, zorder=3)

# Segment 3: Recent messages (clear)
seg3_left = seg2_left + seg2_width + 0.1
seg3_width = bar_width * 0.35
seg3_box = FancyBboxPatch(
    (seg3_left, bar_y - bar_height / 2 + 0.05),
    seg3_width, bar_height - 0.1,
    boxstyle="round,pad=0.06",
    facecolor="#E8F8F7", edgecolor=BRIGHT_TEAL,
    linewidth=1.5, zorder=2
)
ax2.add_patch(seg3_box)
ax2.text(seg3_left + seg3_width / 2, bar_y + 0.2,
         "Recent Messages",
         ha="center", va="center",
         fontsize=10, fontweight="bold", color=DEEP_NAVY, zorder=3)
ax2.text(seg3_left + seg3_width / 2, bar_y - 0.2,
         "Clear and active",
         ha="center", va="center",
         fontsize=9, color=SEA_GREEN, zorder=3)

# Label: "Context Window"
ax2.annotate("Context Window",
             xy=(bar_left, bar_y + bar_height / 2 + 0.1),
             xytext=(bar_left, bar_y + bar_height / 2 + 0.1),
             fontsize=10, fontweight="bold", color=DEEP_NAVY)
ax2.annotate("",
             xy=(bar_right, bar_y + bar_height / 2 + 0.15),
             xytext=(bar_left + 2.3, bar_y + bar_height / 2 + 0.15),
             arrowprops=dict(arrowstyle="->", color=DEEP_NAVY, lw=1.5))

# Three failure scenarios below
scenarios = [
    ("Session Timeout", "Everything disappears", ALERT_RED),
    ("New Session", "Zero memory of prior work", ALERT_RED),
    ("Long Conversation", "Early details lost", GOLDEN_YELLOW),
]

scenario_y = 2.2
for i, (title, desc, color) in enumerate(scenarios):
    sx = 2.0 + i * 3.3
    box = FancyBboxPatch(
        (sx - 1.3, scenario_y - 0.45), 2.6, 0.9,
        boxstyle="round,pad=0.1",
        facecolor=WHITE, edgecolor=color,
        linewidth=2, zorder=2
    )
    ax2.add_patch(box)
    ax2.text(sx, scenario_y + 0.1, title,
             ha="center", va="center",
             fontsize=10, fontweight="bold", color=DEEP_NAVY, zorder=3)
    ax2.text(sx, scenario_y - 0.2, desc,
             ha="center", va="center",
             fontsize=9, color=OCEAN_TEAL, zorder=3)

# Bottom callout
ax2.text(6, 1.0,
         "Chat history is not project memory.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, fontweight="bold", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor=GOLDEN_YELLOW, linewidth=2.0),
         zorder=5)

out_path2 = os.path.join(OUT_DIR, "08_context_problem.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 08_context_problem.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 03 – The Three-File External Memory System
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(12, 9))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 12)
ax3.set_ylim(0, 9)
ax3.axis("off")

# Title
ax3.text(6, 8.5, "The External Memory System",
         ha="center", va="center",
         fontsize=18, fontweight="bold", color=DEEP_NAVY)
ax3.text(6, 8.0, "Three files that survive session resets",
         ha="center", va="center",
         fontsize=11, color=OCEAN_TEAL, fontstyle="italic")

# Three file cards at the top
files = [
    ("plan.md", "The Blueprint", "Objective, rules,\nsteps, constraints",
     OCEAN_TEAL, WHITE),
    ("status_update.md", "The Save Button", "Completed, outputs,\nissues, next steps",
     GOLDEN_YELLOW, DEEP_NAVY),
    ("CLAUDE.md", "The Instructor", "Behavior rules,\nsession startup, guardrails",
     BRIGHT_TEAL, WHITE),
]

card_width = 2.8
card_height = 2.4
card_y = 5.5
card_positions = [1.8, 4.6, 7.4]

for i, (fname, subtitle, desc, bg, fg) in enumerate(files):
    cx = card_positions[i]

    # Card background
    card = FancyBboxPatch(
        (cx - card_width / 2, card_y - card_height / 2),
        card_width, card_height,
        boxstyle="round,pad=0.12",
        facecolor=bg, edgecolor=DEEP_NAVY,
        linewidth=2, zorder=2
    )
    ax3.add_patch(card)

    # File name
    ax3.text(cx, card_y + 0.65, fname,
             ha="center", va="center",
             fontsize=12, fontweight="bold", fontfamily="monospace",
             color=fg, zorder=3)

    # Subtitle
    ax3.text(cx, card_y + 0.15, subtitle,
             ha="center", va="center",
             fontsize=11, fontstyle="italic",
             color=fg, alpha=0.9, zorder=3)

    # Description
    ax3.text(cx, card_y - 0.55, desc,
             ha="center", va="center",
             fontsize=9, color=fg, alpha=0.85,
             linespacing=1.4, zorder=3)

# Arrows from all three cards pointing down to Claude
arrow_target_y = 2.8
for cx in card_positions:
    ax3.annotate("",
                 xy=(6, arrow_target_y + 0.5),
                 xytext=(cx, card_y - card_height / 2 - 0.1),
                 arrowprops=dict(arrowstyle="-|>", color=DEEP_NAVY,
                                 lw=2, mutation_scale=18,
                                 connectionstyle="arc3,rad=0"),
                 zorder=4)

# Claude session box in the center bottom
claude_width = 4.0
claude_height = 1.2
claude_cx = 6.0
claude_cy = 2.2

claude_box = FancyBboxPatch(
    (claude_cx - claude_width / 2, claude_cy - claude_height / 2),
    claude_width, claude_height,
    boxstyle="round,pad=0.12",
    facecolor=DEEP_NAVY, edgecolor=BRIGHT_TEAL,
    linewidth=2.5, zorder=2
)
ax3.add_patch(claude_box)
ax3.text(claude_cx, claude_cy + 0.2, "Claude Session",
         ha="center", va="center",
         fontsize=13, fontweight="bold", color=BRIGHT_TEAL, zorder=3)
ax3.text(claude_cx, claude_cy - 0.2, "Reads files at start, updates as work progresses",
         ha="center", va="center",
         fontsize=9, color=WHITE, alpha=0.85, zorder=3)

# Update arrow going back up to status_update.md
ax3.annotate("",
             xy=(card_positions[1], card_y - card_height / 2 - 0.1),
             xytext=(claude_cx + 0.3, claude_cy + claude_height / 2 + 0.05),
             arrowprops=dict(arrowstyle="-|>", color=GOLDEN_YELLOW,
                             lw=2.5, mutation_scale=18,
                             connectionstyle="arc3,rad=-0.3",
                             linestyle="--"),
             zorder=4)
ax3.text(8.2, 3.6, "updates",
         ha="center", va="center",
         fontsize=9, fontweight="bold", color=GOLDEN_YELLOW,
         fontstyle="italic", zorder=5)

# Bottom callout
ax3.text(6, 0.6,
         "AI is not your memory -- your files are.",
         ha="center", va="center",
         fontsize=12, color=DEEP_NAVY, fontweight="bold", fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor=GOLDEN_YELLOW, linewidth=2.0),
         zorder=5)

out_path3 = os.path.join(OUT_DIR, "08_external_memory.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 08_external_memory.png  ->  {OUT_DIR}")
