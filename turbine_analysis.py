import pandas as pd

"""
###############################################################################
   
   File        : turbine_analysis.js
   
   Date        : Wednesday 17th June 2026
   
   Author      : Tom Melton
   
   Description : Script to identify faulty turbines based on anomalies from
                 telemetry date
    
   History     : 17/06/2026 - v1.0
   
###############################################################################
"""

# Define constants   
PATH            = "telemetry_data.xlsx"
MAX_AVE_TEMP    = 85 #°c
MAX_VIB         = 15 #mms⁻¹


# Read in telemetry data as a dataframe
df = pd.read_excel(PATH)


# Find turbines exceesing the maximum average temperature
aveTemps = df.groupby("turbine_id", as_index=False)["temperature_c"].mean()
tempOutliers = aveTemps[aveTemps["temperature_c"] > MAX_AVE_TEMP]
tempOutliers = tempOutliers["turbine_id"].to_list()


# Find turbines exceeding the maximum vibration level
vibOutliers = df[df["vibration_mm_s"] > MAX_VIB]
vibOutliers = vibOutliers["turbine_id"].drop_duplicates()
vibOutliers = vibOutliers.to_list()


# Display results
print("Analysis Results:")
print(f"- Vibrations > {MAX_VIB} mms⁻¹: {vibOutliers}")
print(f"- Ave Temp > {MAX_AVE_TEMP} °c: {tempOutliers}")