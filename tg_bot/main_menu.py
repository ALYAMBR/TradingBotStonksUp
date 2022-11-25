import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from common import *

logger = logging.getLogger(__name__)

main_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Все акции', callback_data=f'{MAIN_MENU_CALLBACK_DATA_PREFIX} {MAIN_MENU_ALL_STOCKS_PREFIX}')],
    [InlineKeyboardButton('Поиск акции', callback_data=f'{MAIN_MENU_CALLBACK_DATA_PREFIX} {MAIN_MENU_SEARCH_STOCKS_PREFIX}')]
])


async def start(update: Update, _) -> None:
    await update.message.reply_text('Приветственное сообщение', reply_markup=main_menu_keyboard)


async def start_callback(update: Update, _) -> None:
    await update.callback_query.answer()
    await update.callback_query.message.reply_text('Приветственное сообщение', reply_markup=main_menu_keyboard)

