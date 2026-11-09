import datetime

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Open-Meteo forecast endpoint; change these coordinates to your location.
API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=40.7128&longitude=-74.0060"
    "&hourly=temperature_2m&timezone=auto"
)
FETCH_INTERVAL_SECONDS = 5

data_log = {"Timestamp": [], "Temperature": []}


def fetch_live_weather():
    """Fetch hourly temperatures and return the value closest to now."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        raw_json = response.json()

        hourly = raw_json["hourly"]
        df = pd.DataFrame(
            {"time": hourly["time"], "temp": hourly["temperature_2m"]}
        )
        df["time"] = pd.to_datetime(df["time"])

        # Open-Meteo returns local times for the requested timezone.
        now = pd.Timestamp.now().tz_localize(None)
        closest_index = (df["time"] - now).abs().idxmin()
        temperature = df.loc[closest_index, "temp"]
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        return timestamp, temperature
    except (requests.RequestException, KeyError, ValueError, TypeError) as error:
        print(f"Weather data fetch failed: {error}")
        return None, None


fig, ax = plt.subplots(figsize=(10, 5))


def update_dashboard(_frame):
    """Fetch a reading and refresh the chart."""
    timestamp, temperature = fetch_live_weather()
    if timestamp is None or temperature is None or pd.isna(temperature):
        return

    data_log["Timestamp"].append(timestamp)
    data_log["Temperature"].append(temperature)
    if len(data_log["Timestamp"]) > 15:
        data_log["Timestamp"].pop(0)
        data_log["Temperature"].pop(0)

    ax.clear()
    ax.plot(
        data_log["Timestamp"],
        data_log["Temperature"],
        marker="o",
        color="#e74c3c",
        linewidth=2.5,
        label="Live Temperature (°C)",
    )
    ax.set_title(
        "Group 15: Real-Time Weather Processing Pipeline",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Pipeline System Time (HH:MM:SS)", fontsize=11, labelpad=10)
    ax.set_ylabel("Temperature Values (°C)", fontsize=11, labelpad=10)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    plt.xticks(rotation=35)
    plt.tight_layout()


ani = animation.FuncAnimation(
    fig,
    update_dashboard,
    interval=FETCH_INTERVAL_SECONDS * 1000,
    cache_frame_data=False,
)
plt.show()