# NAHEO: Neuro-Adaptive Hybrid Energy Orchestrator

A Physics-Informed Hierarchical Control Framework for Battery-Operated Cyber-Physical Systems

---

## Abstract

The proliferation of battery-operated Cyber-Physical Systems (CPS), from IoT sensor nodes to autonomous drones, has created a critical need for intelligent energy management. Traditional control strategies such as PID loops or static rule-based power management often fail to balance competing demands of performance latency and energy conservation in dynamic environments.

NAHEO addresses these challenges through a hierarchical control framework integrating:
- Digital Twin architecture using Extended Kalman Filtering (EKF) for virtual sensing
- Harvesting-Aware Reinforcement Learning (HARL) for strategic energy budgeting  
- Model Predictive Control (MPC) with Event-Triggered Control (ETC) for optimal execution

Validated through high-fidelity simulations, NAHEO achieves 25-30% reduction in energy consumption compared to standard baselines while maintaining system stability under stochastic load disturbances.

---

## System Architecture

NAHEO operates on three hierarchical layers mimicking biological nervous systems:

### Layer 1: Perception (Virtual Sensor)
**Component:** Extended Kalman Filter (EKF)  
**Function:** Estimates hidden states (load current I and internal battery resistance R_int) using observable metrics (terminal voltage V_t and temperature T)

This eliminates the need for physical current sensors while enabling real-time battery aging detection.

### Layer 2: Strategy (Energy Economist)  
**Component:** Harvesting-Aware Reinforcement Learning (HARL)  
**Function:** Determines energy allocation policy based on battery state of charge (SoC). Maps system context to strategic parameter λ (aggressiveness factor)

- High SoC: λ → 0 (prioritize performance)
- Low SoC: λ → ∞ (prioritize energy conservation)

### Layer 3: Execution (Physical Reactor)
**Component:** Model Predictive Control (MPC) + Event-Triggered Control (ETC)  
**Function:** 
- MPC predicts future voltage trajectory and computes optimal PWM duty cycle
- ETC monitors system stability and triggers CPU sleep during steady states

```
┌───────────────────────────────────────┐
│  LAYER 1: EKF Virtual Sensor          │
│  Estimates [I, R] from voltage sag    │
└─────────────┬─────────────────────────┘
              │
┌─────────────▼─────────────────────────┐
│  LAYER 2: HARL Strategy               │
│  Learns optimal λ based on SoC        │
└─────────────┬─────────────────────────┘
              │
┌─────────────▼─────────────────────────┐
│  LAYER 3: MPC + ETC Execution         │
│  Optimal control with sleep mode      │
└───────────────────────────────────────┘
```

---

## Mathematical Formulation

### Extended Kalman Filter (EKF)

State vector: x_k = [I_k, R_k]^T  
Measurement: z_k = V_ocv - V_terminal

**Prediction:**
```
x̂_k|k-1 = x̂_k-1|k-1
P_k|k-1 = P_k-1|k-1 + Q_k
```

**Correction (with Jacobian linearization):**
```
H_k = [R_k-1, I_k-1]
K_k = P_k|k-1 H_k^T (H_k P_k|k-1 H_k^T + R_noise)^-1
x̂_k|k = x̂_k|k-1 + K_k (z_k - h(x̂_k|k-1))
```

### Q-Learning (HARL)

Reward function with scarcity penalty:
```
R_t = Performance_t - Ψ(SoC_t) · Energy_t
Ψ(SoC) = 1/(SoC + ε)
```

Bellman update:
```
Q(S, A) ← Q(S, A) + α [R + γ max Q(S', A') - Q(S, A)]
```

### Model Predictive Control (MPC)

Optimization problem:
```
min J = (V_ref - V_k+1)^2 + λ (Δu)^2
```

Where V_k+1 = a V_k + b u_k (first-order converter model)

Analytical solution:
```
Δu* = b(V_ref - aV_k - bu_k-1) / (b^2 + λ)
```

Event-triggered logic:
```
|Δu*| < δ_threshold ⟹ CPU Sleep
```

---

## Experimental Scenarios

### Scenario A: Abundance State
Solar-powered sensor node at noon with 95% SoC. HARL sets λ ≈ 0, prioritizing performance and data throughput.

### Scenario B: Scarcity State  
Same node at midnight with 15% SoC. HARL sets λ ≫ 0, allowing voltage drift within safe bounds to extend operational lifetime until energy harvesting resumes.

### Scenario C: Disturbance State
Robotic arm encounters sudden resistance. EKF detects current spike, ETC wakes CPU, and MPC clamps duty cycle to prevent thermal runaway.

---

## Validation Results

Comparison against tuned PID controller over 120-second operational cycle using high-fidelity Digital Twin simulation:

| Metric | Standard PID | NAHEO | Improvement |
|--------|--------------|-------|-------------|
| Total Energy | 1543 J | 1102 J | 28.5% |
| Avg Temperature | 42°C | 34°C | -8°C |
| Voltage Stability | 0.05 V MSE | 0.08 V MSE | Acceptable |

Energy savings achieved through:
1. Sleep modes during steady states (ETC)
2. Dynamic voltage scaling under light loads (HARL)  
3. Predictive control eliminating overshoot (MPC)

---

## Implementation

### Prerequisites
```bash
pip install numpy matplotlib
```

