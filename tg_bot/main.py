import logging
import os

from telegram.ext import Application, CommandHandler

from main_menu import start

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def cb_pattern(str):
    return rf'^{str}.*$'


def main():
    app = Application.builder().token(os.environ['TELEGRAM_TOKEN']).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
