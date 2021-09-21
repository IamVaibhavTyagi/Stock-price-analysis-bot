# Stock Price Analysis Bot

Developed a Bot to give Live price of a National Stock Exchange (NSE) stock upon messaging the Stock Symbol

Created a technical analysis module which provided the market performance of a stock using the data of last 
6 months

## Technology used:
* Python
* Telegram API
* NSEpy library

## About The Project:

* The Bot is built using Telegram API which will act as a front-end for the user to interact.
* To get LIVE price of a stock the user will have to enter the SYMBOL of the stock.
* Using the SYMBOL we can scrap the live data from NSE official website using Python.
* Data analysis is performed using Pandas,Numpy and Matplotlib. I have used NSEpy library to retreive data.

### Demonstration:

* Entering the NSE SYMBOL of a stock and receiving the Live Price update and Technical analysis graphs.

![stock_price1_Trim_SparkVideo (1)](https://user-images.githubusercontent.com/39727591/134106935-68bb0ddd-9dd4-4238-aba4-df423ef0e015.gif)

* If an incorrect stock symbol is entered, then an error as below will be given.

<img src="https://user-images.githubusercontent.com/39727591/134107185-04407ded-0970-40cf-99f9-1e3105a1d047.jpg" width="30%" height="30%">



