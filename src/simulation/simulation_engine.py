"""
Core simulation engine for NAHEO energy efficiency evaluation.
"""

import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json

from ..algorithms.base_algorithm import BaseAlgorithm
from .user_behavior import UserBehaviorGenerator


@dataclass
class SimulationResult:
    """Results from a simulation run."""
    algorithm_name: str
    energy_consumed: float
    active_time: float
    idle_time: float
    total_time: float
    requests_served: int
    requests_missed: int
    service_quality: float
    energy_efficiency: float
    additional_metrics: Dict[str, Any]


class SimulationEngine:
    """
    Main simulation engine for evaluating energy efficiency algorithms.
    """
    
    def __init__(self, duration: int = 3600, time_step: float = 1.0):
        """
        Initialize simulation engine.
        
        Args:
            duration: Simulation duration in time steps (default: 1 hour)
            time_step: Duration of each time step in seconds
        """
        self.duration = duration
        self.time_step = time_step
        self.behavior_generator = UserBehaviorGenerator()
    
    def run_simulation(self, algorithm: BaseAlgorithm, user_pattern: List[bool],
                      verbose: bool = False) -> SimulationResult:
        """
        Run simulation with given algorithm and user pattern.
        
        Args:
            algorithm: Energy efficiency algorithm to evaluate
            user_pattern: List of user requests at each time step
            verbose: Whether to print progress
            
        Returns:
            SimulationResult containing performance metrics
        """
        if len(user_pattern) != self.duration:
            raise ValueError(f"User pattern length ({len(user_pattern)}) must match duration ({self.duration})")
        
        # Reset algorithm state
        algorithm.reset()
        
        # Track service quality
        requests_served = 0
        requests_missed = 0
        
        # Run simulation
        start_time = time.time()
        
        for t in range(self.duration):
            user_request = user_pattern[t]
            
            # Algorithm decides whether to be active
            context = {
                'timestamp': t,
                'time_of_day': (t * self.time_step) % 86400
            }
            should_be_active = algorithm.should_activate(t, user_request, context)
            
            # Check service quality
            if user_request:
                if should_be_active:
                    requests_served += 1
                else:
                    requests_missed += 1
            
            # Update algorithm state
            algorithm.update(t, should_be_active, user_request)
            
            # Progress reporting
            if verbose and (t + 1) % (self.duration // 10) == 0:
                progress = ((t + 1) / self.duration) * 100
                print(f"  Progress: {progress:.1f}% - Energy: {algorithm.energy_consumed:.2f}W")
        
        sim_time = time.time() - start_time
        
        # Calculate metrics
        metrics = algorithm.get_metrics()
        total_requests = requests_served + requests_missed
        service_quality = requests_served / total_requests if total_requests > 0 else 1.0
        
        # Energy efficiency: service quality per unit energy
        energy_efficiency = service_quality / metrics['energy_consumed'] if metrics['energy_consumed'] > 0 else 0
        
        if verbose:
            print(f"  Completed in {sim_time:.2f}s")
        
        return SimulationResult(
            algorithm_name=algorithm.name,
            energy_consumed=metrics['energy_consumed'],
            active_time=metrics['active_time'],
            idle_time=metrics['idle_time'],
            total_time=metrics['total_time'],
            requests_served=requests_served,
            requests_missed=requests_missed,
            service_quality=service_quality,
            energy_efficiency=energy_efficiency,
            additional_metrics={k: v for k, v in metrics.items() 
                              if k not in ['energy_consumed', 'active_time', 'idle_time', 'total_time']}
        )
    
    def compare_algorithms(self, algorithms: List[BaseAlgorithm], 
                          pattern_type: str = 'realistic',
                          verbose: bool = True) -> List[SimulationResult]:
        """
        Compare multiple algorithms on the same user pattern.
        
        Args:
            algorithms: List of algorithms to compare
            pattern_type: Type of user behavior pattern
            verbose: Whether to print progress
            
        Returns:
            List of SimulationResult for each algorithm
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Running Simulation Comparison")
            print(f"{'='*60}")
            print(f"Duration: {self.duration} time steps")
            print(f"Pattern: {pattern_type}")
            print(f"Algorithms: {len(algorithms)}")
            print(f"{'='*60}\n")
        
        # Generate user pattern
        user_pattern = self.behavior_generator.generate_pattern(self.duration, pattern_type)
        total_requests = sum(user_pattern)
        
        if verbose:
            print(f"Generated user pattern with {total_requests} requests ({total_requests/self.duration*100:.1f}% activity)\n")
        
        # Run simulations
        results = []
        for i, algorithm in enumerate(algorithms):
            if verbose:
                print(f"[{i+1}/{len(algorithms)}] Testing {algorithm.name}...")
            
            result = self.run_simulation(algorithm, user_pattern, verbose=verbose)
            results.append(result)
            
            if verbose:
                print(f"  Results: Energy={result.energy_consumed:.2f}W, "
                      f"Quality={result.service_quality*100:.1f}%, "
                      f"Efficiency={result.energy_efficiency:.4f}\n")
        
        return results
    
    def print_comparison(self, results: List[SimulationResult]):
        """
        Print formatted comparison of simulation results.
        
        Args:
            results: List of simulation results to compare
        """
        print(f"\n{'='*80}")
        print(f"SIMULATION RESULTS COMPARISON")
        print(f"{'='*80}\n")
        
        # Find best in each category
        best_energy = min(results, key=lambda r: r.energy_consumed)
        best_quality = max(results, key=lambda r: r.service_quality)
        best_efficiency = max(results, key=lambda r: r.energy_efficiency)
        
        for result in results:
            print(f"Algorithm: {result.algorithm_name}")
            print(f"{'─'*80}")
            
            energy_marker = " ⭐ BEST" if result == best_energy else ""
            print(f"  Energy Consumed:    {result.energy_consumed:10.2f} W{energy_marker}")
            
            quality_marker = " ⭐ BEST" if result == best_quality else ""
            print(f"  Service Quality:    {result.service_quality*100:9.2f} %{quality_marker}")
            
            efficiency_marker = " ⭐ BEST" if result == best_efficiency else ""
            print(f"  Energy Efficiency:  {result.energy_efficiency:10.4f}{efficiency_marker}")
            
            print(f"  Active Time:        {result.active_time:10.1f} s ({result.active_time/result.total_time*100:.1f}%)")
            print(f"  Requests Served:    {result.requests_served:10d}")
            print(f"  Requests Missed:    {result.requests_missed:10d}")
            
            if result.additional_metrics:
                print(f"  Additional Metrics:")
                for key, value in result.additional_metrics.items():
                    print(f"    {key}: {value}")
            
            print()
        
        # Summary comparison
        if len(results) > 1:
            baseline = results[0]  # Assume first is baseline
            print(f"{'='*80}")
            print(f"IMPROVEMENT OVER BASELINE ({baseline.algorithm_name})")
            print(f"{'='*80}\n")
            
            for result in results[1:]:
                energy_saving = (1 - result.energy_consumed / baseline.energy_consumed) * 100
                quality_change = (result.service_quality - baseline.service_quality) * 100
                
                print(f"{result.algorithm_name}:")
                print(f"  Energy Savings:     {energy_saving:+.2f}%")
                print(f"  Quality Change:     {quality_change:+.2f}%")
                print()
        
        print(f"{'='*80}\n")
    
    def export_results(self, results: List[SimulationResult], filename: str):
        """
        Export simulation results to JSON file.
        
        Args:
            results: List of simulation results
            filename: Output filename
        """
        data = []
        for result in results:
            data.append({
                'algorithm_name': result.algorithm_name,
                'energy_consumed': result.energy_consumed,
                'active_time': result.active_time,
                'idle_time': result.idle_time,
                'total_time': result.total_time,
                'requests_served': result.requests_served,
                'requests_missed': result.requests_missed,
                'service_quality': result.service_quality,
                'energy_efficiency': result.energy_efficiency,
                'additional_metrics': result.additional_metrics
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Results exported to {filename}")
