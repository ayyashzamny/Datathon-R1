import pandas as pd
import numpy as np
import plotly.graph_objects as go  # For interactive plots
import seaborn as sns

# Load the cleaned data
solar_data = pd.read_csv('data/cleaned_solar_data.csv')
weather_data = pd.read_csv('data/cleaned_weather_data.csv')

# Convert 'DATE_TIME' column to datetime format for both datasets
solar_data['DATE_TIME'] = pd.to_datetime(solar_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

# Merge the solar and weather data on 'DATE_TIME'
combined_data = pd.merge(solar_data, weather_data, on='DATE_TIME', how='inner')

# Visualize power generation trends (AC_POWER over time)
fig1 = go.Figure()

# Add AC Power line plot
fig1.add_trace(go.Scatter(x=combined_data['DATE_TIME'], y=combined_data['AC_POWER'],
                         mode='lines', name='AC Power', line=dict(color='blue')))

# Add DC Power line plot
fig1.add_trace(go.Scatter(x=combined_data['DATE_TIME'], y=combined_data['DC_POWER'],
                         mode='lines', name='DC Power', line=dict(color='red', dash='dash')))

fig1.update_layout(
    title='Power Generation (AC and DC) Over Time',
    xaxis_title='Date Time',
    yaxis_title='Power (W)',
    xaxis=dict(tickangle=45),
    template="plotly_dark"
)

fig1.write_image('outputs/power_generation_trend_plotly.png')
fig1.show()

# Visualize power generation and weather variables (e.g., Temperature and Irradiation)
fig2 = go.Figure()

# Scatter plot for Ambient Temperature vs AC Power
fig2.add_trace(go.Scatter(x=combined_data['AMBIENT_TEMPERATURE'], y=combined_data['AC_POWER'],
                         mode='markers', name='AC Power vs Temperature', marker=dict(color='green', opacity=0.5)))

# Scatter plot for Irradiation vs AC Power
fig2.add_trace(go.Scatter(x=combined_data['IRRADIATION'], y=combined_data['AC_POWER'],
                         mode='markers', name='AC Power vs Irradiation', marker=dict(color='orange', opacity=0.5)))

fig2.update_layout(
    title='AC Power vs Weather Variables',
    xaxis_title='Variable Value',
    yaxis_title='AC Power (W)',
    template="plotly_dark",
    showlegend=True
)

fig2.write_image('outputs/scatter_plots_plotly.png')
fig2.show()

# Calculate the correlation matrix between weather variables and power generation
correlation_data = combined_data[['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION', 'AC_POWER', 'DC_POWER']]
correlation_matrix = correlation_data.corr()

# Visualize the correlation matrix as a heatmap using seaborn (since Plotly doesn't handle heatmaps as easily)
plt = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.set_title('Correlation Matrix Between Weather Variables and Power Generation')
plt.tight_layout()
plt.savefig('outputs/correlation_matrix_plotly.png')
plt.show()

# Anomaly detection: Look for anomalies by checking for outliers or deviations in trends
low_power_threshold = 50  # Example threshold for low AC Power (in watts)

anomalies = combined_data[combined_data['AC_POWER'] < low_power_threshold]
anomalies.to_csv('outputs/anomalies_detected.csv', index=False)

# Visualize anomalies on the power generation plot using Plotly
fig3 = go.Figure()

# Add AC Power line plot
fig3.add_trace(go.Scatter(x=combined_data['DATE_TIME'], y=combined_data['AC_POWER'],
                         mode='lines', name='AC Power', line=dict(color='blue')))

# Add anomalies as scatter plot
fig3.add_trace(go.Scatter(x=anomalies['DATE_TIME'], y=anomalies['AC_POWER'],
                         mode='markers', name='Anomalies', marker=dict(color='red', size=8, symbol='x')))

fig3.update_layout(
    title='AC Power with Anomalies Highlighted',
    xaxis_title='Date Time',
    yaxis_title='Power (W)',
    xaxis=dict(tickangle=45),
    template="plotly_dark"
)

fig3.write_image('outputs/anomaly_detection_plotly.png')
fig3.show()

# End of analysis
