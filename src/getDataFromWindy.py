import pandas as pd
import requests
from datetime import datetime
import argparse
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_weather_data_from_windy(lat, lon):
    """
    Récupère les données météo depuis l'API Windy en utilisant la latitude et la longitude données.
    """
    url = "https://api.windy.com/api/point-forecast/v2"
    api_key = os.getenv("WINDY_API_KEY")  # Assurez-vous que la clé API est dans votre fichier .env

    headers = {
        "Content-Type": "application/json"
    }

    # Construction du corps de la requête
    request_body = {
        "lat": lat,
        "lon": lon,
        "model": "iconEu",
        "parameters": ["wind", "windGust", "ptype", "lclouds", "rh", "temp", "snowPrecip", "pressure"],
        "levels": ["surface"],
        "key": api_key
    }

    try:
        response = requests.post(url, json=request_body, headers=headers)
        response.raise_for_status()  # Vérifie que la requête s'est bien déroulée
        return response.json()  # Retourne la réponse en format JSON
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch weather data from Windy API: {e}")
        return None

def process_weather_data(data):
    """
    Traite les données météo récupérées pour les rendre exploitables.
    """
    try:
        ts_list = data["ts"]
        now_ms = int(datetime.now().timestamp() * 1000)
        ts_array = np.array(ts_list)
        closest_index = np.argmin(np.abs(ts_array - now_ms))

        temp = data["temp-surface"][closest_index]
        wind_u = data["wind_u-surface"][closest_index]
        wind_v = data["wind_v-surface"][closest_index]
        gust = data["gust-surface"][closest_index]
        precip = data["past3hsnowprecip-surface"][closest_index]

        return {
            "timestamp": datetime.fromtimestamp(ts_list[closest_index] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_day": temp,
            "temperature_night": temp - 3,
            "snowfall": precip,
            "snow_3d_accum": 0,
            "type_of_snow": "Old",
            "snow_humidity": 70,
            "precipitation_cumulated": precip,
            "wind_avg": (wind_u**2 + wind_v**2) ** 0.5,
            "wind_gust": gust,
            "altitude": 1800,
            "slope_angle": 35,
            "orientation": "N",
            "temp_variation": 3,
            "wind_gust_ratio": gust / ((wind_u**2 + wind_v**2) ** 0.5 + 1e-6),
            "snowpack_stability": 0.75,
        }

    except KeyError as e:
        print(f"KeyError: Missing expected field: {e}")
        return None


def parse_arguments():
    """
    Parse les arguments de ligne de commande pour obtenir la latitude et la longitude.
    """
    parser = argparse.ArgumentParser(description="Predict avalanche risk based on location.")
    parser.add_argument("latitude", type=float, help="Latitude of the location")
    parser.add_argument("longitude", type=float, help="Longitude of the location")
    return parser.parse_args()


def main():
    """
    Fonction principale pour récupérer et afficher les données météo.
    """
    args = parse_arguments()
    latitude = args.latitude
    longitude = args.longitude

    print(f"📡 Fetching weather for lat={latitude}, lon={longitude}...")

    # Récupération des données météo depuis l'API
    weather_data = fetch_weather_data_from_windy(latitude, longitude)

    # Si des données ont été récupérées, les traiter et les afficher
    if weather_data:
        processed_data = process_weather_data(weather_data)
        if processed_data:
            print("Processed Data:", processed_data)
        else:
            print("Failed to process the data.")
    else:
        print("Failed to fetch weather data.")


if __name__ == "__main__":
    main()
