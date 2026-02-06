# NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator

NAHEO is a hierarchical, multi-agent control system designed to optimize energy consumption in battery-operated Cyber-Physical Systems (CPS). It replaces traditional "Always-On" or "Timer-Based" control with a cognitive architecture that learns user patterns, predicts energy needs, and executes control actions with minimal waste.

## Simulation Framework

This repository includes a comprehensive simulation framework for evaluating and comparing different energy efficiency algorithms. The simulation allows you to:

- Compare **Always-On**, **Timer-Based**, and **NAHEO Adaptive** algorithms
- Model realistic user behavior patterns
- Measure energy consumption, service quality, and efficiency
- Customize algorithm parameters and scenarios

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/muditagrawal2024/NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator.git
cd NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator

# Install dependencies
pip install -r requirements.txt
```

### Run Your First Simulation

```bash
# Run with default settings (1 hour simulation)
python simulate.py

# Run with custom duration and save results
python simulate.py --duration 7200 --output results.json

# Run with specific user behavior pattern
python simulate.py --pattern bursty

# Create a custom configuration file
python simulate.py --create-config
```

### Run Example

```bash
python examples/basic_usage.py
```

## Key Features

### Algorithms Implemented

1. **Always-On Algorithm**: Baseline approach where the system is always active
2. **Timer-Based Algorithm**: Activates system during predefined time windows
3. **NAHEO Adaptive Algorithm**: Learns user patterns and adapts to minimize energy waste while maintaining quality of service

### User Behavior Patterns

- **Realistic**: Time-of-day patterns mimicking typical daily usage
- **Periodic**: Regular activity bursts at fixed intervals
- **Random**: Uniform random activity distribution
- **Bursty**: Alternating high and low activity periods

### Performance Metrics

- Energy consumption (Watts)
- Service quality (% of requests served)
- Energy efficiency (quality per unit energy)
- Active/idle time distribution
- Prediction accuracy (for adaptive algorithms)

## Example Output

```
================================================================================
SIMULATION RESULTS COMPARISON
================================================================================

Algorithm: Always-On
  Energy Consumed:         36000.00 W
  Service Quality:            100.00 %
  Energy Efficiency:         0.0028
  Active Time:              3600.0 s (100.0%)

Algorithm: NAHEO-Adaptive
  Energy Consumed:         15432.00 W ⭐ BEST
  Service Quality:             98.67 %
  Energy Efficiency:         0.0064 ⭐ BEST
  Active Time:              1320.0 s (36.7%)

IMPROVEMENT OVER BASELINE:
  Energy Savings:     57.13%
  Quality Change:     -1.33%
```

## Documentation

For detailed documentation, see [SIMULATION_GUIDE.md](SIMULATION_GUIDE.md)

## Project Structure

```
├── src/
│   ├── algorithms/       # Algorithm implementations
│   ├── simulation/       # Simulation engine and user behavior models
│   └── utils/           # Configuration management
├── examples/            # Example scripts and configurations
├── simulate.py         # Main simulation runner
└── SIMULATION_GUIDE.md # Comprehensive documentation
```

## Contributing

Contributions are welcome! Feel free to:
- Implement new algorithms
- Add user behavior patterns
- Improve documentation
- Report issues or suggest features

## License

MIT License - see LICENSE file for details
