from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from environment import SatelliteOrbitEnv

# Create environment
env = Monitor(SatelliteOrbitEnv(reward_mode="shaped"))

# Create PPO agent
model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
)

# Train
print("Training started. Watch ep_rew_mean — it should rise over time.\n")
model.learn(total_timesteps=300_000)

# Save
model.save("satellite_ppo")
print("\nDone! Model saved as satellite_ppo.zip")