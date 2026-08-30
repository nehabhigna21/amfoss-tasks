"""
Generate all figures for the paper.
Run this AFTER evaluate_robustness.py has completed.

Produces:
  results/fig1_convergence.png     — training curves PPO vs SAC
  results/fig2_success_rate.png    — success rate vs disturbance level
  results/fig3_fuel_usage.png      — fuel consumption vs disturbance level
  results/fig4_pos_error.png       — position error vs disturbance level
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os, glob

os.makedirs("results", exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family"  : "serif",
    "font.size"    : 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi"   : 150,
})

COLORS = {
    "naive"     : "#2196F3",   # blue
    "fuel_aware": "#4CAF50",   # green
    "shaped"    : "#F44336",   # red
}
STYLES = {
    "PPO": "-",
    "SAC": "--",
}
MARKERS = {
    "naive"     : "o",
    "fuel_aware": "s",
    "shaped"    : "^",
}

# ── Figure 1: Convergence Curves ─────────────────────────────────────────────
def load_monitor(path):
    try:
        df = pd.read_csv(path, skiprows=1)
        return df["r"].values
    except:
        return None

def smooth(y, w=30):
    if len(y) < w:
        return y
    return np.convolve(y, np.ones(w)/w, mode="valid")

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
fig.suptitle("Figure 1 — Training Convergence Curves", fontweight="bold")

for ax, algo in zip(axes, ["PPO", "SAC"]):
    ax.set_title(f"{algo}")
    any_data = False
    for reward in ["naive", "fuel_aware", "shaped"]:
        # Try both naming conventions
        for pattern in [
            f"logs/{algo}_{reward}.monitor.csv",
            f"logs/{algo}_{reward}/*.monitor.csv",
        ]:
            paths = glob.glob(pattern)
            if paths:
                r = load_monitor(paths[0])
                if r is not None and len(r) > 0:
                    rs = smooth(r, w=30)
                    ep = np.arange(len(rs))
                    ax.plot(ep, rs,
                            color=COLORS[reward],
                            linewidth=2,
                            label=f"{reward.replace('_',' ')}")
                    any_data = True
                    break

    ax.set_xlabel("Episode")
    ax.set_ylabel("Episode Reward")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.5, linestyle=":")
    if not any_data:
        ax.text(0.5, 0.5, f"No {algo} logs found\n(run training first)",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=10, color="gray")

plt.tight_layout()
plt.savefig("results/fig1_convergence.png", bbox_inches="tight")
plt.close()
print("✓ Saved: results/fig1_convergence.png")


# ── Figures 2-4: Robustness Results ─────────────────────────────────────────
if not os.path.exists("results/robustness_results.csv"):
    print("\n⚠ robustness_results.csv not found.")
    print("  Run evaluate_robustness.py first, then re-run this script.")
else:
    df = pd.read_csv("results/robustness_results.csv")

    dist_order  = ["None", "Mild", "Moderate", "Strong", "Extreme"]
    dist_labels = ["None\n(×0)", "Mild\n(×1)", "Moderate\n(×5)",
                   "Strong\n(×15)", "Extreme\n(×30)"]
    x = np.arange(len(dist_order))

    metrics = [
        ("Success_Rate",     "Success Rate",          "fig2_success_rate.png",  True),
        ("Avg_Fuel_Used",    "Average Fuel Used",      "fig3_fuel_usage.png",    False),
        ("Avg_Pos_Error_km", "Average Position Error (km)", "fig4_pos_error.png", False),
    ]

    for col, ylabel, fname, is_rate in metrics:
        fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=False)
        fig.suptitle(f"{ylabel} vs Disturbance Level", fontweight="bold")

        for ax, algo in zip(axes, ["PPO", "SAC"]):
            ax.set_title(algo)
            sub = df[df["Algorithm"] == algo]

            for reward in ["naive", "fuel_aware", "shaped"]:
                row = sub[sub["Reward"] == reward]
                if row.empty:
                    continue
                row = row.set_index("Disturbance").reindex(dist_order)
                vals = row[col].values

                ax.plot(x, vals,
                        color=COLORS[reward],
                        marker=MARKERS[reward],
                        linewidth=2,
                        markersize=7,
                        label=reward.replace("_", " "))

            ax.set_xticks(x)
            ax.set_xticklabels(dist_labels)
            ax.set_xlabel("Disturbance Level")
            ax.set_ylabel(ylabel)
            ax.legend()
            ax.grid(True, alpha=0.3)

            if is_rate:
                ax.set_ylim(-0.05, 1.05)
                ax.yaxis.set_major_formatter(
                    ticker.FuncFormatter(lambda v, _: f"{v*100:.0f}%"))

        plt.tight_layout()
        plt.savefig(f"results/{fname}", bbox_inches="tight")
        plt.close()
        print(f"✓ Saved: results/{fname}")

    # ── Summary table ────────────────────────────────────────────────────────
    print("\n── Robustness Summary Table ──────────────────────────────────")
    pivot = df.pivot_table(
        index=["Algorithm", "Reward"],
        columns="Disturbance",
        values="Success_Rate"
    )[dist_order]
    pivot.columns.name = None
    pivot = pivot * 100
    print(pivot.round(1).to_string())
    pivot.round(1).to_csv("results/table_success_rates.csv")
    print("\nTable saved: results/table_success_rates.csv")

print("\nAll figures generated in: results/")
