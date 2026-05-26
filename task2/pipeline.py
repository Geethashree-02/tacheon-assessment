import requests
import logging
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parameters
LATITUDE = 12.9
LONGITUDE = 77.6
CITY = "Bangalore"
PROJECT_ID = "tacheon-assessment-497521"
DATASET_ID = "weather_data"
TABLE_ID = "hourly_weather"
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

def fetch_weather(latitude=LATITUDE, longitude=LONGITUDE):
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
    df = df.dropna()
    df["temperature_f"] = (df["temperature_c"] * 9/5) + 32
    df["feels_hot"] = df["temperature_c"] > 30
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date.astype(str)
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    df["fetched_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Transformed {len(df)} rows!")
    return df

def load_to_bigquery(df):
    try:
        client = bigquery.Client.from_service_account_json(CREDENTIALS_PATH)
        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        logging.info(f"Loaded {len(df)} rows to BigQuery table {table_ref}!")
    except Exception as e:
        logging.error(f"BigQuery load failed: {e}")

if __name__ == "__main__":
    raw = fetch_weather()
    df = transform_data(raw)
    if df is not None:
        print(df.head(5))
        df.to_csv("weather_output.csv", index=False)
        load_to_bigquery(df)
        logging.info("Pipeline complete!")