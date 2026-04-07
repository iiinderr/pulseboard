import sys
import time
import argparse
import datetime
import requests
import json
import os


WEATHER_CACHE = "weather.json"
CRYPTO_CACHE  = "crypto.json"
STOCKS_CAHCE = "stocks.json"
CACHE_TTL     = 60 * 10  # 10 minutes

def is_cache_valid(path):
    if not os.path.exists(path):
        return False
    age = time.time() - os.path.getmtime(path)
    return age < CACHE_TTL

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
        # --- location (existing cache logic) ---
        if os.path.exists("location.json"):
            with open("location.json") as f:
                loc = json.load(f)
        else:
            loc = requests.get("https://ipapi.co/json/", timeout=5).json()
            with open("location.json", "w") as f:
                json.dump(loc, f)

        lat  = loc.get("latitude")
        lon  = loc.get("longitude")
        city = loc.get("city", "Unknown")

        if not lat or not lon:
            lat, lon, city = 28.61, 77.23, "New Delhi"

        # --- weather cache ---
        if is_cache_valid(WEATHER_CACHE):
            with open(WEATHER_CACHE) as f:
                data = json.load(f)
        else:
            url  = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
            data = requests.get(url, timeout=5).json()

            # only save if we got real data
            if "current" in data:
                with open(WEATHER_CACHE, "w") as f:
                    json.dump(data, f)

        current = data.get("current", {})
        temp    = current.get("temperature_2m", "N/A")
        code    = current.get("weather_code", -1)
        desc    = WEATHER_CODES.get(code, "Unknown")

        return city, temp, desc

    except Exception:
        return "Unknown", "N/A", "API error"


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
    try:
        if is_cache_valid(CRYPTO_CACHE):
            with open(CRYPTO_CACHE) as f:
                data = json.load(f)
        else:
            ids  = ",".join(COINS.keys())
            url  = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
            data = requests.get(url, timeout=5).json()

            # only save if we got real prices (not an error dict)
            if any(k in data for k in COINS):
                with open(CRYPTO_CACHE, "w") as f:
                    json.dump(data, f)

        results = []
        for coin, symbol in COINS.items():
            price = data.get(coin, {}).get("usd", "N/A")
            results.append((symbol, price))

        return results

    except Exception:
        return [(symbol, "N/A") for symbol in COINS.values()]

def print_crypto():
    coins = fetch_crypto()

    section("Crypto Market", "💎")

    for symbol, price in coins:
        print(row(symbol, f"${price}"))

    section_end()

TICKERS = {
    "AAPL": "Apple",
    "GOOGL": "Google",
    "TSLA": "Tesla"
}

def fetch_stocks():
    try:
        if is_cache_valid(STOCKS_CAHCE):
            with open(STOCKS_CAHCE) as f:
                data = json.load(f)
        else:
            symbols = ",".join(TICKERS.keys())
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
            headers = {"User-Agent": "Mozilla/5.0"}
            data = requests.get(url, headers=headers, timeout=5).json()

            # only save if we got real quotes
            quotes = data.get("quoteResponse", {}).get("result", [])
            if quotes:
                with open(STOCKS_CAHCE, "w") as f:
                    json.dump(data, f)

        results = []
        quotes = data.get("quoteResponse", {}).get("result", [])
        for q in quotes:
            ticker = q.get("symbol")
            price = q.get("regularMarketPrice", "N/A")
            results.append((ticker, price))

        return results

    except Exception:
        return [(ticker, "N/A") for ticker in TICKERS.keys()]

def print_stocks():
    stocks = fetch_stocks()

    section("Stock Market", "📈")

    for ticker, price in stocks:
        print(row(ticker, f"${price}"))

    section_end()


# ───────────── MAIN ─────────────
if __name__ == "__main__":
    print_banner()
    print_weather()
    print_crypto()
    print_stocks()