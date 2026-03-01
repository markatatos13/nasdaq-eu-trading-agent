import yfinance as yf
import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

WATCHLIST = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "ASML", "SAP.DE"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_market():
    for ticker in WATCHLIST:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="5m")
        if len(data) > 0:
            latest = data["Close"].iloc[-1]
            prev = data["Close"].iloc[0]
            change = ((latest - prev) / prev) * 100
            
            if abs(change) > 2:
                signal = f"{ticker} moved {round(change,2)}% today. Current price: {round(latest,2)}"
                send_telegram(signal)

while True:
    check_market()
    time.sleep(900)
