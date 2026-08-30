"""
Disturbance Robustness Evaluation
===================================
Takes all 6 trained models and tests them under 4 disturbance levels
they were NEVER trained on. This is the core experiment of the paper.

Disturbance = scaling factor applied to j2_drift in the environment.
- Level 0 (none):     scale = 0.0   (no drift, clean conditions)
- Level 1 (mild):     scale = 1.0   (normal j2 drift, training conditions)
- Level 2 (moderate): scale = 5.0   (5x stronger drift)
- Level 3 (strong):   scale = 15.0  (15x stronger drift)
- Level 4 (extreme):  scale = 30.0  (30x — well outside training distribution)

Results saved to: results/robustness_results.csv
"""

import numpy as np
import pandas as pd
import os
from stable_baselines3 import PPO, SAC
from environment import SatelliteOrbitEnv
import gymnasium as gym

os.makedirs("results", exist_ok=True)

# ── Disturbance-aware environment wrapper ────────────────────────────────────
class SatelliteOrbitEnvWithDisturbance(SatelliteOrbitEnv):
    """Same as base env but with configurable disturbance scale."""

    def __init__(self, reward_mode="shaped", disturbance_scale=1.0):
        super().__init__(reward_mode=reward_mode)
        self.disturbance_scale = disturbance_scale
        # Force curriculum to level 1 for fair evaluation
        self.curriculum_level = 1

    def step(self, action):
        action = np.clip(action, -1.0, 1.0).astype(np.float32)

        thrust    = action * 0.1
        fuel_used = float(np.linalg.norm(thrust)) * 10.0
        self.fuel = max(0.0, self.fuel - fuel_used)

        self.vel_error = (self.vel_error - thrust).astype(np.float32)

        # ← disturbance scale applied here
        j2_drift = np.array([0.001, 0.0005, 0.0002], dtype=np.float32)
        j2_drift *= self.disturbance_scale

        self.pos_error = (
            self.pos_error
            + self.vel_error * self.dt
            + j2_drift
        ).astype(np.float32)

        self.step_count += 1

        pos_mag = float(np.linalg.norm(self.pos_error))
        vel_mag = float(np.linalg.norm(self.vel_error))

        reward = self._compute_reward(pos_mag, vel_mag, fuel_used)

        success       = pos_mag < 5.0 and vel_mag < 0.05
        out_of_fuel   = self.fuel <= 0
        out_of_bounds = pos_mag > 500.0
        terminated    = success or out_of_fuel or out_of_bounds
        truncated     = self.step_count >= self.max_steps

        info = {
            "pos_error"      : pos_mag,
            "vel_error"      : vel_mag,
            "fuel_remaining" : self.fuel,
            "success"        : success,
        }

        return self._get_obs(), reward, terminated, truncated, info


# ── Configuration ────────────────────────────────────────────────────────────
EPISODES_PER_CONDITION = 30   # same as reference paper

disturbance_levels = [
    ("None",     0.0),
    ("Mild",     1.0),
    ("Moderate", 5.0),
    ("Strong",   15.0),
    ("Extreme",  30.0),
]

experiments = [
    ("PPO", "naive"),
    ("PPO", "fuel_aware"),
    ("PPO", "shaped"),
    ("SAC", "naive"),
    ("SAC", "fuel_aware"),
    ("SAC", "shaped"),
]

# ── Run evaluations ──────────────────────────────────────────────────────────
results = []

for algo, reward in experiments:
    model_path = f"models/{algo}_{reward}"
    print(f"\n{'='*55}")
    print(f"  Evaluating: {algo} + {reward}")
    print(f"{'='*55}")

    try:
        model = PPO.load(model_path) if algo == "PPO" else SAC.load(model_path)
    except Exception as e:
        print(f"  ✗ Could not load model: {e}")
        print(f"    Make sure training is complete first.")
        continue

    for dist_name, dist_scale in disturbance_levels:
        env = SatelliteOrbitEnvWithDisturbance(
            reward_mode=reward,
            disturbance_scale=dist_scale
        )

        successes   = 0
        fuels_used  = []
        pos_errors  = []
        ep_rewards  = []
        steps_taken = []

        for ep in range(EPISODES_PER_CONDITION):
            obs, _ = env.reset()
            ep_reward = 0.0
            done = False

            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward_val, terminated, truncated, info = env.step(action)
                ep_reward += reward_val
                done = terminated or truncated

            if info["success"]:
                successes += 1
            fuels_used.append(env.max_fuel - info["fuel_remaining"])
            pos_errors.append(info["pos_error"])
            ep_rewards.append(ep_reward)
            steps_taken.append(env.step_count)

        success_rate = successes / EPISODES_PER_CONDITION
        avg_fuel     = np.mean(fuels_used)
        avg_pos_err  = np.mean(pos_errors)
        avg_reward   = np.mean(ep_rewards)
        avg_steps    = np.mean(steps_taken)

        results.append({
            "Algorithm"       : algo,
            "Reward"          : reward,
            "Disturbance"     : dist_name,
            "Dist_Scale"      : dist_scale,
            "Success_Rate"    : success_rate,
            "Avg_Fuel_Used"   : avg_fuel,
            "Avg_Pos_Error_km": avg_pos_err,
            "Avg_Reward"      : avg_reward,
            "Avg_Steps"       : avg_steps,
            "N_Episodes"      : EPISODES_PER_CONDITION,
        })

        print(f"  [{dist_name:8s} ×{dist_scale:4.0f}]  "
              f"Success: {success_rate*100:5.1f}%  "
              f"Fuel: {avg_fuel:5.1f}  "
              f"PosErr: {avg_pos_err:6.2f} km")

# ── Save results ─────────────────────────────────────────────────────────────
df = pd.DataFrame(results)
df.to_csv("results/robustness_results.csv", index=False)
print(f"\n\nResults saved to: results/robustness_results.csv")
print(df.to_string(index=False))
