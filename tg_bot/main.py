import logging
import os

from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from main_menu import start, main_menu_keyboard_callback
import main_menu

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def cb_pattern(str):
    return rf'^{str}.*$'


def main():
    app = Application.builder().token(os.environ['TELEGRAM_TOKEN']).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(pattern=cb_pattern(main_menu.CALLBACK_DATA_PREFIX), callback=main_menu_keyboard_callback))
    app.run_polling()


if __name__ == "__main__":
    main()
