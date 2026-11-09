import pandas as pd
import requests

# Your specific Open-Meteo API endpoint
url = "https://api.open-meteo.com/v1/forecast?latitude=9.0765&longitude=7.3986&hourly=temperature_2m&forecast_days=1&timezone=Africa%2FLagos"

try:
    # 1. Fetch the live data from the API
    response = requests.get(url)
    response.raise_for_status()  # Check for errors
    data = response.json()

    # 2. Extract the nested hourly data
    # The JSON structure groups times and values into separate lists under 'hourly'
    hourly_data = data["hourly"]

    # 3. Process into a pandas DataFrame
    df = pd.DataFrame(
        {
            "Time": hourly_data["time"],
            "Temperature (°C)": hourly_data["temperature_2m"],
        }
    )

    # 4. (Optional) Convert Time string to actual Datetime object for analysis
    df["Time"] = pd.to_datetime(df["Time"])

    # Display the final structured data
    print("--- Weather Data Successfully Processed ---")
    print(df)

except Exception as e:
    print(f"An error occurred: {e}")
