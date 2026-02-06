"""
Base algorithm interface for energy efficiency strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAlgorithm(ABC):
    """
    Abstract base class for energy efficiency algorithms.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.energy_consumed = 0.0
        self.active_time = 0.0
        self.idle_time = 0.0
        
    @abstractmethod
    def should_activate(self, timestamp: float, user_request: bool, context: Dict[str, Any]) -> bool:
        """
        Determine if the system should be active at the given timestamp.
        
        Args:
            timestamp: Current simulation time
            user_request: Whether user has requested service
            context: Additional context information
            
        Returns:
            True if system should be active, False otherwise
        """
        pass
    
    @abstractmethod
    def update(self, timestamp: float, was_active: bool, user_request: bool):
        """
        Update algorithm state after each time step.
        
        Args:
            timestamp: Current simulation time
            was_active: Whether system was active in this time step
            user_request: Whether user requested service
        """
        pass
    
    def reset(self):
        """Reset algorithm state."""
        self.energy_consumed = 0.0
        self.active_time = 0.0
        self.idle_time = 0.0
    
    def get_metrics(self) -> Dict[str, float]:
        """
        Get performance metrics for the algorithm.
        
        Returns:
            Dictionary containing performance metrics
        """
        return {
            'energy_consumed': self.energy_consumed,
            'active_time': self.active_time,
            'idle_time': self.idle_time,
            'total_time': self.active_time + self.idle_time
        }
