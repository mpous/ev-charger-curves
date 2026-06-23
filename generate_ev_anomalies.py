import numpy as np
import pandas as pd
import os
import random

def generate_anomalous_ev_dataset(num_curves=50, output_dir="ev_dataset_anomalies"):
    """
    Generates a synthetic dataset of EV charging curves with injected anomalies.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    anomaly_types = ['power_drop', 'power_spike', 'soc_jump', 'plateau']

    for i in range(1, num_curves + 1):
        # 1. Base Parameters (Same as clean script)
        start_soc = np.random.uniform(10, 70)
        knee_soc = np.random.uniform(75, 85)
        max_power = np.random.uniform(50, 150)
        decay_rate = np.random.uniform(0.05, 0.2)
        steps = 100
        soc_values = np.linspace(start_soc, 100, steps)
        timestamps = np.arange(0, steps * 10, 10)
        power_values = np.zeros(steps)
        
        for j in range(steps):
            current_soc = soc_values[j]
            if current_soc < knee_soc:
                power_values[j] = max_power
            else:
                power_values[j] = max_power * np.exp(-decay_rate * (current_soc - knee_soc))
        
        noise = np.random.normal(0, max_power * 0.02, steps)
        power_values += noise
        power_values = np.maximum(power_values, 0)

        # 2. Inject Anomalies
        # 100% chance of an anomaly in this specific anomalous dataset
        anomaly_type = random.choice(anomaly_types)
        anomaly_idx = random.randint(20, 80)
        
        if anomaly_type == 'power_drop':
            # Sudden drop in power (e.g., thermal throttling or connection issue)
            power_values[anomaly_idx:] *= 0.4
        
        elif anomaly_type == 'power_spike':
            # Sensor spike
            power_values[anomaly_idx] += max_power * 0.8
            
        elif anomaly_type == 'soc_jump':
            # Sensor error: sudden jump in SOC
            soc_values[anomaly_idx:] += 10.0
            soc_values = np.clip(soc_values, 0, 105) # Keep within reasonable bounds
            
        elif anomaly_type == 'plateau':
            # Power stops increasing and stays flat/constant unexpectedly
            power_values[anomaly_idx:] = power_values[anomaly_idx]

        # 3. Finalizing Data
        df = pd.DataFrame({
            'timestamp': timestamps,
            'soc': soc_values,
            'power_kw': power_values
        })

        # 4. Save to Individual CSV
        file_name = f"anomaly_{i:03d}.csv"
        file_path = os.path.join(output_dir, file_name)
        df.to_csv(file_path, index=False)

    print(f"Successfully generated {num_curves} anomalous curves in '{output_dir}/'")

if __name__ == "__main__":
    generate_anomalous_ev_dataset()
