# Project AirCast: Low-Cost PM2.5 Forecasting
## Summary
AirCast is a machine learning project with the aim of forecasting particulate matter (PM2.5) conentrations using low-cost sensor data. By integrating historical air quality measurements from the **OpenAQ** platform combined with meteorological variables, the model aims to provide actionable 3-hour and 6-hour ahead forecasts.
## Data Architecture
### Sensor data (OpenAQ)
I utilize the OpenAQ Python SDK to ingest high-frequency PM2.5 data. While the sensors provide PM1 and others, PM2.5 is as the primary target.
For this prototype, I am using one location from the center of Munich, Germany.
### Feature engineering
We generate time series features in categories:
- Date features (Pandas datetime)
    - year
    - month
    - day_of_week
    - is_weekend
    - is_holiday
    - hour_of_day
    - sin / cos representations
- Rolling & lag
    - Rolling mean 12h
    - Lag 3h | 6h | 9h | 12h
- Environmental (various APIs)
    - Wind speed
    - Wind direction
    - Barometric pressure
    - Rain
# Modelling
## Target
The target is a negatively shifted pm25. This allows the model to learn how the pm25 values is different in the future.
## Experiments
### Number 1: Ridge regression, basic features, 3 hours lead
![image](./images/3hr_lead_ridge.png)
We observe some lag, indicating that the model is purely considering the past pm25 values. Feature importance supports this.

# TODOs:
- More data: Currently, the model only has 3 months of data from 2026.
- Better features: Include wind, pressure, weather
- Tuning: Use Optuna for hyperparameter search