from datetime import *
import streamlit as st
import requests
from twilio.rest import Client

st.set_page_config(page_title="Trade Alert", page_icon=":red_triangle_pointed_up:")
st.subheader("Welcome to Stock trading alert app!")
STOCK = st.text_input(label="Enter stock code")
ph_no = st.text_input(label="Enter Your Ph.no for details else leave blank")

COMPANY_NAME = "Tesla Inc"
ALPHA_ADVANTAGE_API_KEY = "####"
NEWS_API_KEY = "####"
INTERVAL = 60
OUTPUT_SIZE = "compact"
TWILIO_ACC_SID = "####"
AUTH_TOKEN = "####"
client = Client(TWILIO_ACC_SID, AUTH_TOKEN)


def get_details(stock, interval, alpha_advantage_api_key):
    response_stock = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={interval}min&outputsize=compact&apikey={alpha_advantage_api_key}")
    data = response_stock.json()
    data_date = data["Time Series (60min)"]
    close_time = "16:00:00"
    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    day_before_yesterday_date = today_date - timedelta(days=2)
    i = 0
    holiday_print = False
    while i == 0:
        date_time_yesterday = f"{yesterday_date} {close_time}"
        date_time_day_before_yesterday = f"{day_before_yesterday_date} {close_time}"
        res = ""
        res2 = ""
        percentage = 0
        try:
            stock_data_1 = float(data_date[date_time_yesterday]["2. high"])
            res += f"date : {date_time_yesterday}, price: {stock_data_1}\n"
            i = 1
        except KeyError:
            if not holiday_print:
                res += "there was a holiday yesterday so here are the last known data:\n"
                holiday_print = True
            yesterday_date = yesterday_date - timedelta(days=1)
            day_before_yesterday_date = yesterday_date - timedelta(days=1)
        else:
            stock_data_2 = float(data_date[date_time_day_before_yesterday]["2. high"])
            res2 += f" date : {date_time_day_before_yesterday}, price : {stock_data_2}\n"
            percentage = ((stock_data_1-stock_data_2)/stock_data_2)*100
        return res, res2, percentage


bgcol1, bgcol2, bgcol3, bgcol4, bgcol5, bgcol6 = st.columns(6)
if bgcol3.button('Get Details'):
    result1, result2, percent = get_details(STOCK, INTERVAL, ALPHA_ADVANTAGE_API_KEY)
    col1, col2 = st.columns(2)
    col1.write(result1)
    col2.write(result2)
    col11, col12, col13 = st.columns(3)
    col12.write(f"Change in price: {percent}")
    col21, col22, col23 = st.columns(3)
    if percent > 0 or percent < 0:
        response_news = requests.get(url=f"https://newsapi.org/v2/everything?q=tesla&from=2023-06-15&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}")
        news = response_news.json()
        for j in range(3):
            title = news["articles"][j]["title"]
            desc = news["articles"][j]["description"]
            if percent > 0:
                message = client.messages \
                    .create(
                            body=f"TSLA: 🔺{percent}%\n Headline : {title}\n Brief : {desc}",
                            from_="####",
                            to=ph_no
                    )
            else:
                message = client.messages \
                    .create(
                            body=f"TSLA: 🔻{percent}%\n Headline : {title}\n Brief : {desc}",
                            from_="####",
                            to=ph_no
                        )

if bgcol4.button('Get News'):
    response_news = requests.get(url=f"https://newsapi.org/v2/everything?q=tesla&from=2023-06-15&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}")
    news = response_news.json()
    for j in range(3):
        title1 = f"{j+1}). {news['articles'][j]['title']}"
        st.write(title1)
        desc1 = news["articles"][j]["description"]
        st.write(desc1)



