import requests
import datetime as dt
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
STOCK_API_URL = "https://www.alphavantage.co/query"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
dates = [(dt.datetime.now() - dt.timedelta(i)).strftime('%Y-%m-%d') for i in range(2, 4)]
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_URL = "http://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "from": dates[-1],
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}
PHONE_NUMBER = "+12513331821"
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")


print(ACCOUNT_SID)

stock_response = requests.get(STOCK_API_URL, params=STOCK_PARAMS)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stocks = [stock_data[item]["4. close"] for item in dates]
stock_percentage = 100 - (float(stocks[-1]) / float(stocks[0]) * 100)

news_response = requests.get(NEWS_API_URL, params=NEWS_PARAMS)
news_response.raise_for_status()
news_data = news_response.json()["articles"]
most_popular_news = [news_response.json()["articles"][i] for i in range(0, 3)]
formatted_news = []


def formatting_news():
    if stock_percentage > 0:
        sign = "🔺"
    else:
        sign = "🔻"

    for item in most_popular_news:
        new = f"{STOCK}: {sign}{round(stock_percentage, 2)}%\nHeadline: {item['title']}\nBrief: {item['description']}"
        formatted_news.append(new)


formatting_news()

client = Client(ACCOUNT_SID, AUTH_TOKEN)

for i in range(0, 3):
    message = client.messages \
                    .create(
                     body=formatted_news[i],
                     from_=PHONE_NUMBER,
                     to='PHONE NUMBER')

    print(message.status)