### Execution
```bash
python master_presentation.py
```

Generates 14 visualization plots demonstrating system performance across multiple scenarios.

### Repository Structure
```
NAHEO_Simulation/
├── master_presentation.py    # Main demonstration script
├── e_naheo_brain_v2.py        # Algorithm implementation
├── virtual_physics.py         # Digital Twin physics engine
└── README.md                  # Documentation
```

---

## Key Contributions

1. **Virtual Sensing:** EKF eliminates hardware current sensors while tracking battery degradation
2. **Cognitive Energy Management:** HARL learns context-dependent energy allocation policies  
3. **Predictive Control:** MPC anticipates voltage drops before occurrence
4. **Computational Efficiency:** ETC reduces CPU energy consumption by 47%

---

## Comparison with Existing Approaches

**vs. PID Controllers**  
Traditional PID: Reactive error correction after disturbances  
NAHEO MPC: Predictive control using system model (200ms lookahead)

**vs. Deep Reinforcement Learning**  
Deep RL: Requires GPUs, 100K+ training samples  
NAHEO: Tabular Q-learning, 2000 iterations, 60-byte memory footprint

**vs. Fixed Scheduling**  
Fixed: Identical behavior regardless of battery state  
NAHEO: Harvesting-aware adaptation to energy availability

---

## Theoretical Foundation

NAHEO follows Physics-Informed Neuro-Symbolic Optimization (PINSO):
- **Physics-Informed:** Ohm's Law and thermal dynamics constrain the control space
- **Neuro-Adaptive:** Q-Learning enables online policy optimization
- **Symbolic:** Hard-coded safety limits prevent unsafe states

This paradigm shift moves from reactive to cognitive energy management, combining RL foresight with model-based control robustness.

---

## Hardware Deployment

Target platform: ESP32 microcontroller (160MHz, 520KB RAM)  
Battery: 2S Li-Ion (7.4V nominal)  
Power stage: PWM-controlled buck converter

Memory footprint:
- Q-table: 60 bytes (5 states × 3 actions)  
- EKF state: 32 bytes  
- Total: < 2KB RAM

---

## References

### Foundational Works

1. Kalman, R.E. (1960). "A New Approach to Linear Filtering and Prediction Problems." *ASME Journal of Basic Engineering*, 82(1), 35-45.

2. Watkins, C.J.C.H. (1989). *Learning from Delayed Rewards*. PhD Thesis, Cambridge University.

### Extended Kalman Filtering for Battery Management

3. Plett, G.L. (2004). "Extended Kalman filtering for battery management systems of LiPB-based HEV battery packs: Part 1. Background." *Journal of Power Sources*, 134(2), 252-261.

4. He, H., Xiong, R., & Fan, J. (2011). "Evaluation of lithium-ion battery equivalent circuit models for state of charge estimation by an extended Kalman filter." *Energies*, 4(4), 582-598.

5. Li, X., et al. (2021). "A review of lithium-ion battery state of charge estimation methods: equivalent circuit model and data-driven approach." *Measurement*, 174, 108968.

6. Wang, Y., et al. (2022). "State of charge estimation for lithium-ion batteries based on a novel adaptive extended Kalman filter and deep neural network." *Journal of Energy Storage*, 50, 104566.

### Model Predictive Control in Power Electronics

7. Camacho, E.F. & Bordons, C. (2007). *Model Predictive Control*. Springer-Verlag.

8. Cortés, P., et al. (2008). "Model predictive control in power electronics: A critical review." *IEEE Transactions on Industrial Electronics*, 55(12), 4312-4324.

9. Geyer, T., & Quevedo, D.E. (2014). "Multistep finite control set model predictive control for power electronics." *IEEE Transactions on Power Electronics*, 29(12), 6836-6846.

### Event-Triggered and Self-Triggered Control

10. Heemels, W.P.M.H., et al. (2012). "An introduction to event-triggered and self-triggered control." *IEEE Conference on Decision and Control*, 3270-3285.

11. Borgers, D.P., & Heemels, W.P.M.H. (2014). "Event-triggered control of linear systems with output feedback." *IEEE Transactions on Automatic Control*, 59(7), 1923-1928.

12. Gatsis, K., et al. (2018). "Control with unreliability and intermittency: A review." *Proceedings of the IEEE*, 106(7), 1149-1163.

### Reinforcement Learning for Energy Management

13. Mao, H., et al. (2016). "Resource management with deep reinforcement learning." *ACM Workshop on Hot Topics in Networks (HotNets)*, 50-56.

14. Racua-Rosales, A.I., et al. (2020). "Reinforcement Learning for Energy Management in Hybrid Electric Vehicles: A Review." *IEEE Access*, 8, 172323-172340.

15. Zhang, T., et al. (2023). "Deep reinforcement learning for energy-efficient edge computing: A survey." *IEEE Communications Surveys & Tutorials*, 25(2), 791-828.

---

## Conclusion

NAHEO demonstrates that intelligent energy orchestration can be achieved on resource-constrained embedded systems without cloud infrastructure. The framework is hardware-agnostic and scalable, applicable to devices from microwatt physiological sensors to kilowatt autonomous vehicles.

Future work includes hardware validation on ESP32 platforms and extension to renewable energy harvesting prediction layers.
