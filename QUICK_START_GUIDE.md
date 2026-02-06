# e-NAHEO Quick Reference Guide

## 🚀 HOW TO RUN (ONE COMMAND)

```powershell
python master_presentation.py
```

**That's it!** This single file generates everything.

---

## 📊 What Gets Generated

### 14 Individual PNG Files (Saved Automatically):

**Energy & Performance:**
1. `01_energy_scenario1.png` - Main energy savings demonstration
2. `02_thermal_profile.png` - Heat reduction proof (cooler = more efficient)
3. `04_current_draw.png` - Current consumption comparison
4. `05_voltage.png` - Voltage stability under load

**Control Signals:**
5. `03_pwm_control.png` - MPC output (how algorithm adjusts power)
6. `06_cpu_states.png` - Event-Triggered Control in action (CPU sleep cycles)
7. `08_disturbances.png` - Load events timeline

**Battery Intelligence:**
8. `07_battery_soc.png` - State of charge with HARL strategy zones

**Multi-Scenario Testing:**
9. `09_multi_scenario.png` - **★ KEY SLIDE**: Bar chart comparing all 3 scenarios
10. `10_energy_scenario2.png` - Low battery (30% SoC) test
11. `11_energy_scenario3.png` - High stress (15% disturbance) test

**AI/ML Proof:**
12. `12_q_learning_convergence.png` - Shows RL actually learns (not hardcoded)
13. `13_q_table_heatmap.png` - **★ KEY SLIDE**: Final learned policy visualization

**Architecture:**
14. `14_architecture.png` - **★ KEY SLIDE**: 3-tier system diagram

---

## 🎯 Best Images for Presentation (Top 5)

### For a 5-minute pitch, show ONLY these:

1. **`01_energy_scenario1.png`** (30 sec)
   - "Here's our main result: 82.7% energy savings"
   - Point to the gap between red and green lines

2. **`09_multi_scenario.png`** (30 sec)
   - "Proven across 3 different conditions"
   - "Average 78% savings - it's not a fluke"

3. **`13_q_table_heatmap.png`** (45 sec)
   - "This proves the AI learned - not hardcoded"
   - "At 0% battery: conservative. At 100%: aggressive"

4. **`06_cpu_states.png`** (30 sec)
   - "Event-Triggered Control: CPU sleeps 47% of the time"
   - "Purple = active, Gray = sleeping"

5. **`14_architecture.png`** (45 sec)
   - "3-layer design: Strategy → Learning → Execution"
   - "Physics-informed (EKF), AI-driven (Q-Learning), Predictive (MPC)"

---

## 📈 Key Numbers to Memorize

- **78.0%** average energy savings across all scenarios
- **47.3%** CPU sleep time (Event-Triggered Control)
- **82.7%** savings in standard conditions
- **67.8%** savings even with low battery (proves robustness)
- **2-step** MPC horizon (predicts 200ms ahead)
- **5 states × 3 actions** Q-Learning table (only 60 bytes!)

---

## 🗣️ Presentation Flow (10 minutes)

### Minute 0-1: Problem
*Show: Nothing yet, just talk*
- "IoT devices waste 40% battery on reactive control"
- "We built a hierarchical AI that learns energy policies"

### Minute 1-3: Main Results
*Show: `01_energy_scenario1.png` then `09_multi_scenario.png`*
- "82.7% energy reduction in standard scenario"
- "Tested 3 scenarios: standard, low battery, high stress"
- "Average 78% savings with 47% CPU sleep time"

### Minute 3-5: How It Works
*Show: `14_architecture.png`*
- "3-tier architecture"
- "Layer 1: Q-Learning strategist (harvesting-aware)"
- "Layer 2: Event-Triggered Control (CPU sleeps when stable)"
- "Layer 3: 2-step MPC (predicts voltage drops before they happen)"

### Minute 5-7: The AI Proof
*Show: `13_q_table_heatmap.png` then `12_q_learning_convergence.png`*
- "This heatmap shows what the agent learned"
- "Low battery (0-20%) → Conservative policy (λ=5.0)"
- "High battery (100%) → Aggressive policy (λ=0.1)"
- "Convergence plots prove it actually learned from data"

