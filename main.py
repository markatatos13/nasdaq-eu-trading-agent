import yfinance as yf
import time
import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

WATCHLIST = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "ASML", "SAP.DE"]

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def check_market():
    for ticker in WATCHLIST:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="5m")
        if len(data) > 0:
            latest = data["Close"].iloc[-1]
            prev = data["Close"].iloc[0]
            change = ((latest - prev) / prev) * 100

            if abs(change) > 2:
                subject = f"ALERT: {ticker} moved {round(change,2)}%"
                body = f"{ticker} moved {round(change,2)}% today.\nCurrent price: {round(latest,2)}"
                send_email(subject, body)

while True:
    check_market()
    time.sleep(900)
