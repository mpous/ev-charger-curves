import numpy as np
import pandas as pd
import os

def generate_ev_charging_dataset(num_curves=100, output_dir="ev_dataset"):
    """
    Generates a synthetic dataset of EV charging curves following a CC-CV profile.
    
    Args:
        num_curves (int): Number of individual charging sessions to generate.
        output_dir (str): Folder where the CSV files will be    saved.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    for i in range(1, num_curves + 1):
        # 1. Randomize Session Parameters
        start_soc = np.random.uniform(10, 70)  # Start SOC between 10% and 70%
        knee_soc = np.random.uniform(75, 85)   # Knee point SOC between 75% and 85%
        max_power = np.random.uniform(50, 150) # Max power between 50kW and 150kW
        decay_rate = np.random.uniform(0.05, 0.2) # Randomized decay rate for CV phase
        
        # 2. Generate Time-steps and SOC progression
        # We define 100 steps from start_soc to 100%
        steps = 100
        soc_values = np.linspace(start_soc, 100, steps)
        
        # Timestamps: assume 10-second intervals per step
        timestamps = np.arange(0, steps * 10, 10)
        
        # 3. Generate Power Profile (CC-CV)
        power_values = np.zeros(steps)
        
        for j in range(steps):
            current_soc = soc_values[j]
            
            if current_soc < knee_soc:
                # Phase 1: Constant Current (CC)
                power_values[j] = max_power
            else:
                # Phase 2: Constant Voltage (CV) - Exponential decay
                # Power decays proportional to the SOC increase past the knee point
                power_values[j] = max_power * np.exp(-decay_rate * (current_soc - knee_soc))
        
        # 4. Add Gaussian Noise to simulate real-world fluctuations
        # Add a small amount of noise (approx 2% of max power)
        noise = np.random.normal(0, max_power * 0.02, steps)
        power_values += noise
        
        # Ensure power doesn't drop below zero due to noise
        power_values = np.maximum(power_values, 0)

        # 5. Structure Data into a DataFrame
        df = pd.DataFrame({
            'timestamp': timestamps,
            'soc': soc_values,
            'power_kw': power_values
        })

        # 6. Save to Individual CSV
        file_name = f"curve_{i:03d}.csv"
        file_path = os.path.join(output_dir, file_name)
        df.to_csv(file_path, index=False)

    print(f"Successfully generated {num_curves} curves in '{output_dir}/'")

if __name__ == "__main__":
    # Run the generator
    generate_ev_charging_dataset()
