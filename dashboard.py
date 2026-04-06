import sys
import time
import argparse
import datetime
import requests
import json
import os



# ───────────── COLORS ─────────────
class C:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED   = "\033[91m"
    CYAN  = "\033[96m"
    WHITE = "\033[97m"


def g(text, color):
    return f"{color}{text}{C.RESET}"


# ───────────── BANNER ─────────────
def print_banner():
    print(g("PulseBoard Dashboard", C.CYAN))
    print(g(f"Time: {datetime.datetime.now()}", C.WHITE))


# ───────────── UI HELPERS ─────────────
def section(title, emoji):
    print(g(f"\n┌─ {emoji} {title} ─" + "─" * 40, C.CYAN))


def section_end():
    print(g("└" + "─" * 50, C.CYAN))


def row(label, value):
    return f"  {label.ljust(20)} {value}"


# ───────────── WEATHER DATA ─────────────
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
}


def fetch_weather():
    try:
        # location API
        if os.path.exists("location.json"):
            with open("location.json") as f:
                data = json.load(f)
        else:
            data = requests.get("https://ipapi.co/json/").json()
            with open("location.json", "w") as f:
                json.dump(data, f)
        
        # print(data)

        loc = data

        lat = loc.get("latitude")
        lon = loc.get("longitude")
        city = loc.get("city", "Unknown")

        # fallback if API fails
        if not lat or not lon:
            lat = 28.61
            lon = 77.23
            city = "New Delhi"

        # Step 2: weather API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        data = requests.get(url, timeout=5).json()

        current = data.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        code = current.get("weather_code", -1)

        desc = WEATHER_CODES.get(code, "Unknown")

        return city, temp, desc

    except Exception:
        return "Unknown", "N/A", "API error"


# ───────────── PRINT WEATHER ─────────────
def print_weather():
    city, temp, desc = fetch_weather()

    section("Weather Report", "🌡")

    print(row("Location", city))
    print(row("Temperature", g(f"{temp}°C", C.GREEN)))
    print(row("Condition", desc))

    section_end()

COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL"
}

def fetch_crypto():
    ids = ",".join(COINS.keys())

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

    data = requests.get(url, timeout=5).json()

    results = []

    for coin, symbol in COINS.items():
        price = data.get(coin, {}).get("usd", "N/A")

        results.append((symbol, price))

    return results

def print_crypto():
    coins = fetch_crypto()

    section("Crypto Market", "💎")

    for symbol, price in coins:
        print(row(symbol, f"${price}"))

    section_end()


# ───────────── MAIN ─────────────
if __name__ == "__main__":
    print_banner()
    print_weather()
    print_crypto()