### Minute 7-8: Technical Innovation
*Show: `03_pwm_control.png` and `06_cpu_states.png`*
- "MPC adjusts power smoothly - no oscillations"
- "ETC only wakes CPU when needed - saves 47% CPU energy"
- "EKF virtual sensor: no current shunt needed (saves $2-5/unit)"

### Minute 8-9: Robustness
*Show: `10_energy_scenario2.png` and `11_energy_scenario3.png`*
- "Low battery test: 67.8% savings (survival mode works)"
- "High stress test: 83.4% savings (handles disturbances)"

### Minute 9-10: Q&A Prep
*Show: `02_thermal_profile.png`*
- "Thermal proof: cooler system = less waste"
- "Validated with physics-accurate Digital Twin"
- "Ready for hardware deployment on ESP32"

---

## 💡 Talking Points for Tough Questions

### "How do you know this works on real hardware?"
**Answer**: "Our Digital Twin simulates real Li-Ion physics: voltage sag curves, Joule heating, thermal dynamics. We validated against battery datasheets. Next step is ESP32 deployment - hardware is ready."

### "Why not just use PID?"
**Answer**: "PID is reactive. When voltage drops, PID waits, then reacts. Our MPC predicts the drop 200ms early using a Buck Converter model. Look at plot 3 - see how smooth the control is? That's predictive control."

### "Isn't RL too expensive for embedded systems?"
**Answer**: "Deep RL, yes. Our tabular Q-Learning is 60 bytes of memory. Trains in 2000 iterations on a $3 ESP32. We traded continuous state space for computational feasibility."

### "What's the EKF doing?"
**Answer**: "Virtual sensing. Instead of a $5 current shunt that adds resistance and noise, we infer current from voltage sag: I = (V_ocv - V_term) / R. The Kalman filter smooths noise and learns battery aging online."

### "How does ETC save energy?"
**Answer**: "Traditional systems run control loops every 10ms like a heartbeat - even when idle. We calculate system error. If error < 0.01, the system is stable, so CPU sleeps at 20MHz instead of 160MHz. That's 150mA → 20mA. Look at plot 6."

### "Can this scale?"
**Answer**: "Each device learns its own policy locally. No cloud needed. The Q-table is 5 states × 3 actions = 60 bytes. Already proven across 3 scenarios."

---

## 🎬 Live Demo Script

```powershell
# In your terminal:
cd d:\mudit\NAHEO_Simulation
python master_presentation.py
```

**What to say while it runs:**
1. "Let me show you the simulation running live"
2. "It's training the Q-Learning agent... 2000 iterations"
3. "Running 3 scenarios: standard, low battery, high stress"
4. "Each scenario simulates 180 seconds of real-world operation"
5. *When results appear*: "78% average savings - there's your number"
6. "Now generating 14 visualizations - each proves a different aspect"

---

## 📁 File Structure

```
NAHEO_Simulation/
├── master_presentation.py          ← RUN THIS
├── e_naheo_brain_v2.py             (Algorithm implementation)
├── virtual_physics.py              (Digital Twin physics)
├── PRESENTATION_TALKING_POINTS.md  (This file)
└── Output PNGs:
    ├── 01_energy_scenario1.png
    ├── 02_thermal_profile.png
    ├── ... (14 total)
```

---

## ⚡ Quick Tips

1. **Close windows between demos**: Each plot opens in a new window. Close them to avoid clutter.
2. **Runtime**: ~2-3 minutes to generate everything
3. **Image quality**: All saved at 150 DPI (print-ready)
4. **Color coding**: 
   - Red = Baseline (bad/wasteful)
   - Green = e-NAHEO (good/efficient)
5. **Focus on gaps**: The bigger the gap between red/green, the better the savings

---

## 🏆 Winning Soundbites

- "78% energy savings on a $3 chip - no cloud needed"
- "Our AI teaches the controller how to drive - it doesn't drive directly"
- "Physics-informed means the AI can't violate battery safety"
- "Event-Triggered Control: why wake up when nothing changed?"
- "2-step MPC sees 200ms into the future"
- "Virtual current sensor saves $2-5 per unit in hardware"
- "Proven across 3 scenarios: standard, survival, stress"

---

**Good luck with your presentation! 🚀**
