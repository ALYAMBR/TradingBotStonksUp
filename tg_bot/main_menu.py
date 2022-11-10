import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

CALLBACK_DATA_PREFIX = 'main_menu_keyboard'

ALL_STOCKS_PREFIX = 'main_menu_keyboard'
SEARCH_STOCKS_PREFIX = 'main_menu_keyboard'

main_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Все акции', callback_data=f'main_menu_keyboard {ALL_STOCKS_PREFIX}')],
    [InlineKeyboardButton('Поиск акции', callback_data=f'main_menu_keyboard {SEARCH_STOCKS_PREFIX}')]
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Приветственное сообщение', reply_markup=main_menu_keyboard)


async def main_menu_keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    if update.callback_query.data.find(ALL_STOCKS_PREFIX) != -1:
        pass
    elif update.callback_query.data.find(SEARCH_STOCKS_PREFIX) != -1:
        pass
