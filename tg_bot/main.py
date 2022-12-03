import logging
import os

from telegram.ext import Application, CommandHandler

from main_menu import start
from list_stock import list_stock_handler, list_stock_back_handler, list_stock_previous_page_handler, \
    list_stocks_search_page_handler, list_stock_next_page_handler, list_stock_choice_page_handler
from prediction import prediction_handler, prediction_go_back_handler, prediction_date_x_handler, \
    prediction_date_y_handler, prediction_date_z_handler, predict_ticker_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def cb_pattern(str):
    return rf'^{str}.*$'


def main():
    app = Application.builder().token(os.environ['TELEGRAM_TOKEN']).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(list_stock_handler)
    app.add_handler(list_stock_back_handler)
    app.add_handler(list_stock_previous_page_handler)
    app.add_handler(list_stocks_search_page_handler)
    app.add_handler(list_stock_next_page_handler)
    app.add_handler(list_stock_choice_page_handler)

    app.add_handler(prediction_handler)
    app.add_handler(prediction_go_back_handler)
    app.add_handler(prediction_date_x_handler)
    app.add_handler(prediction_date_y_handler)
    app.add_handler(prediction_date_z_handler)

    app.add_handler(predict_ticker_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
