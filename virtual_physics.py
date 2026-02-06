import random
import math

class PhysicsEngine:
    def __init__(self):
        # --- Battery Specs (2S Li-Ion Configuration) ---
        # 2 cells in series: Nominal ~7.4V, Max ~8.4V, Min ~6.0V
        self.battery_capacity = 2000.0 # mAh
        self.current_charge = 2000.0   # mAh
        self.internal_resistance = 0.3 # Ohms (Simulates voltage sag under load)
        self.ocv = 8.4 # Open Circuit Voltage (Starts full)
        
        # --- Thermal Specs (Thermodynamics) ---
        self.temperature = 25.0 # Starting Room Temp (Celsius)
        self.thermal_mass = 15.0 # Higher = takes longer to heat up/cool down
        self.cooling_rate = 0.08 # Natural convection cooling
        
        # --- Load Specs (Laser/Motor) ---
        self.base_load_resistance = 10.0 # Ohms (Baseline load)
        
        # --- Simulation State ---
        self.voltage_terminal = 8.4
        self.current_draw = 0.0
        self.disturbance_active = False # Represents Robot Movement/Stall

    def update(self, dt, pwm_duty, cpu_freq_mode):
        """
        Simulates 1 time step of physics.
        dt: Time step in seconds
        pwm_duty: 0.0 to 1.0 (Control Input from Algo)
        cpu_freq_mode: 'HIGH' (Active) or 'LOW' (Sleep/ETC)
        """
        
        # 1. Disturbance Simulation (Random Events)
        # 5% chance to toggle disturbance (Robot starts/stops moving)
        # This simulates an external factor demanding more power
        if random.random() < 0.05: 
            self.disturbance_active = not self.disturbance_active
            
        # 2. Calculate Electrical Load
        # If Disturbance is active (Motor Stall/High Load), Resistance drops
        R_load = self.base_load_resistance
        if self.disturbance_active: 
            R_load *= 0.4 # Load becomes heavy (Low resistance = High Current)
        
        # Effective Voltage seen by Load (PWM Simulation)
        # This simulates the Buck Converter output or PWM masking
        V_applied = self.voltage_terminal * pwm_duty
        
        # Ohm's Law: I_load = V / R
        I_load = V_applied / R_load
        
        # CPU Current (Simulating ESP32 Power Consumption)
        # Novelty: This validates Event-Triggered Control saving power
        # High Freq (160MHz) uses ~150mA, Low Freq/Sleep uses ~20mA
        I_cpu = 0.15 if cpu_freq_mode == 'HIGH' else 0.02 
        
        self.current_draw = I_load + I_cpu
        
        # 3. Battery Physics (Discharge Curve)
        # Calculate Coulombs consumed in this time step
        coulombs = self.current_draw * dt
        # Convert Coulombs to mAh (1 mAh = 3.6 Coulombs)
        self.current_charge -= (coulombs * 1000 / 3600) 
        
        # Calculate State of Charge (SoC)
        soc_factor = max(0, self.current_charge / self.battery_capacity)
        
        # Voltage Sag Model (V_term = V_ocv - I*R_int)
        # Approximated Li-Ion Curve: 6.0V (empty) to 8.4V (full)
        self.ocv = 6.0 + (2.4 * soc_factor) 
        self.voltage_terminal = self.ocv - (self.current_draw * self.internal_resistance)
        
        # 4. Thermal Physics (Joule Heating)
        # Heat Generated = I^2 * R (Internal Battery R) + CPU Heat + MOSFET Heat
        power_heat_internal = (self.current_draw**2 * self.internal_resistance)
        power_heat_cpu = (I_cpu * 3.3)
        power_heat_total = power_heat_internal + power_heat_cpu
        
        # Temp Rise = Power * dt / Mass
        temp_rise = power_heat_total * dt / self.thermal_mass
        
        # Newton's Law of Cooling
        cooling = (self.temperature - 25.0) * self.cooling_rate * dt
        
        self.temperature += (temp_rise - cooling)
        
        # Return state dictionary for the Brain to "Sense"
        return {
            "V": self.voltage_terminal,
            "I": self.current_draw,
            "T": self.temperature,
            "Disturbance": self.disturbance_active,
            "SoC": soc_factor * 100
        }