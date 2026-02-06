# NAHEO Energy Efficiency Simulation

## Overview

NAHEO (Neuro-Adaptive Hybrid Energy Orchestrator) is a simulation framework for evaluating and comparing energy management algorithms in battery-operated Cyber-Physical Systems (CPS). The framework implements multiple algorithms and provides tools to analyze their performance.

## Features

- **Multiple Algorithm Implementations**:
  - **Always-On**: Baseline approach with continuous operation
  - **Timer-Based**: Scheduled activation based on predefined time windows
  - **NAHEO Adaptive**: Intelligent learning-based approach that adapts to user behavior patterns

- **Realistic User Behavior Modeling**:
  - Time-of-day patterns
  - Periodic patterns
  - Random patterns
  - Bursty patterns

- **Comprehensive Metrics**:
  - Energy consumption
  - Service quality
  - Energy efficiency
  - Active/idle time distribution
  - Prediction accuracy (for adaptive algorithms)

## Installation

### Requirements

- Python 3.7 or higher
- NumPy

### Setup

1. Clone the repository:
```bash
git clone https://github.com/muditagrawal2024/NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator.git
cd NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Running the Simulation

Run a basic simulation with default settings:
```bash
python simulate.py
```

Run with a custom configuration:
```bash
python simulate.py --config examples/config_basic.json
```

Run with specific parameters:
```bash
python simulate.py --duration 7200 --pattern realistic --output my_results.json
```

### Creating a Configuration File

Generate a default configuration file:
```bash
python simulate.py --create-config
```

This creates a `config.json` file that you can customize.

### Running Examples

Basic usage example:
```bash
python examples/basic_usage.py
```

## Configuration

The simulation is configured using JSON files. Here's an example:

```json
{
  "simulation": {
    "duration": 3600,
    "time_step": 1.0,
    "pattern_type": "realistic",
    "random_seed": 42,
    "verbose": true,
    "output_file": "results.json"
  },
  "algorithms": [
    {
      "name": "Always-On",
      "type": "always_on",
      "parameters": {
        "active_power": 10.0
      }
    },
    {
      "name": "Timer-Based",
      "type": "timer_based",
      "parameters": {
        "schedule": [[32400, 72000]],
        "active_power": 10.0,
        "idle_power": 1.0
      }
    },
    {
      "name": "NAHEO-Adaptive",
      "type": "naheo_adaptive",
      "parameters": {
        "active_power": 10.0,
        "idle_power": 1.0,
        "learning_rate": 0.1,
        "prediction_threshold": 0.5,
        "wake_up_cost": 2.0
      }
    }
  ]
}
```

### Configuration Parameters

#### Simulation Settings

- `duration`: Simulation duration in time steps (default: 3600 = 1 hour)
- `time_step`: Duration of each time step in seconds (default: 1.0)
- `pattern_type`: User behavior pattern ('realistic', 'periodic', 'random', 'bursty')
- `random_seed`: Random seed for reproducibility
- `verbose`: Enable detailed output
- `output_file`: Path to save results (JSON format)

#### Algorithm Parameters

**Always-On Algorithm:**
- `active_power`: Power consumption when active (watts)

**Timer-Based Algorithm:**
- `schedule`: List of [start_time, end_time] pairs in seconds since midnight
- `active_power`: Power consumption when active (watts)
- `idle_power`: Power consumption when idle (watts)

**NAHEO Adaptive Algorithm:**
- `active_power`: Power consumption when active (watts)
- `idle_power`: Power consumption when idle (watts)
- `learning_rate`: Rate of pattern learning (0-1)
- `prediction_threshold`: Confidence threshold for activation (0-1)
- `wake_up_cost`: Energy cost for system wake-up (watts)

## User Behavior Patterns

The simulation supports different user behavior patterns:

1. **Realistic**: Simulates typical daily usage with time-of-day variations
   - Low activity at night (12 AM - 6 AM)
   - Moderate activity in morning/evening
   - High activity during work hours

2. **Periodic**: Regular bursts of activity at fixed intervals
   - Useful for testing timer-based approaches

3. **Random**: Uniform random activity
   - Baseline for unpredictable scenarios

4. **Bursty**: Alternating periods of high and low activity
   - Tests adaptability to changing patterns

## Understanding the Results

The simulation provides comprehensive metrics:

- **Energy Consumed**: Total energy used in watts
- **Service Quality**: Percentage of user requests successfully served
- **Energy Efficiency**: Service quality per unit energy (higher is better)
- **Active Time**: Time system was active (seconds and percentage)
- **Requests Served/Missed**: Count of successful and failed service requests

### Example Output

```
================================================================================
SIMULATION RESULTS COMPARISON
================================================================================

