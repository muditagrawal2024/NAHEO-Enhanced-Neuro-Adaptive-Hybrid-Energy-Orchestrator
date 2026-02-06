"""
e-NAHEO Master Presentation Script
Generates ALL visualizations in separate windows and saves them individually
Run this ONE file for complete demo
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random
import numpy as np
from virtual_physics import PhysicsEngine
from e_naheo_brain_v2 import NAHEO_Brain_V2

print("\n" + "="*70)
print("  e-NAHEO: MASTER PRESENTATION GENERATOR")
print("="*70)
print("  This will generate 14 separate visualizations")
print("  Each will open in a new window and save as individual PNG")
print("="*70 + "\n")

# ============================================================================
# SIMULATION RUNNER
# ============================================================================
def run_simulation(mode="SMART", duration_seconds=180, initial_soc=100, disturbance_rate=0.05):
    hw = PhysicsEngine()
    brain = NAHEO_Brain_V2()
    hw.current_charge = (initial_soc / 100) * hw.battery_capacity
    
    if mode == "SMART":
        print(f"[{mode}] Pre-training RL Agent...")
        for _ in range(2000):
            soc_train = random.uniform(0, 100)
            ocv_est = 6.0 + (2.4 * (soc_train/100))
            v_train = ocv_est - (random.uniform(0, 2.0) * 0.3)
            dummy_sensor = {
                "V": max(5.5, v_train), 
                "Disturbance": random.choice([True, False]), 
                "SoC": soc_train
            }
            brain.run_cycle(dummy_sensor)
    
    time_log, temp_log, energy_log, current_log = [], [], [], []
    voltage_log, pwm_log, cpu_mode_log, disturbance_log, soc_log = [], [], [], [], []
    total_energy_consumed = 0.0
    cpu_high_time = 0.0
    dt = 0.1
    
    print(f"--- Running: {mode} Mode (SoC: {initial_soc}%, Disturbance: {disturbance_rate*100}%) ---")
    
    for t in range(int(duration_seconds / dt)):
        current_time = t * dt
        sensors = {
            "V": hw.voltage_terminal, 
            "Disturbance": hw.disturbance_active,
            "SoC": (hw.current_charge / hw.battery_capacity) * 100
        }
        
        if mode == "SMART":
            pwm, cpu_mode, _ = brain.run_cycle(sensors)
        else:
            pwm = 1.0
            cpu_mode = "HIGH"
        
        if random.random() < disturbance_rate:
            hw.disturbance_active = not hw.disturbance_active
            
        state = hw.update(dt, pwm, cpu_mode)
        total_energy_consumed += (state['V'] * state['I'] * dt)
        if cpu_mode == "HIGH":
            cpu_high_time += dt
        
        time_log.append(current_time)
        temp_log.append(state['T'])
        energy_log.append(total_energy_consumed)
        current_log.append(state['I'])
        voltage_log.append(state['V'])
        pwm_log.append(pwm)
        cpu_mode_log.append(1 if cpu_mode == "HIGH" else 0)
        disturbance_log.append(1 if state['Disturbance'] else 0)
        soc_log.append(sensors['SoC'])
        
    cpu_efficiency = (1 - (cpu_high_time / duration_seconds)) * 100
    
    return {
        'time': time_log, 'temp': temp_log, 'energy': energy_log,
        'current': current_log, 'voltage': voltage_log, 'pwm': pwm_log,
        'cpu_mode': cpu_mode_log, 'disturbance': disturbance_log, 'soc': soc_log,
        'total_energy': total_energy_consumed, 'cpu_efficiency': cpu_efficiency
    }

# ============================================================================
# RUN ALL SCENARIOS
# ============================================================================
print("\n" + "="*70)
print("PHASE 1: RUNNING MULTI-SCENARIO SIMULATIONS")
print("="*70 + "\n")

print("SCENARIO 1: Standard Battery (100% SoC, Normal Load)")
baseline_1 = run_simulation("DUMB", 180, 100, 0.05)
smart_1 = run_simulation("SMART", 180, 100, 0.05)
savings_1 = ((baseline_1['total_energy'] - smart_1['total_energy']) / baseline_1['total_energy']) * 100

print("\nSCENARIO 2: Low Battery Challenge (30% SoC, Normal Load)")
baseline_2 = run_simulation("DUMB", 180, 30, 0.05)
smart_2 = run_simulation("SMART", 180, 30, 0.05)
savings_2 = ((baseline_2['total_energy'] - smart_2['total_energy']) / baseline_2['total_energy']) * 100

print("\nSCENARIO 3: High-Stress Environment (100% SoC, 15% Disturbance)")
baseline_3 = run_simulation("DUMB", 180, 100, 0.15)
smart_3 = run_simulation("SMART", 180, 100, 0.15)
savings_3 = ((baseline_3['total_energy'] - smart_3['total_energy']) / baseline_3['total_energy']) * 100

print("\n" + "="*70)
print("BENCHMARK RESULTS:")
print(f"  Scenario 1 (Standard):  {savings_1:.1f}% Energy Saved | CPU Sleep: {smart_1['cpu_efficiency']:.1f}%")
print(f"  Scenario 2 (Low Batt):  {savings_2:.1f}% Energy Saved | CPU Sleep: {smart_2['cpu_efficiency']:.1f}%")
print(f"  Scenario 3 (Hi-Stress): {savings_3:.1f}% Energy Saved | CPU Sleep: {smart_3['cpu_efficiency']:.1f}%")
print(f"  → Average Savings: {np.mean([savings_1, savings_2, savings_3]):.1f}%")
print("="*70 + "\n")

# ============================================================================
# PHASE 2: GENERATE INDIVIDUAL PLOTS
# ============================================================================
print("="*70)
print("PHASE 2: GENERATING VISUALIZATIONS (14 separate images)")
print("="*70 + "\n")

plot_count = 0

# PLOT 1: Energy Consumption Comparison (Scenario 1)
plot_count += 1
print(f"[{plot_count}/14] Generating: Energy Consumption (Scenario 1)...")
fig1 = plt.figure(figsize=(12, 6), num="Energy Consumption - Scenario 1")
plt.plot(baseline_1['time'], baseline_1['energy'], 'r--', label='Baseline', linewidth=3, alpha=0.7)
plt.plot(smart_1['time'], smart_1['energy'], 'g-', label='e-NAHEO', linewidth=3)
plt.fill_between(smart_1['time'], smart_1['energy'], baseline_1['energy'], color='green', alpha=0.2)
plt.title(f'Energy Consumption: Standard Scenario (-{savings_1:.1f}% Savings)', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Total Energy (Joules)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\01_energy_scenario1.png', dpi=150, bbox_inches='tight')

# PLOT 2: Thermal Profile Comparison
plot_count += 1
print(f"[{plot_count}/14] Generating: Thermal Profile...")
fig2 = plt.figure(figsize=(12, 6), num="Thermal Profile")
plt.plot(baseline_1['time'], baseline_1['temp'], 'r--', label='Baseline', linewidth=3, alpha=0.7)
plt.plot(smart_1['time'], smart_1['temp'], 'g-', label='e-NAHEO', linewidth=3)
plt.fill_between(smart_1['time'], smart_1['temp'], baseline_1['temp'], color='gray', alpha=0.2)
plt.title('System Thermal Profile (Lower = More Efficient)', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\02_thermal_profile.png', dpi=150, bbox_inches='tight')

# PLOT 3: PWM Control Signal
plot_count += 1
print(f"[{plot_count}/14] Generating: PWM Control Signal...")
fig3 = plt.figure(figsize=(12, 6), num="PWM Control Signal")
plt.plot(smart_1['time'], smart_1['pwm'], 'b-', linewidth=2)
plt.fill_between(smart_1['time'], smart_1['pwm'], alpha=0.3, color='blue')
plt.title('MPC Output: PWM Duty Cycle Control', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('PWM Duty Cycle (0-1)', fontsize=12)
plt.ylim([0, 1.1])
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\03_pwm_control.png', dpi=150, bbox_inches='tight')

# PLOT 4: Current Draw Comparison
plot_count += 1
print(f"[{plot_count}/14] Generating: Current Draw Profile...")
fig4 = plt.figure(figsize=(12, 6), num="Current Draw")
plt.plot(baseline_1['time'], baseline_1['current'], 'r--', label='Baseline', linewidth=3, alpha=0.7)
plt.plot(smart_1['time'], smart_1['current'], 'g-', label='e-NAHEO', linewidth=3)
plt.title('Current Draw Profile', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Current (Amperes)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\04_current_draw.png', dpi=150, bbox_inches='tight')

# PLOT 5: Terminal Voltage
plot_count += 1
print(f"[{plot_count}/14] Generating: Terminal Voltage...")
fig5 = plt.figure(figsize=(12, 6), num="Terminal Voltage")
plt.plot(smart_1['time'], smart_1['voltage'], 'orange', linewidth=3)
plt.axhline(y=6.0, color='red', linestyle=':', linewidth=2, label='Cutoff Voltage (6V)')
plt.axhline(y=8.4, color='green', linestyle=':', linewidth=2, label='Full Voltage (8.4V)')
plt.title('Terminal Voltage Under Load', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Voltage (V)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\05_voltage.png', dpi=150, bbox_inches='tight')

# PLOT 6: CPU Power States
plot_count += 1
print(f"[{plot_count}/14] Generating: CPU Power States (ETC)...")
fig6 = plt.figure(figsize=(12, 6), num="CPU Power States")
plt.fill_between(smart_1['time'], smart_1['cpu_mode'], alpha=0.6, color='purple', label='CPU Active (160MHz)')
plt.fill_between(smart_1['time'], 0, where=np.array(smart_1['cpu_mode'])==0, alpha=0.6, color='gray', label='CPU Sleep (20MHz)')
plt.title(f'Event-Triggered Control: CPU Power States ({smart_1["cpu_efficiency"]:.1f}% Sleep Time)', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('CPU State', fontsize=12)
plt.ylim([-0.1, 1.2])
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\06_cpu_states.png', dpi=150, bbox_inches='tight')

# PLOT 7: Battery State of Charge
plot_count += 1
print(f"[{plot_count}/14] Generating: Battery SoC...")
fig7 = plt.figure(figsize=(12, 6), num="Battery SoC")
plt.plot(smart_1['time'], smart_1['soc'], 'b-', linewidth=3)
plt.fill_between(smart_1['time'], smart_1['soc'], alpha=0.2, color='blue')
plt.axhline(y=40, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Conservative Mode Threshold')
plt.axhline(y=80, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Performance Mode Threshold')
plt.title('Battery State of Charge (HARL Strategy Zones)', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('SoC (%)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\07_battery_soc.png', dpi=150, bbox_inches='tight')

# PLOT 8: Load Disturbance Events
plot_count += 1
print(f"[{plot_count}/14] Generating: Disturbance Events...")
fig8 = plt.figure(figsize=(12, 6), num="Disturbance Events")
plt.fill_between(smart_1['time'], smart_1['disturbance'], alpha=0.5, color='red', label='Load Disturbance Active')
plt.title('Stochastic Load Disturbance Events (Motor Stalls)', fontsize=14, fontweight='bold')
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Disturbance Active', fontsize=12)
plt.ylim([-0.1, 1.2])
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\08_disturbances.png', dpi=150, bbox_inches='tight')

# PLOT 9: Multi-Scenario Bar Chart
plot_count += 1
print(f"[{plot_count}/14] Generating: Multi-Scenario Comparison...")
fig9 = plt.figure(figsize=(10, 7), num="Multi-Scenario Comparison")
scenarios = ['Standard\n(100% SoC, 5% Dist)', 'Low Battery\n(30% SoC, 5% Dist)', 'High Stress\n(100% SoC, 15% Dist)']
savings_data = [savings_1, savings_2, savings_3]
colors = ['green', 'orange', 'red']
bars = plt.bar(scenarios, savings_data, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
plt.ylabel('Energy Savings (%)', fontsize=12)
plt.title('e-NAHEO Performance Across Multiple Scenarios', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, savings_data):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 2,
            f'{val:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\09_multi_scenario.png', dpi=150, bbox_inches='tight')

# PLOT 10: Scenario 2 Energy
plot_count += 1
print(f"[{plot_count}/14] Generating: Scenario 2 Energy...")
fig10 = plt.figure(figsize=(12, 6), num="Scenario 2 - Low Battery")
plt.plot(baseline_2['time'], baseline_2['energy'], 'r--', label='Baseline', linewidth=3, alpha=0.7)
plt.plot(smart_2['time'], smart_2['energy'], color='orange', linewidth=3, label='e-NAHEO')
plt.fill_between(smart_2['time'], smart_2['energy'], baseline_2['energy'], color='orange', alpha=0.2)
plt.title(f'Scenario 2: Low Battery Start (-{savings_2:.1f}% Savings)', fontsize=14, fontweight='bold')
plt.ylabel('Energy (Joules)', fontsize=12)
plt.xlabel('Time (seconds)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\10_energy_scenario2.png', dpi=150, bbox_inches='tight')

# PLOT 11: Scenario 3 Energy
plot_count += 1
print(f"[{plot_count}/14] Generating: Scenario 3 Energy...")
fig11 = plt.figure(figsize=(12, 6), num="Scenario 3 - High Stress")
plt.plot(baseline_3['time'], baseline_3['energy'], 'r--', label='Baseline', linewidth=3, alpha=0.7)
plt.plot(smart_3['time'], smart_3['energy'], 'darkred', linewidth=3, label='e-NAHEO')
plt.fill_between(smart_3['time'], smart_3['energy'], baseline_3['energy'], color='red', alpha=0.2)
plt.title(f'Scenario 3: High-Stress Environment (-{savings_3:.1f}% Savings)', fontsize=14, fontweight='bold')
plt.ylabel('Energy (Joules)', fontsize=12)
plt.xlabel('Time (seconds)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\11_energy_scenario3.png', dpi=150, bbox_inches='tight')

# ============================================================================
# PHASE 3: Q-LEARNING ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("PHASE 3: Q-LEARNING CONVERGENCE ANALYSIS")
print("="*70 + "\n")

brain_ql = NAHEO_Brain_V2()
training_iterations = 3000
q_value_history = {state: {action: [] for action in brain_ql.rl.actions} for state in [0, 20, 40, 60, 80]}

print("Training Q-Learning agent (3000 iterations)...")
for i in range(training_iterations):
    soc_train = random.uniform(0, 100)
    ocv_est = 6.0 + (2.4 * (soc_train/100))
    v_train = ocv_est - (random.uniform(0, 2.0) * 0.3)
    dummy_sensor = {
        "V": max(5.5, v_train), 
        "Disturbance": random.choice([True, False]), 
        "SoC": soc_train
    }
    brain_ql.run_cycle(dummy_sensor)
    
    if i % 50 == 0:
        for state in q_value_history.keys():
            if state in brain_ql.rl.q_table:
                for action in brain_ql.rl.actions:
                    q_value_history[state][action].append(brain_ql.rl.q_table[state][action])

# PLOT 12: Q-Learning Convergence
plot_count += 1
print(f"[{plot_count}/14] Generating: Q-Learning Convergence...")
fig12 = plt.figure(figsize=(14, 8), num="Q-Learning Convergence")
soc_states = [0, 20, 40, 60, 80]
action_labels = {0.1: 'Aggressive (λ=0.1)', 1.0: 'Balanced (λ=1.0)', 5.0: 'Conservative (λ=5.0)'}
action_colors = {0.1: 'red', 1.0: 'blue', 5.0: 'green'}

for idx, state in enumerate(soc_states):
    plt.subplot(2, 3, idx + 1)
    if state in q_value_history:
        for action in brain_ql.rl.actions:
            if len(q_value_history[state][action]) > 0:
                plt.plot(range(0, len(q_value_history[state][action])*50, 50), 
                        q_value_history[state][action], 
                        label=action_labels[action],
                        color=action_colors[action],
                        linewidth=2.5)
    plt.title(f'SoC = {state}%', fontweight='bold', fontsize=12)
    plt.xlabel('Training Iteration')
    plt.ylabel('Q-Value')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)

plt.suptitle('Q-Learning Strategy Convergence (HARL Meta-Brain)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\12_q_learning_convergence.png', dpi=150, bbox_inches='tight')

# PLOT 13: Q-Table Heatmap
plot_count += 1
print(f"[{plot_count}/14] Generating: Q-Table Policy Heatmap...")
fig13 = plt.figure(figsize=(10, 7), num="Q-Table Policy")
q_matrix = np.zeros((len(soc_states), len(brain_ql.rl.actions)))
for i, state in enumerate(soc_states):
    if state in brain_ql.rl.q_table:
        for j, action in enumerate(brain_ql.rl.actions):
            q_matrix[i, j] = brain_ql.rl.q_table[state][action]

im = plt.imshow(q_matrix, cmap='RdYlGn', aspect='auto')
plt.xticks(range(len(brain_ql.rl.actions)), ['λ=0.1\n(Aggressive)', 'λ=1.0\n(Balanced)', 'λ=5.0\n(Conservative)'])
plt.yticks(range(len(soc_states)), [f'{s}%' for s in soc_states])
plt.xlabel('Action (MPC Penalty)', fontsize=12)
plt.ylabel('Battery SoC', fontsize=12)
plt.title('Learned Policy: Final Q-Table (Higher = Better)', fontsize=14, fontweight='bold')

for i in range(len(soc_states)):
    for j in range(len(brain_ql.rl.actions)):
        plt.text(j, i, f'{q_matrix[i, j]:.2f}',
                ha="center", va="center", color="black", fontsize=11, fontweight='bold')

plt.colorbar(im, label='Q-Value')
plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\13_q_table_heatmap.png', dpi=150, bbox_inches='tight')

print("\nLearned Optimal Policy:")
for state in sorted(brain_ql.rl.q_table.keys()):
    best_action = max(brain_ql.rl.q_table[state], key=brain_ql.rl.q_table[state].get)
    print(f"  SoC {state:3d}% → Best Action: λ={best_action} ({action_labels[best_action]})")

# ============================================================================
# PHASE 4: TECHNICAL ARCHITECTURE
# ============================================================================
print("\n" + "="*70)
print("PHASE 4: TECHNICAL ARCHITECTURE DIAGRAM")
print("="*70 + "\n")

# PLOT 14: System Architecture
plot_count += 1
print(f"[{plot_count}/14] Generating: System Architecture...")
fig14 = plt.figure(figsize=(12, 10), num="System Architecture")
ax = plt.gca()
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)

# Title
ax.text(5, 11, 'e-NAHEO: 3-Tier Hierarchical Control Architecture', 
        ha='center', fontsize=16, fontweight='bold')

# Layer 3 (Bottom)
ax.add_patch(plt.Rectangle((0.5, 1), 9, 2, facecolor='lightcoral', edgecolor='black', linewidth=3))
ax.text(5, 2, 'LAYER 3: MPC REACTOR\n2-Step Horizon Predictive Control\nDVFS + PWM Output', 
        ha='center', va='center', fontsize=11, fontweight='bold')

# Layer 2 (Middle)
ax.add_patch(plt.Rectangle((0.5, 4), 9, 2, facecolor='lightblue', edgecolor='black', linewidth=3))
ax.text(5, 5, 'LAYER 2: Q-LEARNING CORE\nTabular RL (5 States × 3 Actions)\nEvent-Triggered Control (ETC)', 
        ha='center', va='center', fontsize=11, fontweight='bold')

# Layer 1 (Top)
ax.add_patch(plt.Rectangle((0.5, 7), 9, 2, facecolor='lightgreen', edgecolor='black', linewidth=3))
ax.text(5, 8, 'LAYER 1: HARL META-BRAIN\nHarvesting-Aware RL Strategy\nEnergy Budget Management', 
        ha='center', va='center', fontsize=11, fontweight='bold')

# Sensors
ax.add_patch(plt.Rectangle((0.2, 9.5), 2, 1.2, facecolor='yellow', edgecolor='black', linewidth=2))
ax.text(1.2, 10.1, 'SENSORS\nV, T, SoC', ha='center', va='center', fontsize=10, fontweight='bold')

# Digital Twin
ax.add_patch(plt.Rectangle((7.8, 9.5), 2, 1.2, facecolor='orange', edgecolor='black', linewidth=2))
ax.text(8.8, 10.1, 'EKF GHOST\nI, R Estimate', ha='center', va='center', fontsize=10, fontweight='bold')

# Arrows
ax.arrow(1.2, 9.4, 0, -0.3, head_width=0.3, head_length=0.2, fc='black', ec='black', linewidth=2)
ax.arrow(8.8, 9.4, 0, -0.3, head_width=0.3, head_length=0.2, fc='black', ec='black', linewidth=2)
ax.arrow(5, 6.8, 0, -0.7, head_width=0.4, head_length=0.2, fc='red', ec='red', linewidth=3)
ax.arrow(5, 3.8, 0, -0.7, head_width=0.4, head_length=0.2, fc='red', ec='red', linewidth=3)

# Info box
info_text = (
    "Algorithm Stack:\n"
    "• EKF: Dual-state [I, R] estimation\n"
    "• Q-Learning: ε-greedy (ε=0.1)\n"
    "• MPC: 2-step analytical solution\n"
    "• ETC: 10ms threshold for sleep\n"
    f"→ Result: {np.mean([savings_1, savings_2, savings_3]):.1f}% avg energy savings"
)
ax.text(0.3, 0.3, info_text, fontsize=10, 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('d:\\mudit\\NAHEO_Simulation\\14_architecture.png', dpi=150, bbox_inches='tight')

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("="*70)
print("\nSaved 14 individual PNG files:")
print("  01_energy_scenario1.png       - Main energy comparison")
print("  02_thermal_profile.png        - Temperature comparison")
print("  03_pwm_control.png            - MPC control signal")
print("  04_current_draw.png           - Current profile")
print("  05_voltage.png                - Terminal voltage")
print("  06_cpu_states.png             - ETC power states")
print("  07_battery_soc.png            - State of charge")
print("  08_disturbances.png           - Load events")
print("  09_multi_scenario.png         - Scenario comparison")
print("  10_energy_scenario2.png       - Low battery test")
print("  11_energy_scenario3.png       - High stress test")
print("  12_q_learning_convergence.png - RL training")
print("  13_q_table_heatmap.png        - Learned policy")
print("  14_architecture.png           - System diagram")
print("\n" + "="*70)
print("FINAL RESULTS SUMMARY:")
print(f"  Average Energy Savings: {np.mean([savings_1, savings_2, savings_3]):.1f}%")
print(f"  Average CPU Sleep Time: {np.mean([smart_1['cpu_efficiency'], smart_2['cpu_efficiency'], smart_3['cpu_efficiency']]):.1f}%")
print("="*70)

print("\nShowing all windows... (Close each window to proceed)")
plt.show()
