"""
Generate Article 04 visuals — AI in Accounting Is Not the Wild West Anymore.

Visual 01: Hero / front image
  Branded title card for the article.

Visual 02: COSO Five Components for Generative AI
  Circular diagram showing the five COSO IC components with GenAI at center.

Visual 03: Traceable AI Workflow
  Horizontal flow: Defined Inputs → Transparent Transformation → Human Review → Evidence Retention.

Saved to articles/04-ai-governance-in-accounting/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
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
ax1.text(6, 3.8, "AI in Accounting Is Not\nthe Wild West Anymore",
         ha="center", va="center",
         fontsize=26, fontweight="bold", color=BRIGHT_TEAL,
         linespacing=1.3)

# Subtitle
ax1.text(6, 2.2, "But It's Also Not Plug-and-Play",
         ha="center", va="center",
         fontsize=16, color=GOLDEN_YELLOW, fontstyle="italic")

# Divider line
ax1.plot([3, 9], [1.5, 1.5], color=OCEAN_TEAL, linewidth=2)

# Byline
ax1.text(6, 0.9, "PythonMuse  |  By Svetlana Toohey",
         ha="center", va="center",
         fontsize=11, color=WHITE, alpha=0.7)

out_path1 = os.path.join(OUT_DIR, "04_visual_front.png")
plt.savefig(out_path1, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 04_visual_front.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 02 – COSO Five Components for Generative AI
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(12, 12))
fig2.patch.set_facecolor(WHITE)
ax2.set_facecolor(WHITE)
ax2.set_xlim(-6.5, 6.5)
ax2.set_ylim(-6.5, 7.0)
ax2.set_aspect("equal")
ax2.axis("off")

# Title
ax2.text(0, 6.5, "COSO Internal Control Components",
         ha="center", va="center",
         fontsize=20, fontweight="bold", color=DEEP_NAVY)
ax2.text(0, 5.9, "Applied to Generative AI Governance",
         ha="center", va="center",
         fontsize=14, color=OCEAN_TEAL, fontstyle="italic")

# Center circle – Generative AI
center_circle = plt.Circle((0, 0), 1.4, facecolor=DEEP_NAVY,
                            edgecolor=BRIGHT_TEAL, linewidth=3, zorder=5)
ax2.add_patch(center_circle)
ax2.text(0, 0.2, "Generative", ha="center", va="center",
         fontsize=15, fontweight="bold", color=BRIGHT_TEAL, zorder=6)
ax2.text(0, -0.35, "AI", ha="center", va="center",
         fontsize=15, fontweight="bold", color=BRIGHT_TEAL, zorder=6)

# Five components around the center — titles and descriptions combined inside
components = [
    ("Control\nEnvironment",         "Ownership, governance\npolicies, oversight"),
    ("Risk\nAssessment",             "Prompt manipulation,\nmodel drift, data leakage"),
    ("Control\nActivities",          "Approval workflows,\nvalidation, access controls"),
    ("Information &\nCommunication", "Traceability of inputs\nand outputs"),
    ("Monitoring\nActivities",       "Performance evaluation,\ndetect unexpected behavior"),
]

colors = [BRIGHT_TEAL, GOLDEN_YELLOW, SEA_GREEN, SOFT_SAGE, OCEAN_TEAL]
text_colors = [WHITE, DEEP_NAVY, WHITE, DEEP_NAVY, WHITE]
desc_colors = [WHITE, DEEP_NAVY, WHITE, DEEP_NAVY, WHITE]
radius = 3.6
bubble_r = 1.55
angles = [90, 162, 234, 306, 18]

for i, (title, desc) in enumerate(components):
    angle_rad = np.radians(angles[i])
    cx = radius * np.cos(angle_rad)
    cy = radius * np.sin(angle_rad)

    # Component circle — larger to fit description inside
    comp_circle = plt.Circle((cx, cy), bubble_r, facecolor=colors[i],
                              edgecolor=DEEP_NAVY, linewidth=2, zorder=3)
    ax2.add_patch(comp_circle)

    # Component title (upper half of bubble)
    ax2.text(cx, cy + 0.4, title, ha="center", va="center",
             fontsize=11, fontweight="bold", color=text_colors[i],
             linespacing=1.1, zorder=4)

    # Description (lower half of bubble, smaller)
    ax2.text(cx, cy - 0.6, desc, ha="center", va="center",
             fontsize=8, color=desc_colors[i], alpha=0.85,
             linespacing=1.2, zorder=4)

    # Connector line from center to component
    inner_r = 1.45
    outer_r = radius - bubble_r + 0.05
    x1 = inner_r * np.cos(angle_rad)
    y1 = inner_r * np.sin(angle_rad)
    x2 = outer_r * np.cos(angle_rad)
    y2 = outer_r * np.sin(angle_rad)
    ax2.plot([x1, x2], [y1, y2], color=GRAY_LINE, linewidth=1.5,
             linestyle="--", zorder=1)

out_path2 = os.path.join(OUT_DIR, "04_coso_five_components.png")
plt.savefig(out_path2, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 04_coso_five_components.png  ->  {OUT_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# Visual 03 – Traceable AI Workflow
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(14, 6))
fig3.patch.set_facecolor(WHITE)
ax3.set_facecolor(WHITE)
ax3.set_xlim(0, 14)
ax3.set_ylim(0, 6)
ax3.axis("off")

# Title
ax3.text(7, 5.5, "Structuring AI Workflows for Audit-Ready Evidence",
         ha="center", va="center",
         fontsize=17, fontweight="bold", color=DEEP_NAVY)
ax3.text(7, 5.0, "Every output must be traceable",
         ha="center", va="center",
         fontsize=12, color=OCEAN_TEAL, fontstyle="italic")

# Four workflow steps
steps = [
    ("1. Defined\nInputs",           "GL exports, contracts,\nbank files, recon data",  BRIGHT_TEAL),
    ("2. Transparent\nTransformation", "What was asked?\nWhat data provided?\nWhat output generated?", SEA_GREEN),
    ("3. Human\nReview",              "AI assists.\nHumans approve\nfinal conclusions.",  GOLDEN_YELLOW),
    ("4. Evidence\nRetention",        "Source data +\nprocess + output +\nhuman sign-off", OCEAN_TEAL),
]

box_width = 2.6
box_height = 2.8
y_center = 2.5
x_positions = [1.2, 4.4, 7.6, 10.8]

for i, (title, desc, color) in enumerate(steps):
    x = x_positions[i]

    # Box
    box = FancyBboxPatch(
        (x, y_center - box_height / 2), box_width, box_height,
        boxstyle="round,pad=0.15",
        facecolor=color, edgecolor=DEEP_NAVY, linewidth=2, zorder=2
    )
    ax3.add_patch(box)

    # Determine text color based on background
    txt_color = DEEP_NAVY if color in [GOLDEN_YELLOW, WARM_GLOW, SOFT_SAGE] else WHITE

    # Title
    ax3.text(x + box_width / 2, y_center + 0.65, title,
             ha="center", va="center",
             fontsize=12, fontweight="bold", color=txt_color,
             linespacing=1.2, zorder=3)

    # Description
    ax3.text(x + box_width / 2, y_center - 0.55, desc,
             ha="center", va="center",
             fontsize=9, color=txt_color, alpha=0.9,
             linespacing=1.3, zorder=3)

    # Arrow between boxes
    if i < 3:
        arrow_x_start = x + box_width + 0.05
        arrow_x_end = x_positions[i + 1] - 0.05
        ax3.annotate("",
                     xy=(arrow_x_end, y_center),
                     xytext=(arrow_x_start, y_center),
                     arrowprops=dict(arrowstyle="-|>", color=GOLDEN_YELLOW,
                                     lw=3, mutation_scale=25),
                     zorder=4)

# Bottom callout
ax3.text(7, 0.45,
         '"How do you know this number is correct?"  —  If you can show all four steps, the result is defensible evidence.',
         ha="center", va="center",
         fontsize=10.5, color=DEEP_NAVY, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.45",
                   facecolor="#FFF9EC", edgecolor=GOLDEN_YELLOW, linewidth=2.0),
         zorder=5)

out_path3 = os.path.join(OUT_DIR, "04_traceable_workflow.png")
plt.savefig(out_path3, dpi=180, bbox_inches="tight")
plt.close()
print(f"[OK] 04_traceable_workflow.png  ->  {OUT_DIR}")
