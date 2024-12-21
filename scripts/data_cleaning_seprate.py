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

# Step 5: Standardize DATE_TIME format for Location A and B
def standardize_date_time(row):
    if row['LOCATION'] == 'A':
        # For Location A, the format is 'DD-MM-YYYY HH:MM'
        return pd.to_datetime(row['DATE_TIME'], format='%d-%m-%Y %H:%M', errors='coerce')
    elif row['LOCATION'] == 'B':
        # For Location B, the format is 'M/D/YYYY H:MM'
        return pd.to_datetime(row['DATE_TIME'], format='%m/%d/%Y %H:%M', errors='coerce')
    return pd.NaT  # Return NaT for any invalid formats

# Apply the function to standardize the date format
solar_data['DATE_TIME'] = solar_data.apply(standardize_date_time, axis=1)

# Check if there are any NaT values after date parsing
if solar_data['DATE_TIME'].isnull().sum() > 0 or weather_data['DATE_TIME'].isnull().sum() > 0:
    print("Warning: There are invalid date entries.")
else:
    print("Dates parsed successfully.")

# Step 6: Remove duplicates from each dataset
solar_data.drop_duplicates(inplace=True)
weather_data.drop_duplicates(inplace=True)

# Step 7: Remove outliers from solar data (Optional: Remove rows where DC_POWER is negative)
solar_data = solar_data[solar_data['DC_POWER'] >= 0]

# Step 8: Save the cleaned datasets separately
solar_data.to_csv('cleaned_solar_data.csv', index=False)
weather_data.to_csv('cleaned_weather_data.csv', index=False)

print("Data cleaning completed and saved as 'cleaned_solar_data.csv' and 'cleaned_weather_data.csv'")
