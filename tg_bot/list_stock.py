import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters

from api import api_get_stocks
from common import *
from main_menu import start_callback

logger = logging.getLogger(__name__)


def get_keyboard(page: int, prefix: str) -> InlineKeyboardMarkup:
    resp = api_get_stocks(page, prefix).json()

    keyboard = [[]]
    for i in resp["list"]:
        keyboard.append([InlineKeyboardButton(i['ticker'], callback_data= f'{TICKER_NAME_PREFIX} {i["ticker"]}')])

    keyboard_catalog = [
        InlineKeyboardButton('↩', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_BACK_PREFIX}'),
        InlineKeyboardButton('◀', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_PREVIOUS_PAGE_PREFIX}'),
        InlineKeyboardButton(f'{page}/{resp["totalCount"]}', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_SEARCH_PAGE_PREFIX}'),
        InlineKeyboardButton('▶', callback_data=f'{ALL_STOCKS_CALLBACK_DATA_PREFIX} {ALL_STOCKS_GO_NEXT_PAGE_PREFIX}')
    ]
    keyboard.append(keyboard_catalog)

    return InlineKeyboardMarkup(keyboard)


async def list_stock(update: Update, context: ContextTypes.DEFAULT_TYPE, should_reset=True) -> None:
    if should_reset:
        context.user_data["page"] = 1
        context.user_data["wait_number_for_page"] = False
        context.user_data["ticker_name"] = None

    await update.callback_query.answer()

    keyboard = get_keyboard(context.user_data["page"], context.user_data["ticker_name"])
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию, по которой вы хотите сделать прогноз',
                                   reply_markup=keyboard)


async def search_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["page"] = 1
    context.user_data["wait_number_for_page"] = False
    context.user_data["wait_ticker_name"] = True
    context.user_data["ticker_name"] = None

    await update.callback_query.answer()

    await context.bot.send_message(update.effective_message.chat_id, 'Введите наименование акции')


async def previous_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    page = context.user_data["page"]

    page -= 1

    if page < 1:
        await update.callback_query.answer('Нельзя перейти на предыдущую страницу!')
        page += 1

    context.user_data["page"] = page

    keyboard = get_keyboard(page, context.user_data["ticker_name"])
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию, по которой вы хотите сделать прогноз',
                                   reply_markup=keyboard)


async def next_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    page = context.user_data["page"]

    page += 1

    resp = api_get_stocks(1, context.user_data["ticker_name"]).json()
    if page > resp["totalCount"]:
        await update.callback_query.answer('Нельзя перейти на следующую страницу!')
        page -= 1

    context.user_data["page"] = page

    keyboard = get_keyboard(page, context.user_data["ticker_name"])
    await context.bot.send_message(update.effective_message.chat_id,
                                   'Выберите акцию, по которой вы хотите сделать прогноз',
                                   reply_markup=keyboard)


async def search_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()

    context.user_data["wait_number_for_page"] = True

    await context.bot.send_message(update.effective_message.chat_id, 'Напишите страницу, на которую вы хотите перейти')


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get("wait_number_for_page"):
        try:
            page = int(update.message.text)
        except ValueError:
            await context.bot.send_message(update.effective_message.chat_id, 'Введите целое положительное число')
            return

        resp = api_get_stocks(1, context.user_data["ticker_name"]).json()
        if page > resp["totalCount"] or page < 1:
            await context.bot.send_message(update.effective_message.chat_id,
                                           f'Введите число в промежутке от 1 до {resp["totalCount"]}')
            return

        context.user_data["page"] = page
        context.user_data["wait_number_for_page"] = False

        keyboard = get_keyboard(page, context.user_data["ticker_name"])
        await context.bot.send_message(update.effective_message.chat_id,
                                       'Выберите акцию, по которой вы хотите сделать прогноз',
                                       reply_markup=keyboard)

    if context.user_data.get("wait_ticker_name"):
        context.user_data["ticker_name"] = update.message.text

        context.user_data["wait_ticker_name"] = False

        keyboard = get_keyboard(1, context.user_data["ticker_name"])
        await context.bot.send_message(update.effective_message.chat_id,
                                       'Выберите акцию, по которой вы хотите сделать прогноз',
                                       reply_markup=keyboard)


list_stock_handler = CallbackQueryHandler(
    pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_ALL_STOCKS_PREFIX), callback=list_stock)

search_stock_handler = CallbackQueryHandler(
    pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_SEARCH_STOCKS_PREFIX), callback=search_stock)

list_stock_back_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_BACK_PREFIX), callback=start_callback)

list_stock_previous_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_PREVIOUS_PAGE_PREFIX), callback=previous_page)

list_stock_search_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_SEARCH_PAGE_PREFIX), callback=search_page)

list_stock_next_page_handler = CallbackQueryHandler(
    pattern=cb_pattern(ALL_STOCKS_CALLBACK_DATA_PREFIX, ALL_STOCKS_GO_NEXT_PAGE_PREFIX), callback=next_page)

list_stock_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, message)
