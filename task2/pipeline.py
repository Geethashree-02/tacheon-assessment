import requests
import logging
import pandas as pd
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parameters (easy to change)
LATITUDE = 12.9
LONGITUDE = 77.6
CITY = "Bangalore"

def fetch_weather(latitude=LATITUDE, longitude=LONGITUDE):
    """Fetch weather data from Open-Meteo API"""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
        f"&forecast_days=7"
    )
    try:
        logging.info(f"Fetching weather data for {CITY}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Data fetched successfully!")
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Request timed out!")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def transform_data(raw_data):
    """Transform raw API data into clean tabular format"""
    if not raw_data:
        logging.error("No data to transform!")
        return None

    hourly = raw_data["hourly"]

    df = pd.DataFrame({
        "timestamp": hourly["time"],
        "temperature_c": hourly["temperature_2m"],
        "humidity_percent": hourly["relative_humidity_2m"],
        "windspeed_kmh": hourly["windspeed_10m"],
        "city": CITY,
        "latitude": raw_data["latitude"],
        "longitude": raw_data["longitude"],
    })

    # Handle nulls
    df = df.dropna()

    # Derived fields
    df["temperature_f"] = (df["temperature_c"] * 9/5) + 32
    df["feels_hot"] = df["temperature_c"] > 30
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    df["fetched_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    logging.info(f"Transformed {len(df)} rows of data!")
    return df

if __name__ == "__main__":
    raw = fetch_weather()
    df = transform_data(raw)
    if df is not None:
        print(df.head(10))
        df.to_csv("weather_output.csv", index=False)
        logging.info("Saved to weather_output.csv!")