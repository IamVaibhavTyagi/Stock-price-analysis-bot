from bs4.builder import HTML
from telegram.ext import *
# import telegram as tele
import stockprice as stock_price
from telegram import ParseMode
import os
from os import environ

print("Bot has started")
PORT = int(os.environ.get('PORT', '8443'))


def start_command(update, context):
    # print(update)
    # print("inside start")

    update.message.reply_text(
        "Type a stock's NSE SYMBOL to get related information!")


def help_command(update, context):
    # print("inside help")

    update.message.reply_text(
        "Enter a stock's NSE SYMBOL you want information about.")


def handle_message(update, context):
    text = str(update.message.text).lower()

    stock_price.nsestockprice(text, update, context)

    # responses = stock_price.nsestockprice(text)

    # print(responses)
    # update.message.reply_text(responses, parse_mode='HTML')
    # if stock_price.flag == 1:
    # stock_price.stock_analysis(text, update, context)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(environ['API_KEY'])

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=environ['API_KEY']), webhook_url = f"https://stock-price-analysis-bot.herokuapp.com/{environ['API_KEY']}"
    # updater.bot.setWebhook(
    #    'https://stock-price-analysis-bot.herokuapp.com/'+environ['API_KEY'])

    updater.idle()


main()
