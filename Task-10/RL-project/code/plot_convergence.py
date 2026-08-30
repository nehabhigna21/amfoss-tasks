import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def load_monitor_csv(csv_path):
    try:
        # Monitor CSV has a comment line at top, skip it
        df = pd.read_csv(csv_path, skiprows=1)
        print(f"  Columns: {list(df.columns)}")
        print(f"  Rows: {len(df)}")
        rewards = df.iloc[:, 0].values  # first column = reward
        return rewards
    except Exception as e:
        print(f"  Error: {e}")
        return None

def smooth(y, window=15):
    if len(y) < window:
        return y
    return np.convolve(y, np.ones(window)/window, mode='valid')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Convergence Curves — PPO vs SAC",
             fontsize=16, fontweight='bold')

configs = [
    ("naive",      "blue",   "--"),
    ("fuel_aware", "green",  "-."),
    ("shaped",     "red",    "-" ),
]

for ax, algo in zip(axes, ["PPO", "SAC"]):
    ax.set_title(f"{algo} — All 3 Reward Functions", fontsize=13)
    any_data = False

    for reward, color, style in configs:
        csv_path = f"logs/{algo}_{reward}.monitor.csv"
        print(f"\nLoading {csv_path}")

        if not os.path.exists(csv_path):
            print(f"  File not found")
            continue

        rewards = load_monitor_csv(csv_path)
        if rewards is None or len(rewards) == 0:
            print(f"  Empty data")
            continue

        print(f"  Reward range: {rewards.min():.1f} to {rewards.max():.1f}")
        any_data = True
        episodes = np.arange(len(rewards))
        r_smooth = smooth(rewards, window=15)
        e_smooth = episodes[len(episodes)-len(r_smooth):]

        ax.plot(e_smooth, r_smooth,
                color=color,
                linestyle=style,
                linewidth=2,
                label=f"{algo} + {reward}")

    if any_data:
        ax.set_xlabel("Episodes", fontsize=11)
        ax.set_ylabel("Episode Reward", fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linewidth=0.5)
    else:
        ax.text(0.5, 0.5, f"No {algo} data found",
                ha='center', va='center',
                transform=ax.transAxes, fontsize=12)

os.makedirs("results", exist_ok=True)
plt.tight_layout()
plt.savefig("results/convergence_curves.png",
            dpi=150, bbox_inches='tight')
plt.show()
print("\nSaved: results/convergence_curves.png")