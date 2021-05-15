import pandas as pd
import nsepy as nse
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
from requests.models import Response, parse_header_links
import talib as ta

from datetime import date, datetime
import dateutil.relativedelta

from bs4 import BeautifulSoup
import json


def nsestockprice(symbol, update, context, series='EQ',):

    eq_quote_referer = "https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}&illiquid=0&smeFlag=0&itpFlag=0"
    if '&' in symbol:
        symbol = symbol.replace('&', '%26')

    try:

        nse.liveurls.quote_eq_url.session.headers.update(
            {'Referer': eq_quote_referer.format(symbol)})
        res = nse.liveurls.quote_eq_url(symbol, series)

        html_soup = BeautifulSoup(res.text, 'lxml')
        hresponseDiv = html_soup.find("div", {"id": "responseDiv"})

        d = json.loads(hresponseDiv.get_text())

        result = d['data'][0]

        if result['lastPrice'] >= result['previousClose']:
            Response = f"<b>--Stock Data--</b>\n <i>{result['companyName']} - {result['symbol']}</i>\n<b>PreviousClose : </b> ₹{result['previousClose']} \n<b>OpenPrice :</b> ₹{result['open']} \n<b>DayHigh :</b> ₹{result['dayHigh']}\n<b>DayLow :</b> ₹{result['dayLow']} \n<b>LastPrice :</b> ₹{result['lastPrice']}\n<b>Change :</b> ₹{result['change']} \n<b>Change % :</b> {result['pChange']} %  " + u"\u2B06"+" "+u"\u2705"
            update.message.reply_text(Response, parse_mode='HTML')
            stock_analysis(symbol, update, context)
        else:
            Response = f"<b>--Stock Data--</b>\n <i>{result['companyName']} - {result['symbol']}</i>\n<b>PreviousClose : </b> ₹{result['previousClose']} \n<b>OpenPrice :</b> ₹{result['open']} \n<b>DayHigh :</b> ₹{result['dayHigh']}\n<b>DayLow :</b> ₹{result['dayLow']} \n<b>LastPrice :</b> ₹{result['lastPrice']}\n<b>Change :</b> ₹{result['change']} \n<b>Change % :</b> {result['pChange']} %  " + u"\u2B07"+" "+u"\U0001F6D1"
            update.message.reply_text(Response, parse_mode='HTML')
            stock_analysis(symbol, update, context)
    except:

        update.message.reply_text(
            "Sorry,couldn't find the stock! Please check the spelling.", parse_mode='HTML')


def stock_analysis(symbol, update, context):

    today_date = datetime.now()
    month_ago_date = today_date + \
        dateutil.relativedelta.relativedelta(years=-1)
    df = pd.DataFrame(nse.get_history(
        symbol=symbol, start=month_ago_date, end=today_date))

    # ------------------------------ Simple moving average code----------------------------

    df['MA'] = ta.SMA(df['Close'], timeperiod=14)

    plt.figure(figsize=(20, 12))
    plt.plot(df.index, df['Close'], color='skyblue',
             linewidth=2, label='Close price')
    plt.plot(df.index, df['MA'], color='olive',
             linewidth=2, label='Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price in Rs.')
    plt.title('Simple Moving Average Graph')
    plt.legend()

    plt.savefig('squares.png')

    caption = "Simple Moving Average Graph"
    send_graph(update, context, caption)

    # -------------------------------  Relative Strength Index(RSI) -------------------------

    df['Relative'] = ta.RSI(df['Close'], 14)

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(20, 12))

    ax2.plot(df.index, df['Relative'],
             color='Blue', linewidth=2, label='RSI')
    ax2.axhline(y=30, color="green", linewidth=1, linestyle="--")
    ax2.axhline(y=50, color="grey", linewidth=1, linestyle="--")
    ax2.axhline(y=70, color="green", linewidth=1, linestyle="--")
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    ax2.legend()

    ax1.plot(df.index, df['Close'], color='Orange',
             linewidth=2, label='Close Price')
    ax1.set_ylabel('Close Price')
    ax1.set_title('Relative Strength Index(RSI)')
    ax1.legend()

    fig.savefig('squares.png')

    caption = "Relative Strength Index(RSI)"
    send_graph(update, context, caption)

    # ----------------------------- Bollinger bands -----------------------------------

    df['up_band'], df['mid_band'], df['low_band'] = ta.BBANDS(
        df['Close'], timeperiod=14)

    plt.figure(figsize=(20, 12))
    plt.plot(df.index, df['Close'], color='skyblue',
             linewidth=2, label='Close Price')
    plt.plot(df.index, df['mid_band'], color='Olive',
             linewidth=2, label='Mid-Band')
    plt.plot(df.index, df['up_band'], color='Yellow',
             linewidth=2, label='Up-Band')
    plt.plot(df.index, df['low_band'], color='Red',
             linewidth=2, label='low-Band')

    plt.xlabel('Date')
    plt.ylabel('Price in Rs.')
    plt.title('Bollinger Bands')
    plt.legend()

    plt.savefig('squares.png')

    caption = "Bollinger Bands"
    send_graph(update, context, caption)


def send_graph(update, context, caption):

    TOKEN = "1623484772:AAHhq7rZ7G0nj3-QGZLwZvP3f0_csu9W5qA"
    CHAT_ID = update.message.chat.id
    image_path = "squares.png"
    data = {"chat_id": CHAT_ID, "caption": caption}
    url = "https://api.telegram.org/bot%s/sendPhoto" % TOKEN
    with open(image_path, "rb") as image_file:
        ret = requests.post(url, data=data, files={
            "photo": image_file})

    os.remove("squares.png")
