from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from environment import SatelliteOrbitEnv

print("Retraining SAC with more steps...\n")

# Train all 3 SAC reward versions with more time
experiments = [
    "naive",
    "fuel_aware", 
    "shaped",
]

for reward in experiments:
    print(f"\n{'='*40}")
    print(f"  SAC + {reward} (200k steps)")
    print(f"{'='*40}\n")

    env = Monitor(
        SatelliteOrbitEnv(reward_mode=reward),
        filename=f"logs/SAC_{reward}_long"
    )

    model = SAC(
        "MlpPolicy", env,
        verbose=1,
        learning_rate=3e-4,
        batch_size=64,
        learning_starts=500
    )

    model.learn(total_timesteps=200_000)
    model.save(f"models/SAC_{reward}_long")
    print(f"✓ Done: SAC + {reward}")

print("\nSAC retrain complete!")