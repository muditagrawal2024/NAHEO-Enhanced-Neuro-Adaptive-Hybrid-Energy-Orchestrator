"""
Configuration management for NAHEO simulations.
"""

import json
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class AlgorithmConfig:
    """Configuration for an algorithm."""
    name: str
    type: str  # 'always_on', 'timer_based', 'naheo_adaptive'
    parameters: Dict[str, Any]


@dataclass
class SimulationConfig:
    """Configuration for a simulation run."""
    duration: int = 3600  # 1 hour default
    time_step: float = 1.0
    pattern_type: str = 'realistic'
    random_seed: int = None
    output_file: str = None
    verbose: bool = True


class ConfigManager:
    """Manages simulation configuration."""
    
    @staticmethod
    def load_from_file(filename: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        with open(filename, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_to_file(config: Dict[str, Any], filename: str):
        """Save configuration to JSON file."""
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default simulation configuration."""
        return {
            'simulation': {
                'duration': 3600,
                'time_step': 1.0,
                'pattern_type': 'realistic',
                'random_seed': 42,
                'verbose': True
            },
            'algorithms': [
                {
                    'name': 'Always-On',
                    'type': 'always_on',
                    'parameters': {
                        'active_power': 10.0
                    }
                },
                {
                    'name': 'Timer-Based',
                    'type': 'timer_based',
                    'parameters': {
                        'schedule': [[32400, 72000]],  # 9 AM to 8 PM
                        'active_power': 10.0,
                        'idle_power': 1.0
                    }
                },
                {
                    'name': 'NAHEO-Adaptive',
                    'type': 'naheo_adaptive',
                    'parameters': {
                        'active_power': 10.0,
                        'idle_power': 1.0,
                        'learning_rate': 0.1,
                        'prediction_threshold': 0.5,
                        'wake_up_cost': 2.0
                    }
                }
            ]
        }
    
    @staticmethod
    def create_default_config_file(filename: str = 'config.json'):
        """Create a default configuration file."""
        config = ConfigManager.get_default_config()
        ConfigManager.save_to_file(config, filename)
        return config
