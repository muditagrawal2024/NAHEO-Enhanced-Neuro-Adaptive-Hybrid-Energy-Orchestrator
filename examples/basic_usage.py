#!/usr/bin/env python3
"""
Example: Basic usage of NAHEO simulation framework.

This example demonstrates how to run a simple simulation comparing
different energy management algorithms.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms import (
    AlwaysOnAlgorithm,
    TimerBasedAlgorithm,
    NAHEOAdaptiveAlgorithm
)
from src.simulation import SimulationEngine


def main():
    """Run basic simulation example."""
    
    print("NAHEO Basic Simulation Example")
    print("=" * 60)
    
    # Create simulation engine (1 hour simulation)
    engine = SimulationEngine(duration=3600, time_step=1.0)
    
    # Create algorithms to compare
    algorithms = [
        # Baseline: Always on
        AlwaysOnAlgorithm(active_power=10.0),
        
        # Timer-based: Active 9 AM - 8 PM
        TimerBasedAlgorithm(
            schedule=[(32400, 72000)],  # 9 AM to 8 PM in seconds
            active_power=10.0,
            idle_power=1.0
        ),
        
        # NAHEO: Adaptive learning
        NAHEOAdaptiveAlgorithm(
            active_power=10.0,
            idle_power=1.0,
            learning_rate=0.1,
            prediction_threshold=0.5,
            wake_up_cost=2.0
        )
    ]
    
    # Run comparison with realistic user behavior
    results = engine.compare_algorithms(
        algorithms=algorithms,
        pattern_type='realistic',
        verbose=True
    )
    
    # Print detailed comparison
    engine.print_comparison(results)
    
    # Export results
    engine.export_results(results, 'example_results.json')
    
    print("\nExample completed successfully!")


if __name__ == '__main__':
    main()
