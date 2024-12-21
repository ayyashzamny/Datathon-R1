import pandas as pd
import numpy as np

# Step 1: Load the datasets
solar_data = pd.read_csv('solar_sensor_data.csv')
weather_data = pd.read_csv('weather_sensor_data.csv')

# Step 2: View the first few rows to understand the structure of the data
print("Solar Data:")
print(solar_data.head())
print("\nWeather Data:")
print(weather_data.head())

# Step 3: Check for missing values
print("\nMissing values in Solar Data:")
print(solar_data.isnull().sum())
print("\nMissing values in Weather Data:")
print(weather_data.isnull().sum())

# Step 4: Handle missing values
solar_data.ffill(inplace=True)  # Forward-fill missing values
weather_data.ffill(inplace=True)  # Forward-fill missing values

# Step 5: Ensure timestamps are in correct format (let pandas infer the format)
solar_data['DATE_TIME'] = pd.to_datetime(solar_data['DATE_TIME'], errors='coerce', dayfirst=True)
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'], errors='coerce')

# Check if there are any NaT values after date parsing
if solar_data['DATE_TIME'].isnull().sum() > 0 or weather_data['DATE_TIME'].isnull().sum() > 0:
    print("Warning: There are invalid date entries.")
else:
    print("Dates parsed successfully.")

# Step 6: Merge the datasets on the 'DATE_TIME' column
combined_data = pd.merge(solar_data, weather_data, on='DATE_TIME', how='inner')

# Step 7: Remove duplicates
combined_data.drop_duplicates(inplace=True)

# Step 8: Remove outliers (Optional: Remove rows where DC_POWER is negative)
combined_data = combined_data[combined_data['DC_POWER'] >= 0]

# Step 9: Save the cleaned data
combined_data.to_csv('cleaned_data.csv', index=False)
print("Data cleaning completed and saved as 'cleaned_data.csv'")
