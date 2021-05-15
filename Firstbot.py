from bs4.builder import HTML
from telegram.ext import *
import stockprice as stock_price
from telegram import ParseMode
import os
from dotenv import load_dotenv

load_dotenv()
print("Bot has started")


def start_command(update, context):

    update.message.reply_text(
        "Type a stock's NSE SYMBOL to get related information!")


def help_command(update, context):

    update.message.reply_text(
        "Enter a stock's NSE SYMBOL you want information about.")


def handle_message(update, context):
    text = str(update.message.text).lower()

    stock_price.nsestockprice(text, update, context)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    TOKEN = os.getenv('API_KEY')

    updater = Updater(f"{TOKEN}")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
