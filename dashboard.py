import sys
import time
import argparse
import datetime
import requests
import json
import os

# ───────────── ENV LOAD ─────────────
from dotenv import load_dotenv
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ───────────── CACHE CONFIG ─────────────
WEATHER_CACHE = "weather.json"
CRYPTO_CACHE  = "crypto.json"
STOCKS_CACHE  = "stocks.json"
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


# ───────────── UI ─────────────
def print_banner():
    print(g("PulseBoard Dashboard", C.CYAN))
    print(g(f"Time: {datetime.datetime.now()}", C.WHITE))


def section(title, emoji):
    print(g(f"\n┌─ {emoji} {title} ─" + "─" * 40, C.CYAN))


def section_end():
    print(g("└" + "─" * 50, C.CYAN))


def row(label, value):
    return f"  {label.ljust(20)} {value}"


# ───────────── WEATHER ─────────────
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
}


def fetch_weather():
    try:
        if os.path.exists("location.json"):
            with open("location.json") as f:
                loc = json.load(f)
        else:
            loc = requests.get("https://ipapi.co/json/", timeout=5).json()
            with open("location.json", "w") as f:
                json.dump(loc, f)

        lat = loc.get("latitude")
        lon = loc.get("longitude")
        city = loc.get("city", "Unknown")

        if not lat or not lon:
            lat, lon, city = 28.61, 77.23, "New Delhi"

        if is_cache_valid(WEATHER_CACHE):
            with open(WEATHER_CACHE) as f:
                data = json.load(f)
        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
            data = requests.get(url, timeout=5).json()

            if "current" in data:
                with open(WEATHER_CACHE, "w") as f:
                    json.dump(data, f)

        current = data.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        code = current.get("weather_code", -1)

        desc = WEATHER_CODES.get(code, "Unknown")

        return city, temp, desc

    except Exception:
        return "Unknown", "N/A", "API error"


# ───────────── CRYPTO ─────────────
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
            ids = ",".join(COINS.keys())
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
            data = requests.get(url, timeout=5).json()

            if any(k in data for k in COINS):
                with open(CRYPTO_CACHE, "w") as f:
                    json.dump(data, f)

        return [(symbol, data.get(coin, {}).get("usd", "N/A")) for coin, symbol in COINS.items()]

    except Exception:
        return [(symbol, "N/A") for symbol in COINS.values()]


# ───────────── STOCKS ─────────────
TICKERS = {
    "AAPL": "Apple",
    "GOOGL": "Google",
    "TSLA": "Tesla"
}


def fetch_stocks():
    try:
        if is_cache_valid(STOCKS_CACHE):
            with open(STOCKS_CACHE) as f:
                data = json.load(f)
        else:
            symbols = ",".join(TICKERS.keys())
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
            headers = {"User-Agent": "Mozilla/5.0"}

            data = requests.get(url, headers=headers, timeout=5).json()

            if data.get("quoteResponse", {}).get("result"):
                with open(STOCKS_CACHE, "w") as f:
                    json.dump(data, f)

        quotes = data.get("quoteResponse", {}).get("result", [])

        return [(q.get("symbol"), q.get("regularMarketPrice", "N/A")) for q in quotes]

    except Exception:
        return [(ticker, "N/A") for ticker in TICKERS.keys()]


# ───────────── NEWS ─────────────
DEMO_NEWS = [
    {"title": "AI is transforming the tech industry", "source": "TechCrunch"},
    {"title": "Stock markets hit new highs globally", "source": "Reuters"},
    {"title": "New breakthrough in renewable energy", "source": "BBC"},
]


def fetch_news():
    try:
        if not NEWS_API_KEY:
            return DEMO_NEWS

        url = "https://newsdata.io/api/1/news"

        params = {
            "apikey": NEWS_API_KEY,
            "language": "en",
            "category": "technology,business"
        }

        data = requests.get(url, params=params, timeout=5).json()

        articles = data.get("results", [])[:5]

        return [
            {
                "title": a.get("title", "No title"),
                "source": a.get("source_id", "Unknown")
            }
            for a in articles
        ]

    except Exception:
        return DEMO_NEWS


# ───────────── PRINT FUNCTIONS ─────────────
def print_weather():
    city, temp, desc = fetch_weather()
    section("Weather Report", "🌡")
    print(row("Location", city))
    print(row("Temperature", g(f"{temp}°C", C.GREEN)))
    print(row("Condition", desc))
    section_end()


def print_crypto():
    section("Crypto Market", "💎")
    for symbol, price in fetch_crypto():
        print(row(symbol, f"${price}"))
    section_end()


def print_stocks():
    section("Stock Market", "📈")
    for ticker, price in fetch_stocks():
        print(row(ticker, f"${price}"))
    section_end()


def print_news():
    section("Top News", "📰")
    for i, a in enumerate(fetch_news(), 1):
        print(f"  {i}. {a['title']}")
        print(f"     Source: {a['source']}\n")
    section_end()


# ───────────── MAIN ─────────────
if __name__ == "__main__":
    print_banner()
    print_weather()
    print_crypto()
    print_stocks()
    print_news()