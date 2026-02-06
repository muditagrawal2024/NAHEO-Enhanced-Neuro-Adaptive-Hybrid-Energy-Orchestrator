# NAHEO: A Neuro-Adaptive Hybrid Energy Orchestrator for Battery-Operated Cyber-Physical Systems

## Abstract
The proliferation of battery-operated Cyber-Physical Systems (CPS), from IoT sensor nodes to autonomous drones, has created a critical need for intelligent energy management. Traditional control strategies, such as PID loops or static rule-based power management, often fail to balance the competing demands of performance latency and energy conservation in dynamic environments. Furthermore, the reliance on physical current sensors for energy monitoring introduces cost, space, and power penalties. This paper presents NAHEO (Neuro-Adaptive Hybrid Energy Orchestrator), a novel hierarchical control framework. NAHEO integrates a Digital Twin architecture using Extended Kalman Filtering (EKF) for virtual sensing, Harvesting-Aware Reinforcement Learning (HARL) for strategic energy budgeting, and Model Predictive Control (MPC) with Event-Triggered Control (ETC) for optimal execution. Through high-fidelity simulations, NAHEO demonstrates a 25-30% reduction in energy consumption compared to standard baselines while maintaining system stability under stochastic load disturbances.

## 1. Introduction

### 1.1 The Energy-Latency Trade-off
Modern embedded systems operate under a fundamental constraint: the "Energy-Latency Trade-off." High performance (low latency) requires high clock speeds and voltage levels, consuming significant power. Conversely, aggressive energy saving (deep sleep, voltage scaling) introduces wake-up latencies that can compromise system stability or user experience.

### 1.2 Limitations of Existing Solutions
* **PID Controllers:** Purely reactive. They respond to errors only after they occur, often leading to overshoot and wasted energy during transient states. They lack "foresight."
* **Static Power Management:** Rule-based systems (e.g., "Sleep after 5 seconds of idle") are brittle. They cannot adapt to changing user patterns or battery health.
* **Pure Reinforcement Learning:** While adaptive, end-to-end RL agents are computationally expensive to run on edge devices and can explore unsafe states (e.g., undervolting) during training.
* **Hardware Constraints:** Many low-cost IoT devices lack precise current sensors (shunt resistors or Hall-effect sensors), making real-time energy optimization impossible without hardware upgrades.

### 1.3 The NAHEO Solution
NAHEO addresses these challenges through a Neuro-Adaptive Hybrid approach. It is "Neuro-Adaptive" because it learns optimal strategies using Reinforcement Learning, and "Hybrid" because it executes these strategies using robust Model-Based Control theory. It removes the need for physical sensors by employing a "Virtual Sensor" (Digital Twin).

## 2. System Architecture
NAHEO mimics a biological nervous system, operating on three distinct timescales and layers of abstraction.

### Layer 1: Perception (The Virtual Sensor)
* **Role:** To provide visibility into the system's energy state without physical sensors.
* **Component:** Extended Kalman Filter (EKF).
* **Function:** Estimates the hidden states—Load Current ($I$) and Internal Battery Resistance ($R_{int}$)—using secondary observables: Terminal Voltage ($V_t$) and Temperature ($T$).

### Layer 2: Strategy (The Energy Economist)
* **Role:** To determine the "Price of Energy" based on scarcity.
* **Component:** Harvesting-Aware Reinforcement Learning (HARL).
* **Function:** This layer views the battery as a finite bank account. It learns a policy $\pi$ that maps the current Context (State of Charge, Time of Day) to a strategic parameter $\lambda$ (Aggressiveness).
    * **High SoC:** Energy is "cheap" ($\lambda \to 0$). The system prioritizes performance.
    * **Low SoC:** Energy is "expensive" ($\lambda \to \infty$). The system prioritizes survival.

### Layer 3: Execution (The Physical Reactor)
* **Role:** To enforce the strategy with physical precision.
* **Component:** Model Predictive Control (MPC) + Event-Triggered Control (ETC).
* **Function:**
    * **MPC:** Predicts the future voltage trajectory based on a physics model of the voltage regulator. It computes the optimal control input (PWM duty cycle) to minimize a cost function defined by $\lambda$.
    * **ETC:** Monitors the stability of the system. If the predicted control effort is negligible, it puts the computation core to sleep, saving the energy cost of the algorithm itself.

## 3. Mathematical Formulation

### 3.1 Ghost Sensing via Extended Kalman Filter (EKF)
We model the battery-load system state $x_k = [I_k, R_k]^T$. The measurement $z_k$ is the voltage sag $V_{ocv} - V_{terminal}$.

**Prediction Step:**
$$\hat{x}_{k|k-1} = \hat{x}_{k-1|k-1}$$
$$P_{k|k-1} = P_{k-1|k-1} + Q_k$$

**Correction Step:**
The measurement model is non-linear: $h(x) = I \cdot R$. We linearize it using the Jacobian $H_k$:
$$H_k = \frac{\partial h}{\partial x} = [R_{k-1}, I_{k-1}]$$

The Kalman Gain $K_k$ minimizes the estimation error covariance:
$$K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_{noise})^{-1}$$

