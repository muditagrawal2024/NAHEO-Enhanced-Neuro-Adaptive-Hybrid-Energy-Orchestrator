"""
Timer-Based algorithm: System activates based on predefined schedule.
"""

from typing import Dict, Any, List, Tuple
from .base_algorithm import BaseAlgorithm


class TimerBasedAlgorithm(BaseAlgorithm):
    """
    Timer-based algorithm that activates system during predefined time windows.
    """
    
    def __init__(self, schedule: List[Tuple[float, float]], active_power: float = 10.0, 
                 idle_power: float = 1.0):
        """
        Initialize Timer-Based algorithm.
        
        Args:
            schedule: List of (start_time, end_time) tuples defining active periods
            active_power: Power consumption when active (watts)
            idle_power: Power consumption when idle (watts)
        """
        super().__init__("Timer-Based")
        self.schedule = schedule
        self.active_power = active_power
        self.idle_power = idle_power
    
    def should_activate(self, timestamp: float, user_request: bool, context: Dict[str, Any]) -> bool:
        """Check if current time falls within scheduled active periods."""
        # Use time_of_day from context (seconds since midnight) for schedule matching
        time_of_day = context.get('time_of_day', timestamp)
        for start_time, end_time in self.schedule:
            if start_time <= time_of_day < end_time:
                return True
        return False
    
    def update(self, timestamp: float, was_active: bool, user_request: bool):
        """Update energy consumption based on activity."""
        if was_active:
            self.energy_consumed += self.active_power
            self.active_time += 1.0
        else:
            self.energy_consumed += self.idle_power
            self.idle_time += 1.0
