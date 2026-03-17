# Project Summary
Forecast air quality using a low-cost sensor.

# Data
Pre-training on: OpenQA Dataset using the Python SDK by OpenQA

# Feature engineering
We generate time series features in categories:
1. Sensor data (OpenAQ API)
    1.1. pm1
    1.2. pm25
    1.3. um003
2. Date features (Pandas datetime)
    2.1. year
    2.2. month
    2.3. day_of_week
    2.4. is_weekend
    2.5. is_holiday
    2.6. hour_of_day
3. Rolling & lag
    3.1. Rolling mean 12h | 24h for pm1 and pm25
    3.2. Lag 3h | 6h | 9h | 12h for pm1 and pm25
4. Environmental (various APIs)
    4.1. Wind speed
    4.2. Wind direction
    4.3. Barometric pressure
    4.4. Rain
