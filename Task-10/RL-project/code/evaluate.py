from stable_baselines3 import PPO
from environment import SatelliteOrbitEnv
import numpy as np

# Load trained model
model = PPO.load("satellite_ppo")
env   = SatelliteOrbitEnv(reward_mode="shaped")

print("Testing trained agent over 10 episodes...\n")

successes   = 0
total_fuel  = []
total_error = []

for episode in range(10):
    obs, _         = env.reset()
    episode_reward = 0

    for step in range(200):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward

        if terminated or truncated:
            if info["success"]:
                successes += 1
            total_fuel.append(env.max_fuel - info["fuel_remaining"])
            total_error.append(info["pos_error"])
            print(f"Episode {episode+1:2d} | "
                  f"reward: {episode_reward:8.1f} | "
                  f"pos_error: {info['pos_error']:7.2f} km | "
                  f"fuel used: {env.max_fuel - info['fuel_remaining']:.2f} | "
                  f"success: {info['success']}")
            break

print(f"\n--- Summary ---")
print(f"Success rate : {successes}/10")
print(f"Avg fuel used: {np.mean(total_fuel):.2f}")
print(f"Avg pos error: {np.mean(total_error):.2f} km")