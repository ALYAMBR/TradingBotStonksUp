import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from common import *
from api import api_get_stocks

logger = logging.getLogger(__name__)

PAGE = 1

keyboard_catalog = [
    InlineKeyboardButton('↩', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_BACK_PREFIX}'),
    InlineKeyboardButton('◀', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_LAST_PAGE_PREFIX}'),
    InlineKeyboardButton('...', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_SEARCH_PAGE_PREFIX}'),
    InlineKeyboardButton('▶', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_NEXT_PAGE_PREFIX}')
]


async def list_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    keyboard = get_keyboard(PAGE)
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию',
                                   reply_markup=keyboard)


def get_keyboard(page: int) -> InlineKeyboardMarkup:
    resp = api_get_stocks(page).json()
    keyboard = [[]]
    for i in resp["list"]:
        keyboard.append([InlineKeyboardButton(i['ticker'], callback_data='stock_' + i['ticker'])])
    keyboard.append(keyboard_catalog)
    return InlineKeyboardMarkup(keyboard)


list_stock_handler = CallbackQueryHandler(
    pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_ALL_STOCKS_PREFIX), callback=list_stock)
