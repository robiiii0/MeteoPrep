import joblib
import pandas as pd
import requests
from datetime import datetime
import argparse
import numpy as np
import os

    

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Predict avalanche risk based on location."
    )
    parser.add_argument("latitude", type=float, help="Latitude of the location")
    parser.add_argument("longitude", type=float, help="Longitude of the location")
    return parser.parse_args()


def main():
    args = parse_arguments()
    latitude = args.latitude
    longitude = args.longitude

    print(f"📡 Fetching weather for lat={latitude}, lon={longitude}...")



if __name__ == "__main__":
    main()