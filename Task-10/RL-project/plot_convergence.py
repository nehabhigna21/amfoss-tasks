import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def load_monitor_csv(log_path):
    """Load reward data directly from monitor CSV file."""
    # Find the CSV file in the log folder
    csv_files = glob.glob(os.path.join(log_path, "*.monitor.csv"))
    
    if not csv_files:
        # Maybe the file IS the path directly
        if os.path.exists(log_path + ".monitor.csv"):
            csv_files = [log_path + ".monitor.csv"]
        else:
            print(f"No CSV found in: {log_path}")
            return None, None

    csv_file = csv_files[0]
    print(f"Loading: {csv_file}")

    try:
        # Skip the first comment line
        df = pd.read_csv(csv_file, skiprows=1)
        rewards    = df['r'].values
        timesteps  = df['t'].values
        return timesteps, rewards
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        return None, None

def smooth(y, window=10):
    if len(y) < window:
        return y
    return np.convolve(y, np.ones(window)/window, mode='valid')

# ─── Check what log files exist ─────────────────────
print("Looking for log files...\n")
for f in glob.glob("logs/*"):
    print(f"  Found: {f}")
print()

# ─── Plot ────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Convergence Curves — PPO vs SAC",
             fontsize=16, fontweight='bold')

ppo_config = [
    ("naive",      "blue",   "--"),
    ("fuel_aware", "green",  "-."),
    ("shaped",     "red",    "-" ),
]

sac_config = [
    ("naive",      "blue",   "--"),
    ("fuel_aware", "green",  "-."),
    ("shaped",     "red",    "-" ),
]

# PPO graph
ax1 = axes[0]
ax1.set_title("PPO — All 3 Reward Functions", fontsize=13)
any_ppo = False

for reward, color, style in ppo_config:
    log_path = f"logs/PPO_{reward}"
    t, r = load_monitor_csv(log_path)
    if r is None:
        continue
    any_ppo  = True
    episodes = np.arange(len(r))
    r_smooth = smooth(r, window=10)
    e_smooth = episodes[len(episodes)-len(r_smooth):]
    ax1.plot(e_smooth, r_smooth,
             color=color, linestyle=style,
             linewidth=2, label=f"PPO + {reward}")

if any_ppo:
    ax1.set_xlabel("Episodes", fontsize=11)
    ax1.set_ylabel("Episode Reward", fontsize=11)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linewidth=0.5)
else:
    ax1.text(0.5, 0.5, "No PPO logs found",
             ha='center', va='center',
             transform=ax1.transAxes, fontsize=12)

# SAC graph
ax2 = axes[1]
ax2.set_title("SAC — All 3 Reward Functions", fontsize=13)
any_sac = False

for reward, color, style in sac_config:
    log_path = f"logs/SAC_{reward}"
    t, r = load_monitor_csv(log_path)
    if r is None:
        continue
    any_sac  = True
    episodes = np.arange(len(r))
    r_smooth = smooth(r, window=10)
    e_smooth = episodes[len(episodes)-len(r_smooth):]
    ax2.plot(e_smooth, r_smooth,
             color=color, linestyle=style,