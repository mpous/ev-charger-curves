# EV Charging Curve Synthetic Data Generator

This project provides a Python-based utility to generate high-fidelity synthetic datasets of Electric Vehicle (EV) charging profiles.

## Purpose
The primary goal of this project is to provide a controlled, high-volume dataset for training machine learning models for anomaly detection on the Edge Impulse Studio. By generating both "clean" charging profiles (CC-CV) and "anomalous" profiles (spikes, drops, etc.), you can create a robust training set for detecting battery or charger malfunctions.

## Features
- **CC-CV Profile Generation**: Simulates the standard Constant Current - Constant Voltage charging behavior.
- **Randomized Parameters**: Each curve features randomized start SOC, knee points, max power, and decay rates to simulate diverse vehicle models.
- **Anomaly Injection**: A specialized script to inject realistic electrical anomalies like power drops, sensor spikes, and SOC jumps.
- **Edge Impulse Ready**: Outputs individual `.csv` files that can be directly uploaded to Edge Impulse via the Data Acquisition wizard.

## Local Setup

### 1. Prerequisites
Ensure you have Python 3 installed on your system.

### 2. Setup Virtual Environment
It is recommended to use a virtual environment to manage dependencies:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

### 3. Install Dependencies
Install the required libraries using the provided requirements file:
```bash
pip install -r requirements.txt
```

### 3. Running the Generators

#### To generate Clean Data:
This will create 100 clean charging curves in the `ev_dataset/` folder.
```bash
python3 generate_ev_data.py
```

#### To generate Anomalous Data:
This will create 50 curves with injected anomalies in the `ev_dataset_anomalies/` folder.
```bash
python3 generate_ev_anomalies.py
```

## Deployment to Edge Impulse
1. Log in to your **Edge Impulse Studio** project.
2. Navigate to the **Data Acquisition** tab.
3. Click **Upload Data**.
4. Select all `.csv` files from your desired folder (`ev_dataset` or `ev_dataset_anomalies`).
5. Start training your Anomaly Detection (GDORN) model!
