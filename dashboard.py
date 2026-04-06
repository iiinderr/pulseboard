import sys
import time
import argparse
import datetime
import requests

class C:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED   = "\033[91m"
    CYAN  = "\033[96m"
    WHITE = "\033[97m"

def g(text, color):
    return f"{color}{text}{C.RESET}"

def print_banner():
    print(g("PulseBoard Dashboard", C.CYAN))
    print(g(f"Time: {datetime.datetime.now()}", C.WHITE))

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
} 

def fetch_weather():
    # Step 1: Get location
    loc = requests.get("https://ipapi.co/json/" , timeout =5).json()

    lat = loc.get("latitude")
    lon = loc.get("longitude")
    city = loc.get("city", "Unknown")

    # If location failed
    if not lat or not lon:
        return city, "N/A", "Location error"

    # Step 2: Weather API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
    data = requests.get(url).json()

    temp = data["current"]["temperature_2m"]
    code = data["current"]["weather_code"]

    desc = WEATHER_CODES.get(code, "Unknown")

    return city, temp, desc


def print_weather():
    city, temp, desc = fetch_weather()
    
    print(g("\nWeather:", C.CYAN))
    print(g(f"City: {city}", C.WHITE))
    print(g(f"Temperature: {temp}°C", C.GREEN))
    print(g(f"Condition: {desc}", C.WHITE))

if __name__ == "__main__":
    print_banner()
    print_weather()