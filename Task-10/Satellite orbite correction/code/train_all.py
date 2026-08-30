from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from environment import SatelliteOrbitEnv
import os

os.makedirs("models", exist_ok=True)
os.makedirs("logs",   exist_ok=True)

experiments = [
    ("SAC", "naive"),
    ("SAC", "fuel_aware"),
    ("SAC", "shaped"),
]

for algo, reward in experiments:
    print(f"\n{'='*40}")
    print(f"  {algo} + {reward}")
    print(f"{'='*40}\n")

    env = Monitor(
        SatelliteOrbitEnv(reward_mode=reward),
        filename=f"logs/{algo}_{reward}"
    )

    model = SAC(
        "MlpPolicy", env,
        verbose=1,
        learning_rate=3e-4,
        batch_size=64,
        learning_starts=500
    )

    model.learn(total_timesteps=30_000)
    model.save(f"models/{algo}_{reward}")
    print(f"✓ Done: {algo} + {reward}")

print("\nSAC experiments complete!")