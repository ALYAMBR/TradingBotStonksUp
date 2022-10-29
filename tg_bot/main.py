import logging
import os

from telegram.ext import Application, CommandHandler, MessageHandler, filters

import common
from common import start
from stock_list_handler import create_stock_list_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    app = Application.builder().token(os.environ['TELEGRAM_TOKEN']).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(create_stock_list_handler())
    app.add_handler(MessageHandler(filters=filters.ALL, callback=common.unrecognized_command_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
