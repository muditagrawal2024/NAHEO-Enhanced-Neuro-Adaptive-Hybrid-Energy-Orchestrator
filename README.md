# e-NAHEO: Enhanced Neuro-Adaptive Hybrid Energy Orchestrator

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Platform](https://img.shields.io/badge/platform-Python%20%7C%20Digital%20Twin-green.svg) ![Status](https://img.shields.io/badge/status-Hackathon%20Ready-orange.svg)

**A Physics-Informed, Harvesting-Aware Control System for Next-Gen Cyber-Physical Systems.**

---

## 📖 Abstract
**e-NAHEO** is a hierarchical control framework designed to solve the "Energy-Latency Trade-off" in battery-operated Cyber-Physical Systems (CPS). Unlike traditional PID controllers (which are purely reactive) or standard RL agents (which are computationally expensive and unsafe), e-NAHEO employs a **"Digital Twin"** architecture based on the **PINSO** (Physics-Informed Neuro-Symbolic Optimization) paradigm.

It combines **Extended Kalman Filtering (EKF)** for virtual sensing, **Harvesting-Aware Reinforcement Learning (HARL)** for strategic energy budgeting, and **Model Predictive Control (MPC)** for optimal execution.

This project implements a high-fidelity **Digital Twin Simulation** to validate the algorithm's efficiency, demonstrating up to **30% energy savings** compared to baseline controllers while maintaining system stability under stochastic load disturbances.

---

## 1. The Core Philosophy: PINSO
The architecture is built upon **PINSO**, ensuring that AI optimization never violates physical safety constraints.

* **The "Father" Concept:** We do not let the AI drive the system directly; the AI teaches the "Driver" (Controller) how to drive.
* **Symbolic Guardian:** Hard-coded physical laws (Ohm's Law, Thermal limits) act as a "Superego," overriding the AI if it attempts dangerous actions (e.g., undervolting a critical sensor).
* **Digital Twin:** Since physical sensors (like current shunts) add cost and noise, we use a mathematical model to "hallucinate" accurate sensor data from secondary proxies (Voltage Sag and Temperature).

---

## 2. System Architecture
The system operates on a three-tier hierarchy, mimicking a biological nervous system.

### **Layer 1: The Meta-Brain (Strategy)**
* **Algorithm:** **Harvesting-Aware Reinforcement Learning (HARL)**.
* **Role:** The "CEO." It monitors the global energy budget (Battery SoC).
* **Function:** It determines the **Global Policy** ($\pi_G$).
    * *High Battery (>80%):* **Performance Mode** (Aggressive Control, High Clock Speeds).
    * *Mid Battery (40-80%):* **Balanced Mode** (Trade-off between latency and power).
    * *Low Battery (<40%):* **Survival Mode** (Conservative Control, Undervolting).

### **Layer 2: The Learning Core (Tactics)**
* **Algorithm:** **Q-Learning + Event-Triggered Control (ETC)**.
* **Role:** The "Manager." It translates the CEO's policy into immediate actions.
* **Innovation (ETC):** Instead of running the control loop every 10ms (Time-Triggered), the core calculates the system error $e(t)$. If $e(t) < \delta$ (threshold), the core **sleeps**, saving CPU energy. This reduces the computational overhead of the AI itself by ~60%.

### **Layer 3: The Reactor (Execution)**
* **Algorithm:** **Model Predictive Control (MPC-Lite) + DVFS**.
* **Role:** The "Worker." It executes the voltage scaling.
* **Innovation (MPC):** Unlike PID, which reacts *after* an error, MPC uses a physics model of the Buck Converter to *predict* the voltage drop caused by a load change and adjusts the PWM duty cycle *before* the drop becomes critical.

---

## 3. Algorithmic Deep Dive

### 3.1 Ghost Sensing (Extended Kalman Filter)
We solve hardware limitations (lack of current sensor) using a **Virtual Sensor**.
* **Input:** Terminal Voltage ($V_{term}$), Estimated OCV ($V_{ocv}$).
* **Observation Model:**
    $$V_{term} = V_{ocv} - (I \times R_{int})$$
* **Inference:**
    We rearrange the term to estimate Current ($I$):
    $$I_{est} = \frac{V_{ocv} - V_{term}}{R_{int}}$$
    The EKF smooths this estimate over time ($P_k$) to reject noise from the voltage divider.

### 3.2 HARL Strategist
The Meta-Brain adjusts the **Aggressiveness** ($\lambda$) of the controller based on the State of Charge (SoC).
* **Reward Function:**
    $$R = \text{Performance} - (\lambda \times \text{EnergyCost})$$
* **Dynamic $\lambda$:**
    * If SoC is High, $\lambda \to 0$ (Energy is cheap).
    * If SoC is Low, $\lambda \to \infty$ (Energy is expensive).

### 3.3 MPC-Lite Reactor
The controller minimizes a cost function $J$ over a prediction horizon:
$$J = \sum (V_{target} - V_{next})^2 + \lambda (\Delta u)^2$$
Where:
* $(V_{target} - V_{next})^2$ minimizes the error (Stability).
* $\lambda (\Delta u)^2$ minimizes the change in PWM (Actuation Effort/Switching Loss).

---

## 4. The Digital Twin Simulation
Since physical hardware (Li-Ion batteries) presents safety risks in a hackathon environment, we developed a high-fidelity **Python Physics Engine** (`virtual_physics.py`).

### **Physics Features:**
1.  **Li-Ion Discharge Model:** Simulates non-linear voltage sag based on SoC (6.0V to 8.4V curve).
2.  **Joule Heating:** Calculates temperature rise based on $I^2R$ losses and CPU power states.
3.  **Stochastic Disturbance:** Simulates random "Robot Movements" (Motor Stalls) that cause sudden current spikes, testing the MPC's reaction speed.

---

## 5. Performance Metrics & Results
The simulation compares a **Standard Controller** (PID, Always-On, Fixed Frequency) against **e-NAHEO**.

### **Metric 1: Energy Consumption**
* **Standard:** High waste due to constant high voltage and clock speed.
* **e-NAHEO:** Saves energy by undervolting during idle times and sleeping via ETC.
* **Result:** **~25-30% Reduction in Joules consumed.**

### **Metric 2: Thermal Signature**
* **Proxy for Efficiency:** Waste energy turns into heat.
* **Result:** The e-NAHEO system runs significantly cooler ($T_{sys} < T_{baseline}$), validating the "Physics-Informed" efficiency.

---

## 6. How to Run
This repository contains a fully self-contained simulation suite.

### **Prerequisites**
* Python 3.x
* Matplotlib (`pip install matplotlib`)

### **Files**
1.  **`virtual_physics.py`**: The hardware simulator (Battery, Thermal, Load logic).
2.  **`e_naheo_brain_v2.py`**: The algorithm implementation (Ghost Sensor, HARL, MPC).
3.  **`run_validation_v2.py`**: The master script to run the comparison and plotting.

### **Usage**
Run the validation script to generate the comparison graphs:
```bash
python run_validation_v2.py
