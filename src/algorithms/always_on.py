"""
Always-On algorithm: System is always active (baseline approach).
"""

from typing import Dict, Any
from .base_algorithm import BaseAlgorithm


class AlwaysOnAlgorithm(BaseAlgorithm):
    """
    Baseline algorithm where the system is always active.
    This represents traditional "always-on" power management.
    """
    
    def __init__(self, active_power: float = 10.0):
        """
        Initialize Always-On algorithm.
        
        Args:
            active_power: Power consumption when active (watts)
        """
        super().__init__("Always-On")
        self.active_power = active_power
    
    def should_activate(self, timestamp: float, user_request: bool, context: Dict[str, Any]) -> bool:
        """System is always active."""
        return True
    
    def update(self, timestamp: float, was_active: bool, user_request: bool):
        """Update energy consumption."""
        if was_active:
            # Assume 1 time unit = 1 second for energy calculation
            self.energy_consumed += self.active_power
            self.active_time += 1.0
