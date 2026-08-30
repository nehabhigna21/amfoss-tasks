"""
Proper SAC retraining — 1M timesteps per variant.
Run this overnight. Expected time: ~6-8 hours total depending on your GPU.
"""

from stable_baselines3 import SAC, PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from environment import SatelliteOrbitEnv
import os, time

os.makedirs("models", exist_ok=True)
os.makedirs("logs",   exist_ok=True)

TIMESTEPS = 1_000_000   # 1M — same ballpark as reference paper's 5M but reasonable

experiments = [
    ("SAC", "naive"),
    ("SAC", "fuel_aware"),
    ("SAC", "shaped"),
    # Uncomment below to also retrain PPO with more steps if needed
    # ("PPO", "naive"),
    # ("PPO", "fuel_aware"),
    # ("PPO", "shaped"),
]

for algo, reward in experiments:
    print(f"\n{'='*50}")
    print(f"  Training {algo} + {reward}  ({TIMESTEPS:,} steps)")
    print(f"{'='*50}\n")

    start = time.time()

    env = Monitor(
        SatelliteOrbitEnv(reward_mode=reward),
        filename=f"logs/{algo}_{reward}"
    )

    if algo == "SAC":
        model = SAC(
            "MlpPolicy", env,
            verbose=1,
            learning_rate=3e-4,
            batch_size=256,
            learning_starts=10_000,   # let replay buffer fill before learning
            buffer_size=1_000_000,
            tau=0.005,
            gamma=0.99,
            train_freq=1,
            gradient_steps=1,
            ent_coef="auto",
        )
    else:
        model = PPO(
            "MlpPolicy", env,
            verbose=1,
            learning_rate=3e-4,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            gae_lambda=0.95,
            clip_range=0.2,
        )

    # Save checkpoint every 100k steps so you don't lose progress
    checkpoint = CheckpointCallback(
        save_freq=100_000,
        save_path=f"models/checkpoints/{algo}_{reward}/",
        name_prefix="model"
    )

    model.learn(total_timesteps=TIMESTEPS, callback=checkpoint)
    model.save(f"models/{algo}_{reward}")

    elapsed = time.time() - start
    print(f"\n✓ Done: {algo} + {reward}  ({elapsed/60:.1f} minutes)")

print("\n\nAll training complete!")
print("Models saved in: models/")
print("Logs saved in:   logs/")
