from datetime import datetime, timedelta

import pandas as pd
import requests
from ascend.application.context import ComponentExecutionContext
from ascend.common.events import log
from ascend.resources import read, test


@read(
    tests=[
        test("count_greater_than", count=0),
        test("not_null", column="time"),
        test("not_null", column="temperature_2m"),
    ],
    on_schema_change="sync_all_columns",
)
def weather_api_data(context: ComponentExecutionContext) -> pd.DataFrame:
    """
    Fetch hourly weather data from Open-Meteo API for the last 31 days.

    Args:
        context (ComponentExecutionContext): The execution context

    Returns:
        pd.DataFrame: Hourly weather data including temperature, humidity, precipitation, etc.
    """
    # Calculate date range (last 31 days)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=31)

    # Open-Meteo API endpoint for San Francisco (default location)
    # You can modify latitude/longitude as needed
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": 37.7749,  # San Francisco
        "longitude": -122.4194,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m",
        ],
        "timezone": "America/Los_Angeles",
    }

    log(f"Fetching weather data from {start_date} to {end_date}")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Extract hourly data
        hourly_data = data.get("hourly", {})

        # Create DataFrame
        df = pd.DataFrame(
            {
                "time": pd.to_datetime(hourly_data["time"]),
                "temperature_2m": hourly_data["temperature_2m"],
                "relative_humidity_2m": hourly_data["relative_humidity_2m"],
                "precipitation": hourly_data["precipitation"],
                "wind_speed_10m": hourly_data["wind_speed_10m"],
                "wind_direction_10m": hourly_data["wind_direction_10m"],
            }
        )

        log(f"Successfully fetched {len(df)} hourly weather records")

        return df

    except requests.exceptions.RequestException as e:
        log(f"Error fetching weather data: {str(e)}")
        raise
    except (KeyError, ValueError) as e:
        log(f"Error parsing weather data: {str(e)}")
        raise
