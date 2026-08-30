
import numpy as np
import gymnasium as gym
from gymnasium import spaces


class SatelliteOrbitEnv(gym.Env):

    def __init__(self, reward_mode="shaped"):
        super().__init__()

        self.reward_mode = reward_mode
        self.max_steps   = 200
        self.max_fuel    = 100.0
        self.dt          = 1.0        # 1 second timestep (was 10)

        # Target orbit radius (km) — LEO 400km altitude
        self.Re              = 6371.0
        self.target_radius   = self.Re + 400.0
        self.mu              = 398600.4418
        self.target_velocity = np.sqrt(self.mu / self.target_radius)

        # Curriculum
        self.curriculum_level  = 1
        self.success_history   = []
        self.history_window    = 20
        self.promote_threshold = 0.70

        self.curriculum_levels = {
            1: {"pos_drift": 10.0,  "vel_drift": 0.01},
            2: {"pos_drift": 30.0,  "vel_drift": 0.03},
            3: {"pos_drift": 80.0,  "vel_drift": 0.08},
            4: {"pos_drift": 150.0, "vel_drift": 0.15},
        }

        # Spaces — state is just error vector
        obs_high = np.array([
            500., 500., 500.,   # position error (km)
            2., 2., 2.,         # velocity error (km/s)
            self.max_fuel,      # fuel remaining
            self.max_steps      # time remaining
        ], dtype=np.float32)

        self.observation_space = spaces.Box(
            low=-obs_high, high=obs_high, dtype=np.float32
        )
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(3,), dtype=np.float32
        )

        self.pos_error  = None
        self.vel_error  = None
        self.fuel       = None
        self.step_count = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        level = self.curriculum_levels[self.curriculum_level]

        # Start with small random drift from target
        self.pos_error = self.np_random.uniform(
            -level["pos_drift"],
             level["pos_drift"],
            size=3
        ).astype(np.float32)

        self.vel_error = self.np_random.uniform(
            -level["vel_drift"],
             level["vel_drift"],
            size=3
        ).astype(np.float32)

        self.fuel       = self.max_fuel
        self.step_count = 0

        return self._get_obs(), {"curriculum_level": self.curriculum_level}

    def step(self, action):
        action = np.clip(action, -1.0, 1.0).astype(np.float32)

        # Thrust directly reduces velocity error
        # Scale: max thrust = 0.1 km/s per step
        thrust     = action * 0.1
        fuel_used  = float(np.linalg.norm(thrust)) * 10.0
        self.fuel  = max(0.0, self.fuel - fuel_used)

        # Apply thrust to velocity error
        self.vel_error = (self.vel_error - thrust).astype(np.float32)

        # Orbital dynamics — position error changes with velocity error
        # Small J2-like drift added each step
        j2_drift = np.array([0.001, 0.0005, 0.0002], dtype=np.float32)
        self.pos_error = (
            self.pos_error
            + self.vel_error * self.dt
            + j2_drift
        ).astype(np.float32)

        self.step_count += 1

        # Current errors
        pos_mag = float(np.linalg.norm(self.pos_error))
        vel_mag = float(np.linalg.norm(self.vel_error))

        # Reward
        reward = self._compute_reward(pos_mag, vel_mag, fuel_used)

        # Termination
        success       = pos_mag < 5.0 and vel_mag < 0.05
        out_of_fuel   = self.fuel <= 0
        out_of_bounds = pos_mag > 500.0
        terminated    = success or out_of_fuel or out_of_bounds
        truncated     = self.step_count >= self.max_steps

        if terminated or truncated:
            self._update_curriculum(success)

        info = {
            "pos_error"       : pos_mag,
            "vel_error"       : vel_mag,
            "fuel_remaining"  : self.fuel,
            "success"         : success,
            "curriculum_level": self.curriculum_level
        }

        return self._get_obs(), reward, terminated, truncated, info

    def _compute_reward(self, pos_mag, vel_mag, fuel_used):
        if self.reward_mode == "naive":
            return -(pos_mag + 10.0 * vel_mag) / 100.0

        elif self.reward_mode == "fuel_aware":
            return -(pos_mag + 10.0 * vel_mag) / 100.0 - 0.01 * fuel_used

        elif self.reward_mode == "shaped":
            r = -(pos_mag + 10.0 * vel_mag) / 100.0
            r -= 0.01 * fuel_used
            if pos_mag < 5.0 and vel_mag < 0.05:
                r += 500.0
            if self.fuel <= 0:
                r -= 50.0
            return r

        return 0.0

    def _update_curriculum(self, success):
        self.success_history.append(1 if success else 0)

        if len(self.success_history) > self.history_window:
            self.success_history.pop(0)

        if len(self.success_history) < self.history_window:
            return

        rate      = sum(self.success_history) / len(self.success_history)
        max_level = max(self.curriculum_levels.keys())

        if rate >= self.promote_threshold and self.curriculum_level < max_level:
            self.curriculum_level += 1
            self.success_history  = []
            print(f"\n>>> Level up! Curriculum level {self.curriculum_level} <<<\n")

    def _get_obs(self):
        obs = np.array([
            *self.pos_error,
            *self.vel_error,
            self.fuel,
            float(self.step_count)
        ], dtype=np.float32)
        return np.clip(obs,
                       self.observation_space.low,
                       self.observation_space.high)