from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes

ALGO_API_URL = 'http://localhost:8080'

menu_keyboard = ReplyKeyboardMarkup([
    [
        KeyboardButton('List stocks')
    ]
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Use this to invoke the main menu anywhere
    """
    await update.message.reply_text('Please, choose an option', reply_markup=menu_keyboard)


async def unrecognized_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Use this when any unrecognized command happens
    """
    await update.message.reply_text('Unrecognized command.')
