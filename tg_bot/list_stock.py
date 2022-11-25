import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from common import *
from api import api_get_stocks
from main_menu import start_callback

logger = logging.getLogger(__name__)

page = 1

keyboard_catalog = [
    InlineKeyboardButton('↩', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_BACK_PREFIX}'),
    InlineKeyboardButton('◀', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_LAST_PAGE_PREFIX}'),
    InlineKeyboardButton('...', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_SEARCH_PAGE_PREFIX}'),
    InlineKeyboardButton('▶', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_NEXT_PAGE_PREFIX}')
]


async def list_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    keyboard = get_keyboard(page)
    await context.bot.send_message(update.effective_message.chat_id,
                                   f'{page} страница',
                                   reply_markup=keyboard)


def get_keyboard(page: int) -> InlineKeyboardMarkup:
    resp = api_get_stocks(page).json()
    keyboard = [[]]
    for i in resp["list"]:
        keyboard.append([InlineKeyboardButton(i['ticker'], callback_data='stock_' + i['ticker'])])
    keyboard.append(keyboard_catalog)
    return InlineKeyboardMarkup(keyboard)


async def last_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global page
    page -= 1
    if page < 1:
        await update.callback_query.answer('нельзя перейти на предыдущую страницу')
        page += 1
    keyboard = get_keyboard(page)
    await context.bot.send_message(update.effective_message.chat_id,
                                   f'{page} страница',
                                   reply_markup=keyboard)


async def next_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global page
    page += 1
    # нужно сделать проверку на переполнение
    keyboard = get_keyboard(page)
    await context.bot.send_message(update.effective_message.chat_id,
                                   f'{page} страница',
                                   reply_markup=keyboard)


list_stock_handler = CallbackQueryHandler(
    pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_ALL_STOCKS_PREFIX), callback=list_stock)

list_stock_back_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_BACK_PREFIX), callback=start_callback)

list_stock_last_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_LAST_PAGE_PREFIX), callback=last_page)

list_stock_next_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_NEXT_PAGE_PREFIX), callback=next_page)