Algorithm: Always-On
────────────────────────────────────────────────────────────────────────────────
  Energy Consumed:         36000.00 W
  Service Quality:            100.00 %
  Energy Efficiency:         0.0028
  Active Time:              3600.0 s (100.0%)
  Requests Served:             450
  Requests Missed:               0

Algorithm: NAHEO-Adaptive
────────────────────────────────────────────────────────────────────────────────
  Energy Consumed:         15432.00 W ⭐ BEST
  Service Quality:             98.67 %
  Energy Efficiency:         0.0064 ⭐ BEST
  Active Time:              1320.0 s (36.7%)
  Requests Served:             444
  Requests Missed:               6

================================================================================
IMPROVEMENT OVER BASELINE (Always-On)
================================================================================

NAHEO-Adaptive:
  Energy Savings:     57.13%
  Quality Change:     -1.33%
```

## Project Structure

```
NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator/
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base_algorithm.py
│   │   ├── always_on.py
│   │   ├── timer_based.py
│   │   └── naheo_adaptive.py
│   ├── simulation/
│   │   ├── __init__.py
│   │   ├── simulation_engine.py
│   │   └── user_behavior.py
│   └── utils/
│       ├── __init__.py
│       └── config.py
├── examples/
│   ├── basic_usage.py
│   ├── config_basic.json
│   └── config_extended.json
├── simulate.py
├── requirements.txt
├── SIMULATION_GUIDE.md
└── README.md
```

## Advanced Usage

### Using the Framework Programmatically

```python
from src.algorithms import NAHEOAdaptiveAlgorithm
from src.simulation import SimulationEngine

# Create custom algorithm
algorithm = NAHEOAdaptiveAlgorithm(
    active_power=10.0,
    idle_power=1.0,
    learning_rate=0.15,
    prediction_threshold=0.4
)

# Create simulation
engine = SimulationEngine(duration=7200)

# Run with specific pattern
results = engine.compare_algorithms(
    algorithms=[algorithm],
    pattern_type='bursty',
    verbose=True
)
```

### Creating Custom Algorithms

Extend the `BaseAlgorithm` class:

```python
from src.algorithms.base_algorithm import BaseAlgorithm

class MyCustomAlgorithm(BaseAlgorithm):
    def __init__(self, **params):
        super().__init__("My Algorithm")
        # Initialize your parameters
        
    def should_activate(self, timestamp, user_request, context):
        # Implement activation logic
        return True  # or False
        
    def update(self, timestamp, was_active, user_request):
        # Update state and energy consumption
        if was_active:
            self.energy_consumed += self.active_power
            self.active_time += 1.0
```

## Performance Benchmarks

Typical performance on a standard laptop (approximate):
- 1 hour simulation (3,600 time steps): < 1 second
- 24 hour simulation (86,400 time steps): ~5-10 seconds
- Multiple algorithm comparison: Linear scaling

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional algorithm implementations
- More sophisticated user behavior models
- Visualization tools
- Multi-device simulations
- Network effects

## License

This project is open source and available under the MIT License.

## Citation

If you use NAHEO in your research, please cite:

```
NAHEO: Neuro-Adaptive Hybrid Energy Orchestrator
A framework for evaluating energy efficiency algorithms in CPS
https://github.com/muditagrawal2024/NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator
```

## Contact

For questions, issues, or contributions, please open an issue on GitHub.
