"""
NAHEO Adaptive algorithm: Learns user patterns and adapts accordingly.
"""

import numpy as np
from typing import Dict, Any, List
from collections import defaultdict
from .base_algorithm import BaseAlgorithm


class NAHEOAdaptiveAlgorithm(BaseAlgorithm):
    """
    NAHEO adaptive algorithm that learns user behavior patterns and predicts
    when the system should be active to minimize energy waste while maintaining
    quality of service.
    """
    
    def __init__(self, active_power: float = 10.0, idle_power: float = 1.0,
                 learning_rate: float = 0.1, prediction_threshold: float = 0.5,
                 wake_up_cost: float = 2.0):
        """
        Initialize NAHEO Adaptive algorithm.
        
        Args:
            active_power: Power consumption when active (watts)
            idle_power: Power consumption when idle (watts)
            learning_rate: Rate at which the algorithm learns patterns
            prediction_threshold: Confidence threshold for activation
            wake_up_cost: Energy cost for waking up system (watts)
        """
        super().__init__("NAHEO-Adaptive")
        self.active_power = active_power
        self.idle_power = idle_power
        self.learning_rate = learning_rate
        self.prediction_threshold = prediction_threshold
        self.wake_up_cost = wake_up_cost
        
        # Pattern learning: maps time bins to probability of user activity
        self.time_bin_size = 60  # seconds
        self.activity_patterns = defaultdict(lambda: 0.5)  # Start with neutral prior
        self.pattern_counts = defaultdict(int)
        
        # Recent history for context-aware predictions
        self.recent_requests = []
        self.max_history = 100
        
        # Prediction accuracy tracking
        self.correct_predictions = 0
        self.total_predictions = 0
        
        # State tracking
        self.was_previously_active = False
    
    def _get_time_bin(self, timestamp: float) -> int:
        """Convert timestamp to time bin for pattern matching."""
        return int(timestamp // self.time_bin_size)
    
    def _predict_activity(self, timestamp: float, context: Dict[str, Any]) -> float:
        """
        Predict probability of user activity at given timestamp.
        
        Args:
            timestamp: Current time
            context: Additional context information
            
        Returns:
            Probability of user activity (0-1)
        """
        time_bin = self._get_time_bin(timestamp)
        
        # Base prediction from learned patterns
        base_prob = self.activity_patterns[time_bin]
        
        # Adjust based on recent activity trend
        if len(self.recent_requests) > 0:
            recent_activity_rate = sum(self.recent_requests[-10:]) / min(10, len(self.recent_requests))
            base_prob = 0.7 * base_prob + 0.3 * recent_activity_rate
        
        return base_prob
    
    def should_activate(self, timestamp: float, user_request: bool, context: Dict[str, Any]) -> bool:
        """
        Decide whether to activate system based on prediction and energy cost.
        """
        # Always activate if user is currently requesting
        if user_request:
            return True
        
        # Predict likelihood of imminent user request
        activity_prob = self._predict_activity(timestamp, context)
        
        # Decision based on predicted probability and energy economics
        # Stay active if high probability of continued use
        # Or if wake-up cost makes it inefficient to shut down
        if activity_prob >= self.prediction_threshold:
            return True
        
        # If recently active and probability is moderate, stay active
        # to avoid wake-up costs
        if self.was_previously_active and activity_prob >= 0.3:
            return True
        
        return False
    
    def update(self, timestamp: float, was_active: bool, user_request: bool):
        """
        Update algorithm state and learn from observations.
        """
        # Update energy consumption
        if was_active:
            # Add wake-up cost if transitioning from idle to active
            if not self.was_previously_active:
                self.energy_consumed += self.wake_up_cost
            self.energy_consumed += self.active_power
            self.active_time += 1.0
        else:
            self.energy_consumed += self.idle_power
            self.idle_time += 1.0
        
        self.was_previously_active = was_active
        
        # Learn from user behavior
        time_bin = self._get_time_bin(timestamp)
        
        # Update pattern with exponential moving average
        current_pattern = self.activity_patterns[time_bin]
        observed_value = 1.0 if user_request else 0.0
        self.activity_patterns[time_bin] = (
            (1 - self.learning_rate) * current_pattern + 
            self.learning_rate * observed_value
        )
        self.pattern_counts[time_bin] += 1
        
        # Track recent requests for trend analysis
        self.recent_requests.append(1 if user_request else 0)
        if len(self.recent_requests) > self.max_history:
            self.recent_requests.pop(0)
        
        # Track prediction accuracy
        if was_active and user_request:
            self.correct_predictions += 1
        elif not was_active and not user_request:
            self.correct_predictions += 1
        self.total_predictions += 1
    
    def get_metrics(self) -> Dict[str, float]:
        """Get performance metrics including prediction accuracy."""
        metrics = super().get_metrics()
        
        if self.total_predictions > 0:
            metrics['prediction_accuracy'] = self.correct_predictions / self.total_predictions
        else:
            metrics['prediction_accuracy'] = 0.0
        
        metrics['learned_patterns'] = len(self.activity_patterns)
        
        return metrics
