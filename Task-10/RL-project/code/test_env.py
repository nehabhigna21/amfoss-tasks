from environment import SatelliteOrbitEnv

# Create environment
env = SatelliteOrbitEnv(reward_mode="shaped")

# Reset environment
obs, info = env.reset()

print(f"Curriculum level: {env.curriculum_level}")
print(f"First observation: {obs}")
print(f"Observation shape: {obs.shape}")
print("\nRunning 5 random steps...\n")

# Run some steps
for i in range(5):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    print(f"Step {i+1}")
    print(f"Reward: {reward:.3f} | Pos error: {info['pos_error']:.2f} km | Fuel: {info['fuel_remaining']:.2f}")

    if terminated or truncated:
        print("Episode ended early.")
        break