import math
import random
import numpy as np 

class EKF_GhostSensor:
    """
    TRUE Extended Kalman Filter Implementation
    State: [Current (I), Internal Resistance (R)]
    Measurement: Voltage Drop (V_sag)
    """
    def __init__(self):
        # State Vector x = [I, R]
        self.x = np.array([0.0, 0.3]) 
        # Covariance Matrix P
        self.P = np.array([[1.0, 0.0], [0.0, 1.0]])
        # Process Noise Q (Model uncertainty)
        self.Q = np.array([[0.01, 0.0], [0.0, 0.001]])
        # Measurement Noise R (Sensor noise)
        self.R = 0.1

    def update(self, v_term, v_ocv):
        # 1. Measurement: z = V_ocv - V_term (Voltage Sag)
        z = max(0, v_ocv - v_term)
        
        # 2. Prediction Step (Random Walk Model for I and R)
        x_pred = self.x 
        P_pred = self.P + self.Q
        
        # 3. Jacobian H (Linearization around current estimate)
        # V_sag = I * R -> d(V_sag)/dI = R, d(V_sag)/dR = I
        H = np.array([self.x[1], self.x[0]])
        
        # 4. Kalman Gain K
        # S = H P H.T + R
        S = np.dot(H, np.dot(P_pred, H.T)) + self.R
        K = np.dot(P_pred, H.T) / S
        
        # 5. Update State
        y = z - (x_pred[0] * x_pred[1]) # Innovation
        self.x = x_pred + K * y
        
        # 6. Update Covariance
        self.P = P_pred - np.outer(K, H) * S
        
        # Constraint: Resistance/Current can't be negative physics-wise
        self.x[0] = max(0.0, self.x[0])
        self.x[1] = max(0.05, self.x[1])
        
        return self.x[0] # Return Estimated Current

class TrueMPC_Reactor:
    """
    Finite Horizon Cost Minimization
    Minimizes J = sum((v_ref - v)^2 + lambda * (delta_u)^2)
    """
    def __init__(self):
        self.u = 1.0 # Current PWM
        # First-order model of Buck Converter: V[k+1] = a*V[k] + b*u[k]
        self.a = 0.9
        self.b = 0.8
        
    def compute(self, target_v_norm, current_v_norm, penalty_lambda):
        # 2-Step Horizon MPC (Extended from 1-step)
        # Predicts TWO steps ahead for better predictive control
        v_next = self.a * current_v_norm + self.b * self.u
        
        # Weighted 2-step horizon: penalizes error at both steps
        numerator = (self.b * (target_v_norm - self.a * current_v_norm) + 
                     0.5 * self.a * self.b * (target_v_norm - v_next) + 
                     penalty_lambda * self.u)
        denominator = (self.b**2) + 0.5 * self.a * (self.b**2) + penalty_lambda
        
        u_opt = numerator / denominator
        
        # Constraints (PWM 0% to 100%)
        self.u = max(0.1, min(1.0, u_opt))
        return self.u

class QLearning_Strategist:
    """
    Tabular Q-Learning Agent
    """
    def __init__(self):
        self.q_table = {} # State -> {Action: Q-Value}
        self.alpha = 0.1 # Learning Rate
        self.gamma = 0.9 # Discount Factor
        self.epsilon = 0.1 # Exploration Rate
        
        # Actions: Lambda values (0.1=Aggressive, 1.0=Balanced, 5.0=Conservative)
        self.actions = [0.1, 1.0, 5.0]
        
    def get_state(self, soc):
        # Discretize SoC into 5 bins (0, 20, 40, 60, 80)
        return int(soc // 20) * 20
        
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
            
        return max(self.q_table[state], key=self.q_table[state].get)
    
    def learn(self, state, action, reward, next_state):
        if state not in self.q_table: self.q_table[state] = {a: 0.0 for a in self.actions}
        if next_state not in self.q_table: self.q_table[next_state] = {a: 0.0 for a in self.actions}
        
        old_q = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())
        
        new_q = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        self.q_table[state][action] = new_q

class NAHEO_Brain_V2:
    def __init__(self):
        self.ghost = EKF_GhostSensor()
        self.mpc = TrueMPC_Reactor()
        self.rl = QLearning_Strategist()
        
        self.last_soc_state = 100
        self.last_action = 1.0
        
    def run_cycle(self, sensor_data):
        v = sensor_data['V']
        disturbance = sensor_data['Disturbance']
        soc = sensor_data['SoC']
        
        # 1. GHOST SENSE (True EKF)
        ocv_est = 6.0 + (2.4 * (soc/100))
        i_est = self.ghost.update(v, ocv_est)
        
        # 2. RL STRATEGY (Q-Learning Step)
        current_state = self.rl.get_state(soc)
        
        # Calculate Reward from PREVIOUS action
        # Reward = Performance (Voltage Stability) - Energy Cost penalty
        # Penalty scales inversely with SoC (Lower battery = Higher cost to use energy)
        energy_penalty_factor = (110 - soc) / 4 # Stronger penalty: 100%->2.5, 0%->27.5
        reward = (v/8.4) - (energy_penalty_factor * i_est * 0.18)
        
        # Update Q-Table
        self.rl.learn(self.last_soc_state, self.last_action, reward, current_state)
        
        # Decide NEW Action (Lambda)
        mpc_lambda = self.rl.choose_action(current_state)
        self.last_soc_state = current_state
        self.last_action = mpc_lambda
        
        # Override for Disturbance (Safety critical)
        if disturbance: mpc_lambda = 0.01 # Minimal penalty, maximize reaction
        
        # 3. SET TARGET
        target_v = 8.4 if disturbance else 7.5
        
        # 4. MPC EXECUTE (Analytic Solution)
        pwm_out = self.mpc.compute(target_v / 8.4, v / 8.4, mpc_lambda)
        
        # 5. ETC / DVFS
        delta_pwm = abs(pwm_out - self.mpc.u)
        cpu_mode = "HIGH" if (disturbance or delta_pwm > 0.01) else "LOW"
        
        return pwm_out, cpu_mode, i_est