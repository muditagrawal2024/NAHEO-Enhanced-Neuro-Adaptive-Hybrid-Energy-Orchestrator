"""
User behavior pattern generator for realistic simulation scenarios.
"""

import numpy as np
from typing import List, Tuple, Dict, Any


class UserBehaviorGenerator:
    """
    Generates realistic user behavior patterns for simulation.
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize behavior generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            np.random.seed(seed)
        self.seed = seed
        
        # Configuration constants
        self.NOISE_STD_DEV = 0.02  # Standard deviation for probability noise
    
    def generate_pattern(self, duration: int, pattern_type: str = 'realistic') -> List[bool]:
        """
        Generate user request pattern.
        
        Args:
            duration: Simulation duration in time steps
            pattern_type: Type of pattern ('realistic', 'periodic', 'random', 'bursty')
            
        Returns:
            List of boolean values indicating user requests at each time step
        """
        if pattern_type == 'realistic':
            return self._generate_realistic_pattern(duration)
        elif pattern_type == 'periodic':
            return self._generate_periodic_pattern(duration)
        elif pattern_type == 'random':
            return self._generate_random_pattern(duration)
        elif pattern_type == 'bursty':
            return self._generate_bursty_pattern(duration)
        else:
            raise ValueError(f"Unknown pattern type: {pattern_type}")
    
    def _generate_realistic_pattern(self, duration: int) -> List[bool]:
        """
        Generate realistic user behavior with time-of-day patterns.
        Simulates typical usage: low activity at night, peaks during day.
        """
        requests = []
        
        # Assume each time step is 1 second, day has 86400 seconds
        seconds_per_day = 86400
        
        for t in range(duration):
            # Time of day (0-86400 seconds)
            time_of_day = t % seconds_per_day
            hour = (time_of_day // 3600) % 24
            
            # Base probability depends on hour of day
            if 0 <= hour < 6:  # Night: very low activity
                base_prob = 0.01
            elif 6 <= hour < 9:  # Morning: moderate activity
                base_prob = 0.15
            elif 9 <= hour < 12:  # Late morning: high activity
                base_prob = 0.25
            elif 12 <= hour < 14:  # Lunch: medium activity
                base_prob = 0.10
            elif 14 <= hour < 18:  # Afternoon: high activity
                base_prob = 0.30
            elif 18 <= hour < 22:  # Evening: moderate activity
                base_prob = 0.20
            else:  # Late evening: low activity
                base_prob = 0.05
            
            # Add some randomness
            prob = base_prob + np.random.normal(0, self.NOISE_STD_DEV)
            prob = max(0, min(1, prob))
            
            requests.append(np.random.random() < prob)
        
        return requests
    
    def _generate_periodic_pattern(self, duration: int, period: int = 300) -> List[bool]:
        """
        Generate periodic pattern with fixed intervals.
        
        Args:
            duration: Total duration
            period: Period of activity (time steps between bursts)
        """
        requests = []
        burst_length = 20  # Length of each activity burst
        
        for t in range(duration):
            # Active during burst periods
            in_burst = (t % period) < burst_length
            requests.append(in_burst)
        
        return requests
    
    def _generate_random_pattern(self, duration: int, activity_rate: float = 0.15) -> List[bool]:
        """
        Generate random pattern with uniform probability.
        
        Args:
            duration: Total duration
            activity_rate: Probability of request at any time step
        """
        return [np.random.random() < activity_rate for _ in range(duration)]
    
    def _generate_bursty_pattern(self, duration: int) -> List[bool]:
        """
        Generate bursty pattern with periods of high and low activity.
        """
        requests = []
        
        # Generate burst intervals
        current_state = 'idle'
        state_timer = 0
        idle_duration = 200
        burst_duration = 50
        
        for t in range(duration):
            if state_timer <= 0:
                # Switch state
                if current_state == 'idle':
                    current_state = 'burst'
                    state_timer = burst_duration + np.random.randint(-10, 10)
                else:
                    current_state = 'idle'
                    state_timer = idle_duration + np.random.randint(-50, 50)
            
            if current_state == 'burst':
                requests.append(np.random.random() < 0.4)
            else:
                requests.append(np.random.random() < 0.02)
            
            state_timer -= 1
        
        return requests