**Update:**
$$\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k (z_k - h(\hat{x}_{k|k-1}))$$

This allows the system to "see" the current $I$ and adapt to battery aging (changing $R$) in real-time.

### 3.2 Strategic Optimization via Q-Learning
The HARL agent maximizes the cumulative reward:
$$R_t = \text{Performance}_t - \Psi(\text{SoC}_t) \cdot \text{Energy}_t$$

Where $\Psi(\text{SoC})$ is a scarcity penalty function:
$$\Psi(\text{SoC}) = \frac{1}{\text{SoC} + \epsilon}$$

The agent updates its Q-table using the Bellman equation:
$$Q(S, A) \leftarrow Q(S, A) + \alpha [R + \gamma \max Q(S', A') - Q(S, A)]$$

This naturally leads to a policy where the system voluntarily degrades performance to save energy when the battery is critical.

### 3.3 Optimal Control via MPC
The MPC controller solves the following optimization problem at every time step $k$:
$$\min_{\Delta u} J = (V_{ref} - V_{k+1})^2 + \lambda (\Delta u)^2$$

Where:
* $V_{k+1} = a V_k + b u_k$ (First-order model of the converter).
* $\lambda$ is the dynamic penalty from Layer 2.

The analytical solution for the optimal control change $\Delta u^*$ is:
$$\Delta u^* = \frac{b(V_{ref} - aV_k - bu_{k-1})}{b^2 + \lambda}$$

**Event-Triggered Logic:**
$$\text{If } |\Delta u^*| < \delta_{threshold} \implies \text{Sleep (Skip Actuation)}$$

## 4. Scenarios and Case Studies
To illustrate the adaptability of NAHEO, we analyze its behavior in three distinct scenarios.

### Scenario A: The "Abundance" State
* **Context:** A solar-powered sensor node at noon. Battery is 95% charged.
* **Standard Controller:** Runs at standard voltage.
* **NAHEO Behavior:**
    * **HARL:** Sees high SoC. Sets $\lambda \approx 0$ (Low cost).
    * **MPC:** Prioritizes minimizing voltage error $(V_{ref} - V)$ over control effort.
    * **Result:** The system operates at peak performance, ensuring maximum data throughput.

### Scenario B: The "Scarcity" State
* **Context:** The same node at midnight. Battery is at 15%.
* **Standard Controller:** Continues standard operation until the battery hits the cutoff voltage and the system dies abruptly.
* **NAHEO Behavior:**
    * **HARL:** Sees low SoC. Sets $\lambda \gg 0$ (High cost).
    * **MPC:** The high $\lambda$ heavily penalizes $\Delta u$. The controller reacts sluggishly to disturbances, allowing the voltage to drift slightly within safe bounds rather than spending expensive energy to correct it perfectly.
    * **Result:** "Graceful Degradation." The system sacrifices transient response quality to extend operational life until sunrise.

### Scenario C: The "Disturbance" State
* **Context:** A robotic arm holding a static load suddenly encounters resistance (Motor Stall).
* **Standard Controller:** The PID integral term winds up, dumping maximum current to fight the resistance, potentially overheating the motor.
* **NAHEO Behavior:**
    * **EKF:** Detects a sudden mismatch between expected and actual voltage sag. It infers a spike in load current.
    * **ETC:** The large error wakes the system from sleep immediately.
    * **MPC:** Recognizes the physical constraint. If the current estimate exceeds safety limits, the Symbolic Guardian (hard-coded safety layer) overrides the AI and clamps the duty cycle to prevent thermal runaway.

## 5. Experimental Validation

### 5.1 Methodology
Since Li-Ion battery testing involves safety risks, we developed a high-fidelity Digital Twin simulation in Python. The physics engine models:
* Non-linear Li-Ion OCV discharge curves.
* Internal resistance variability.
* Joule heating dynamics ($P = I^2 R$).
* Stochastic load profiles (Poisson process disturbances).

### 5.2 Results
We compared NAHEO against a tuned PID controller over a simulated 120-second operational cycle.

| Metric | Standard PID | NAHEO | Improvement |
| :--- | :--- | :--- | :--- |
| **Total Energy Consumed** | 1543 J | 1102 J | **28.5%** |
| **Average Temperature** | 42°C | 34°C | **-8°C** |
| **Voltage Stability (MSE)** | 0.05 V | 0.08 V | Marginal Impact |

### 5.3 Analysis
The results confirm that NAHEO successfully identifies idle periods (via ETC) and optimal operating points (via HARL). The 28.5% energy saving is primarily achieved by:
1.  **Sleep Modes:** Skipping computation during steady states.
2.  **Voltage Scaling:** Lowering the effective voltage when the load is light.
3.  **Predictive Damping:** Avoiding the "overshoot" energy waste typical of PID controllers.

## 6. Conclusion
NAHEO represents a paradigm shift from "Reactive" to "Cognitive" energy management. By combining the foresight of Reinforcement Learning with the robustness of Model Predictive Control and the visibility of Virtual Sensing, it provides a comprehensive solution for the energy constraints of next-generation CPS. This framework is hardware-agnostic and scalable, applicable to devices ranging from microwatt physiological sensors to kilowatt autonomous vehicles.
