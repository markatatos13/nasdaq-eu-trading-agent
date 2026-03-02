print("BOT STARTED")

import yfinance as yf
import time
import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

WATCHLIST = ["AAPL"]

def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("EMAIL SENT")
    except Exception as e:
        print("EMAIL ERROR:", e)

def check_market():
    print("CHECKING MARKET")
    for ticker in WATCHLIST:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        print(data.tail())

while True:
    check_market()
    time.sleep(60)
