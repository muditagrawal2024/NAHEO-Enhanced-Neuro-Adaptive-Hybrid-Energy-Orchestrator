#!/usr/bin/env python3
"""
Main simulation runner for NAHEO energy efficiency evaluation.

This script runs comparative simulations of different energy management algorithms
to evaluate their performance in terms of energy consumption and service quality.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.algorithms import (
    AlwaysOnAlgorithm,
    TimerBasedAlgorithm,
    NAHEOAdaptiveAlgorithm
)
from src.simulation import SimulationEngine
from src.utils.config import ConfigManager


def create_algorithm(algo_config: dict):
    """
    Create an algorithm instance from configuration.
    
    Args:
        algo_config: Algorithm configuration dictionary
        
    Returns:
        Algorithm instance
    """
    algo_type = algo_config['type']
    params = algo_config.get('parameters', {})
    
    if algo_type == 'always_on':
        return AlwaysOnAlgorithm(**params)
    elif algo_type == 'timer_based':
        # Convert schedule to list of tuples if needed
        if 'schedule' in params:
            params['schedule'] = [tuple(s) for s in params['schedule']]
        return TimerBasedAlgorithm(**params)
    elif algo_type == 'naheo_adaptive':
        return NAHEOAdaptiveAlgorithm(**params)
    else:
        raise ValueError(f"Unknown algorithm type: {algo_type}")


def run_simulation(config_file: str = None, duration: int = None, 
                  pattern: str = None, output: str = None):
    """
    Run the main simulation.
    
    Args:
        config_file: Path to configuration file
        duration: Override simulation duration
        pattern: Override pattern type
        output: Override output file
    """
    # Load configuration
    if config_file:
        print(f"Loading configuration from {config_file}...")
        config = ConfigManager.load_from_file(config_file)
    else:
        print("Using default configuration...")
        config = ConfigManager.get_default_config()
    
    # Override with command-line arguments
    sim_config = config['simulation']
    if duration is not None:
        sim_config['duration'] = duration
    if pattern is not None:
        sim_config['pattern_type'] = pattern
    if output is not None:
        sim_config['output_file'] = output
    
    # Create simulation engine
    engine = SimulationEngine(
        duration=sim_config['duration'],
        time_step=sim_config.get('time_step', 1.0)
    )
    
    # Create algorithms
    algorithms = []
    for algo_config in config['algorithms']:
        algo = create_algorithm(algo_config)
        algorithms.append(algo)
    
    # Run comparison
    results = engine.compare_algorithms(
        algorithms=algorithms,
        pattern_type=sim_config['pattern_type'],
        verbose=sim_config.get('verbose', True)
    )
    
    # Print results
    engine.print_comparison(results)
    
    # Export results if requested
    output_file = sim_config.get('output_file')
    if output_file:
        engine.export_results(results, output_file)
    
    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='NAHEO Energy Efficiency Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default configuration
  python simulate.py
  
  # Run with custom configuration file
  python simulate.py --config my_config.json
  
  # Run with specific duration and pattern
  python simulate.py --duration 7200 --pattern realistic
  
  # Export results to file
  python simulate.py --output results.json
  
  # Create a default configuration file
  python simulate.py --create-config
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--duration', '-d',
        type=int,
        help='Simulation duration in time steps (default: 3600 = 1 hour)'
    )
    
    parser.add_argument(
        '--pattern', '-p',
        type=str,
        choices=['realistic', 'periodic', 'random', 'bursty'],
        help='User behavior pattern type'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for results (JSON format)'
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a default configuration file and exit'
    )
    
    args = parser.parse_args()
    
    # Handle config creation
    if args.create_config:
        filename = args.config if args.config else 'config.json'
        ConfigManager.create_default_config_file(filename)
        print(f"Default configuration file created: {filename}")
        return 0
    
    # Run simulation
    try:
        run_simulation(
            config_file=args.config,
            duration=args.duration,
            pattern=args.pattern,
            output=args.output
        )
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
