"""Render the LTK Agentic Marketplace high-level architecture diagram.

Pure matplotlib so it runs anywhere. Output: docs/architecture.png

Color key
  blue   = exists at LTK today
  orange = LTK would build
  gray   = external (hosts, platforms, retailers)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "architecture.png"

BLUE_F, BLUE_E = "#dbeafe", "#1d4ed8"
ORNG_F, ORNG_E = "#ffedd5", "#c2410c"
GRAY_F, GRAY_E = "#f3f4f6", "#6b7280"
HUMAN_F, HUMAN_E = "#ffffff", "#111827"
TEXT = "#111827"
SUB = "#4b5563"


def box(ax, x, y, w, h, kind, title, sub=None, *, fs=10.5, dashed=False):
    f, e = {"blue": (BLUE_F, BLUE_E), "orange": (ORNG_F, ORNG_E),
            "gray": (GRAY_F, GRAY_E), "human": (HUMAN_F, HUMAN_E)}[kind]
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.6",
        linewidth=1.6, facecolor=f, edgecolor=e,
        linestyle="--" if dashed else "-"))
    if sub:
        ax.text(x + w / 2, y + h / 2 + 0.75, title, ha="center", va="center",
                color=TEXT, fontsize=fs, fontweight="bold")
        ax.text(x + w / 2, y + h / 2 - 0.95, sub, ha="center", va="center",
                color=SUB, fontsize=fs - 2.2, linespacing=1.15)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                color=TEXT, fontsize=fs, fontweight="bold")


def panel(ax, x, y, w, h, label, edge):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.8",
        linewidth=1.4, facecolor="none", edgecolor=edge, linestyle=(0, (5, 4))))
    ax.text(x + 1.2, y + h - 1.1, label, ha="left", va="center",
            color=edge, fontsize=10, fontweight="bold")


def arrow(ax, p, q, label=None, *, color="#374151", rad=0.0, lw=1.5, lpos=0.5, dx=0, dy=0):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=2, shrinkB=2))
    if label:
        lx = p[0] + (q[0] - p[0]) * lpos + dx
        ly = p[1] + (q[1] - p[1]) * lpos + dy
        ax.text(lx, ly, label, ha="center", va="center", fontsize=8.6,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.95))


def main() -> None:
    fig, ax = plt.subplots(figsize=(18, 12.2), dpi=150)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70.5)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(50, 68.8, "LTK Agentic Marketplace — high-level architecture",
            ha="center", va="center", fontsize=17, fontweight="bold", color=TEXT)
    ax.text(50, 66.9, "Every creator and every brand gets an agent. LTK runs the market between them and keeps attribution intact when agents, not humans, transact.",
            ha="center", va="center", fontsize=10.5, color=SUB)

    # ---- Row A: external hosts -------------------------------------------
    panel(ax, 2, 55.2, 96, 7.3, "WHERE THE AGENTS ARE USED  (external hosts — people talk to their agent here)", GRAY_E)
    hosts = [("ChatGPT", "Apps SDK · custom UI"),
             ("Glean", "internal ops & BD view"),
             ("Claude / Cursor", "developer & power users"),
             ("Personal agents", "Meta · OpenAI · Instinct\nvia Personal Agent Protocol (Poppy)"),
             ("LTK apps", "Creator app · Brand Platform\n(hosted 'bowling-shoe' agent)")]
    hw, gap, x0 = 17.2, 1.9, 3.3
    for i, (t, s) in enumerate(hosts):
        kind = "blue" if t == "LTK apps" else "gray"
        box(ax, x0 + i * (hw + gap), 56.1, hw, 4.9, kind, t, s, fs=10.5)

    # ---- Row B: humans + agents + core ------------------------------------
    box(ax, 2, 47.4, 22, 4.6, "human", "Creator", "sets policy once · approves from the lock screen")
    box(ax, 2, 39.4, 22, 6.6, "orange", "Creator Agent",
        "business partner, negotiator, ops staff\nlearns from posts, links, sales, social, calendar")

    box(ax, 76, 47.4, 22, 4.6, "human", "Brand", "writes a brief · deploys a budget")
    box(ax, 76, 39.4, 22, 6.6, "orange", "Brand Agent",
        "turns the brief into a mandate\nallocates budget across creators in parallel")

    panel(ax, 27, 29.4, 46, 24.6, "LTK AGENTIC MARKETPLACE CORE  (new)", ORNG_E)
    box(ax, 28.5, 46.4, 43, 4.6, "orange", "Agent Gateway",
        "MCP server for hosts · Poppy endpoint for external personal agents · scoped delegation tokens")
    box(ax, 28.5, 39.4, 21, 6.0, "orange", "Negotiation Protocol + Referee",
        "typed offers · floor & max-share checks\nblocks money-losing deals · signs settlements")
    box(ax, 50.5, 39.4, 21, 6.0, "orange", "Agent Memory + Policy Store",
        "floors, standing rules, brand affinity\nwhat each creator has sold and posted")
    box(ax, 28.5, 32.4, 21, 5.8, "orange", "Expected-Value Engine",
        "content bank first · ask the human only\nwhen fee + commission beats their time")
    box(ax, 50.5, 32.4, 21, 5.8, "orange", "Settlement, Escrow + Micro-ledger",
        "flat fee per deliverable on go-live\ncommission per attributed order · bonus pools")

    # ---- Row C: inputs each side ------------------------------------------
    box(ax, 2, 31.6, 10.4, 5.4, "blue", "LTK\nCreator app", fs=9.8)
    box(ax, 13.6, 31.6, 10.4, 5.4, "gray", "Instagram\nTikTok", fs=9.8)
    box(ax, 2, 24.6, 22, 5.4, "orange", "Content Bank Index", "every past post, reel, story and link\ntagged by brand and product")

    box(ax, 76, 31.6, 22, 5.4, "blue", "LTK Brand Platform", "brand accounts · programs · briefs")
    box(ax, 76, 24.6, 22, 5.4, "blue", "Campaigns + Collaborations", "deals, obligations, payouts (existing service)")

    # ---- Row D: existing LTK rails -----------------------------------------
    panel(ax, 2, 10.0, 96, 13.2, "EXISTING LTK RAILS  (the marketplace plugs into these; nothing here is replaced)", BLUE_E)
    box(ax, 3.3, 17.4, 93.4, 4.3, "orange", "Attribution Credential Service",
        "signs an 'influence credential' onto every link/click so the creator is credited even when a shopper's agent completes the purchase")
    rails = [("rstyle.me Link Service", "links_link"),
             ("Clicks Pipeline", "clicks_performance"),
             ("Orders + Sales Attribution", "denormalized_orders"),
             ("Creator Payouts", "campaign_influencer_payout"),
             ("Product Catalog", "catalog ingestion"),
             ("Athena Data Lake", "prod-rs-datalake-curated")]
    rw, rg, rx0 = 14.6, 1.16, 3.3
    for i, (t, s) in enumerate(rails):
        x = rx0 + i * (rw + rg)
        box(ax, x, 11.0, rw, 5.4, "blue", t, s, fs=9.4)

    # ---- Row E: outside commerce -------------------------------------------
    box(ax, 2, 1.6, 30, 5.2, "gray", "Shopper  (or the shopper's personal agent)", "follows the creator · clicks · buys")
    box(ax, 35, 1.6, 30, 5.2, "gray", "Retailers + Affiliate Networks", "Walmart · Target · Amazon · Shopify · Rakuten · Impact")
    box(ax, 68, 1.6, 30, 5.2, "gray", "Payment Rails", "Stripe / existing payout partners")

    # ---- Arrows (numbered to match the prototype's six scenes) -----------
    A = "#374151"
    arrow(ax, (50, 56.1), (50, 51.0), color=GRAY_E, lw=1.3)            # hosts -> gateway
    arrow(ax, (13, 47.4), (13, 46.0), color=A, lw=1.2)                  # creator -> agent
    arrow(ax, (87, 47.4), (87, 46.0), color=A, lw=1.2)                  # brand -> agent
    arrow(ax, (76, 45.0), (71.5, 48.2), "1  mandate + $", color=ORNG_E, dy=-0.7, dx=0)
    arrow(ax, (24, 45.0), (28.5, 48.2), "2  packages", color=ORNG_E, dy=-0.7, dx=0)
    arrow(ax, (47.5, 39.4), (53.0, 38.2), "3→4  settle", color=ORNG_E, dx=4.5, dy=0.3)
    arrow(ax, (7.2, 37.0), (9.5, 39.4), color=BLUE_E, lw=1.2)           # creator app -> agent
    arrow(ax, (18.8, 37.0), (16.5, 39.4), color=GRAY_E, lw=1.2)         # social -> agent
    arrow(ax, (24, 27.8), (28.5, 33.6), "5  bank first,\nthen ask the human", color=ORNG_E, dx=8.5, dy=-2.4)
    arrow(ax, (87, 31.6), (87, 30.0), color=BLUE_E, lw=1.2)             # brand platform -> campaigns
    arrow(ax, (76, 28.0), (71.5, 33.6), color=BLUE_E, lw=1.2)           # campaigns <-> settlement
    arrow(ax, (61, 21.7), (61, 32.4), "6  $ per verified order\n→ micro-ledger", color=BLUE_E, dx=7.2)
    arrow(ax, (10.6, 16.4), (10.6, 17.4), color=ORNG_E, lw=1.2)         # credential onto links
    arrow(ax, (26.4, 16.4), (26.4, 17.4), color=ORNG_E, lw=1.2)         # credential onto clicks
    arrow(ax, (42, 16.4), (42, 17.4), color=BLUE_E, lw=1.2)             # orders -> credential verify
    arrow(ax, (17, 6.8), (10.6, 11.0), "click", color=GRAY_E, lw=1.2, dy=0.5, dx=1.6)
    arrow(ax, (50, 6.8), (42, 11.0), "order", color=GRAY_E, lw=1.2, dy=0.5, dx=1.8)
    arrow(ax, (57.5, 11.0), (83, 6.8), "payout", color=BLUE_E, lw=1.2, dy=0.7)

    # ---- Legend -------------------------------------------------------------
    lx, ly = 19.5, 64.3
    for i, (f, e, t) in enumerate([(BLUE_F, BLUE_E, "exists at LTK today"),
                                   (ORNG_F, ORNG_E, "LTK would build"),
                                   (GRAY_F, GRAY_E, "external system / partner"),
                                   (HUMAN_F, HUMAN_E, "human")]):
        xx = lx + i * 15.5
        ax.add_patch(mpatches.FancyBboxPatch((xx, ly - 0.5), 2.2, 1.1, boxstyle="round,pad=0.02", fc=f, ec=e, lw=1.4))
        ax.text(xx + 2.9, ly, t, va="center", fontsize=9.2, color=TEXT)

    fig.savefig(OUT, bbox_inches="tight", facecolor="white")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
