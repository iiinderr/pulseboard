# 📊 PulseBoard — Real-Time Intelligence Dashboard

PulseBoard is a real-time dashboard that aggregates data from multiple public APIs including weather, cryptocurrency, stock market, and news, and presents it in a structured and readable format.

---

## 👨‍💻 Author

**Inder Pal Singh**

---

## 🚀 Features

* 🌡 Weather data using Open-Meteo API
* 💎 Cryptocurrency prices using CoinGecko API
* 📈 Stock market data using Alpha Vantage API
* 📰 Latest news headlines using NewsData API
* ⚡ Real-time data fetching
* 🧠 Error handling and fallback mechanisms
* 💾 Local caching system to reduce API calls
* 🔐 Environment variable support for API keys

---

## 🛠 Tech Stack

* Python
* REST APIs
* JSON
* Git & GitHub

---

## 📁 Project Structure

pulseboard/
│
├── dashboard.py
├── dashboard.html (UI)
├── README.md
├── requirements.txt

---

## ⚙️ Setup Instructions

### 1. Clone the repository

git clone https://github.com/yourusername/pulseboard.git
cd pulseboard

---

### 2. Install dependencies

pip install -r requirements.txt

---

### 3. Add environment variables

Create a `.env` file and add:

NEWS_API_KEY=your_news_api_key
STOCK_API_KEY=your_stock_api_key

---

### 4. Run the project

python dashboard.py

---

## ⚠️ Notes

* Some APIs may fail due to rate limits
* Fallback data is used for stability
* Cache files are ignored using `.gitignore`

---

## 🎯 Future Improvements

* Add charts and graphs
* Improve UI
* Deploy backend

---

## 📌 Summary

PulseBoard demonstrates real-world API integration, error handling, and structured data processing in a clean and scalable way.
