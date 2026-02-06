# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/muditagrawal2024/NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator.git
cd NAHEO-Enhanced-Neuro-Adaptive-Hybrid-Energy-Orchestrator

# Install dependencies
pip install -r requirements.txt
```

## Running Your First Simulation

### Option 1: Use Default Settings
```bash
python simulate.py
```

This runs a 1-hour simulation comparing three algorithms:
- Always-On (baseline)
- Timer-Based (9 AM - 8 PM schedule)
- NAHEO Adaptive (learning-based)

### Option 2: Use Configuration File
```bash
python simulate.py --config examples/config_basic.json
```

### Option 3: Custom Parameters
```bash
# 2-hour simulation with bursty pattern
python simulate.py --duration 7200 --pattern bursty

# Save results to file
python simulate.py --output my_results.json

# Combine options
python simulate.py --duration 3600 --pattern realistic --output results.json
```

## Pattern Types

- `realistic`: Daily usage pattern (low at night, high during day)
- `periodic`: Regular activity bursts
- `random`: Uniform random activity
- `bursty`: Alternating high/low activity periods

## Understanding the Output

Example output:
```
Algorithm: NAHEO-Adaptive
  Energy Consumed:       4231.00 W     ← Total energy used
  Service Quality:       100.00 %      ← Requests served successfully
  Energy Efficiency:      0.0002       ← Quality per unit energy (higher is better)
  Active Time:              59.0 s     ← Time system was active
  Requests Served:            49       ← Successful service requests
  Requests Missed:             0       ← Failed service requests

IMPROVEMENT OVER BASELINE:
  Energy Savings:     +88.25%          ← Energy saved vs. Always-On
  Quality Change:     +0.00%           ← Service quality difference
```

## Running Examples

```bash
# Basic programmatic usage
python examples/basic_usage.py

# Extended comparison with multiple configurations
python simulate.py --config examples/config_extended.json
```

## Creating Custom Configuration

```bash
# Generate a template configuration file
python simulate.py --create-config

# Edit config.json to customize parameters
# Run with your custom config
python simulate.py --config config.json
```

## Next Steps

- Read [SIMULATION_GUIDE.md](SIMULATION_GUIDE.md) for detailed documentation
- Experiment with different algorithm parameters
- Try different user behavior patterns
- Analyze results for your specific use case

## Common Use Cases

### Test Energy Savings
```bash
python simulate.py --duration 86400 --pattern realistic --output daily_results.json
```

### Compare Multiple Strategies
Edit `examples/config_extended.json` to add your own algorithms and run:
```bash
python simulate.py --config examples/config_extended.json
```

### Analyze Specific Scenarios
```bash
# Morning rush pattern
python simulate.py --duration 3600 --pattern periodic

# Variable usage pattern
python simulate.py --duration 7200 --pattern bursty
```

## Troubleshooting

**Import Error**: Make sure you're in the project root directory when running scripts

**No module 'numpy'**: Install dependencies with `pip install -r requirements.txt`

**Permission denied**: Make scripts executable with `chmod +x simulate.py`

## Support

For questions or issues, please visit the GitHub repository.
