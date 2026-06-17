import pandas as pd
import matplotlib.pyplot as plt
import os

"""
###############################################################################
   
   File        : turbine_analysis.js
   
   Date        : Wednesday 17th June 2026
   
   Author      : Tom Melton
   
   Description : Script to identify faulty turbines based on anomalies from
                 telemetry data
    
   History     : 17/06/2026 - v1.0
   
###############################################################################
"""


"""
How to run this file:
- Have Docker installed
- In the terminal run 'docker compose up'
- Outling turbines will be returned to the console
- Graphs of turbine analytics will be saved to /outputs
"""


# Define constants   
PATH            = "telemetry_data.xlsx"
MAX_AVE_TEMP    = 85 #°c
MAX_VIB         = 15 #mms⁻¹
OUTPUT_DIR      = "/app/outputs"

# Create outputs directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read in telemetry data as a dataframe
df = pd.read_excel(PATH)



# Convert timestamp into datetime datatype
df["timestamp"] = pd.to_datetime(df["timestamp"])



# Find turbines exceesing the maximum average temperature
aveTemps = df.groupby("turbine_id", as_index=False)["temperature_c"].mean()
tempOutliersGroup = aveTemps[aveTemps["temperature_c"] > MAX_AVE_TEMP]
tempOutliers = tempOutliersGroup["turbine_id"].to_list()



# Find turbines exceeding the maximum vibration level
vibOutliersGroup = df[df["vibration_mm_s"] > MAX_VIB]
vibOutliersAve = vibOutliersGroup.groupby("turbine_id", as_index=False)["vibration_mm_s"].mean()
vibOutliers = vibOutliersGroup["turbine_id"].drop_duplicates()
vibOutliers = vibOutliers.to_list()



# Display results
print("Analysis Results:")
print(f"- Ave Temp > {MAX_AVE_TEMP} °c: {tempOutliers}, {tempOutliersGroup['temperature_c'].to_list()}")
print(f"- Vibrations > {MAX_VIB} mms⁻¹: {vibOutliers}, {vibOutliersAve['vibration_mm_s'].to_list()}")



# Produce graph of temp over time for affected turbines
plt.figure(figsize=(15, 5)) #Graph dimentions

# Plot affected turbines
for turbine_id, group in df[df["turbine_id"].isin(tempOutliers)].groupby("turbine_id"):
    group = group.sort_values("timestamp")
    plt.plot(group["timestamp"], group["temperature_c"], label=turbine_id)

# Plot threshold line
plt.axhline(y=MAX_AVE_TEMP, linestyle="--", color="red", label="Average Temperature Threshold")

# Calculate and plot average temp of unaffected turbines
inlierAveTemps =  df[~df["turbine_id"].isin(tempOutliers)].groupby("timestamp")["temperature_c"].mean()
plt.plot(inlierAveTemps, label="Average Inlier Temperature")

# Configure graph
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Outlier Turbine Temperature Over Time")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/temperature_outliers.png", dpi=100, bbox_inches="tight")
print(f"Saved: {OUTPUT_DIR}/temperature_outliers.png")
plt.close()



# Produce graph of vibrations over time for affected turbines
plt.figure(figsize=(15, 5)) #Graph dinentions

# Plot affected turbines
for turbine_id, group in df[df["turbine_id"].isin(vibOutliers)].groupby("turbine_id"):
    group = group.sort_values("timestamp")
    plt.plot(group["timestamp"], group["vibration_mm_s"], label=turbine_id)

# Plot threshold line
plt.axhline(y=MAX_VIB, linestyle="--", color="red", label="Vibration Threshold")

# Calculate and plot average vibrations of unaffected turbines
inlierAveVibs =  df[~df["turbine_id"].isin(vibOutliers)].groupby("timestamp")["vibration_mm_s"].mean()
plt.plot(inlierAveVibs, label="Average Inlier Vibrations")

# Configure graph
plt.xlabel("Time")
plt.ylabel("Vibrations (mms⁻¹)")
plt.title("Outlier Turbine Vibrations Over Time")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/vibration_outliers.png", dpi=100, bbox_inches="tight")
print(f"Saved: {OUTPUT_DIR}/vibration_outliers.png")
plt.close()
