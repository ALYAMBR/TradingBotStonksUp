import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters

from common import *
from api import api_get_stocks
from main_menu import start_callback

logger = logging.getLogger(__name__)

page = 1

wait_number_for_page = False


def get_keyboard(page: int) -> InlineKeyboardMarkup:
    resp = api_get_stocks(page).json()

    keyboard = [[]]

    for i in resp["list"]:
        keyboard.append([InlineKeyboardButton(i['ticker'], callback_data= f'{TICKER_NAME_PREFIX} {i["ticker"]}')])

    keyboard_catalog = [
        InlineKeyboardButton('↩', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_BACK_PREFIX}'),
        InlineKeyboardButton('◀', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_LAST_PAGE_PREFIX}'),
        InlineKeyboardButton(f'{page}/{resp["pageSize"]}', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_SEARCH_PAGE_PREFIX}'),
        InlineKeyboardButton('▶', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_NEXT_PAGE_PREFIX}')
    ]
    keyboard.append(keyboard_catalog)

    return InlineKeyboardMarkup(keyboard)


async def list_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    keyboard = get_keyboard(page)
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию, по которой хотите сделать прогноз',
                                   reply_markup=keyboard)


async def last_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global page
    page -= 1

    if page < 1:
        await update.callback_query.answer('Нельзя перейти на предыдущую страницу!')
        page += 1

    keyboard = get_keyboard(page)
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию, по которой хотите сделать прогноз',
                                   reply_markup=keyboard)


async def next_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global page
    resp = api_get_stocks(page).json()

    page += 1

    if page > resp["pageSize"]:
        await update.callback_query.answer('Нельзя перейти на следующую страницу!')
        page -= 1

    keyboard = get_keyboard(page)
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию, по которой хотите сделать прогноз',
                                   reply_markup=keyboard)


async def search_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()

    global wait_number_for_page
    wait_number_for_page = True

    await context.bot.send_message(update.effective_message.chat_id, 'Напишите страницу, на которую хотите перейти')


async def choice_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global page, wait_number_for_page

    if wait_number_for_page:
        try:
            page = int(update.message.text)
        except ValueError:
            context.bot.send_message(update.effective_message.chat_id, 'Введите целое положительное число')
            return

        wait_number_for_page = False

        keyboard = get_keyboard(page)
        await context.bot.send_message(update.effective_message.chat_id,
                                       'Выберите акцию, по которой хотите сделать прогноз',
                                       reply_markup=keyboard)


list_stock_handler = CallbackQueryHandler(
    pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_ALL_STOCKS_PREFIX), callback=list_stock)

list_stock_back_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_BACK_PREFIX), callback=start_callback)

list_stock_last_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_LAST_PAGE_PREFIX), callback=last_page)

list_stocks_search_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_SEARCH_PAGE_PREFIX), callback=search_page)

list_stock_next_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_NEXT_PAGE_PREFIX), callback=next_page)

list_stock_choice_page_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, choice_page)
