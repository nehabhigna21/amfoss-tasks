from stable_baselines3 import PPO, SAC
from environment import SatelliteOrbitEnv
import numpy as np

experiments = [
    ("PPO", "naive"),
    ("PPO", "fuel_aware"),
    ("PPO", "shaped"),
    ("SAC", "naive"),
    ("SAC", "fuel_aware"),
    ("SAC", "shaped"),
]

print("\n" + "="*65)
print(f"{'Model':<20} {'Success':>8} {'Pos Error':>12} {'Fuel Used':>10}")
print("="*65)

for algo, reward in experiments:
    try:
        if algo == "PPO":
            model = PPO.load(f"models/{algo}_{reward}")
        else:
            model = SAC.load(f"models/{algo}_{reward}")

        env       = SatelliteOrbitEnv(reward_mode=reward)
        successes = 0
        errors    = []
        fuels     = []

        for _ in range(20):
            obs, _ = env.reset()
            for step in range(200):
                action, _ = model.predict(obs, deterministic=True)
                obs, _, terminated, truncated, info = env.step(action)
                if terminated or truncated:
                    if info["success"]:
                        successes += 1
                    errors.append(info["pos_error"])
                    fuels.append(env.max_fuel - info["fuel_remaining"])
                    break

        name = f"{algo} + {reward}"
        print(f"{name:<20} {successes}/20 {np.mean(errors):>12.2f} km "
              f"{np.mean(fuels):>10.2f}")

    except Exception as e:
        print(f"{algo} + {reward:<15} ERROR: {e}")

print("="*65)