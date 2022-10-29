import collections
import logging

import requests
import tabulate
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler, BaseHandler

import common
from common import menu_keyboard

logger = logging.getLogger(__name__)

ticker_keyboard = ReplyKeyboardMarkup([
    [
        KeyboardButton('Exit')
    ]
])

next_prev_keyboard = ReplyKeyboardMarkup([
    [
        KeyboardButton('Previous'),
        KeyboardButton('Next'),
        KeyboardButton('Choose ticker'),
        KeyboardButton('Exit')
    ]
])

# states
BEFORE_TICKER_ENTERED, AFTER_TICKER_ENTERED = range(2)


def create_stock_list_handler() -> BaseHandler:
    return ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Text(['List stocks']), callback=list_stocks_start)],
        states={
            BEFORE_TICKER_ENTERED: [
                MessageHandler(filters=filters.Text(['Exit']), callback=exit_to_main_menu),
                MessageHandler(filters=filters.ALL, callback=handle_entered_ticker)
            ],
            AFTER_TICKER_ENTERED: [
                MessageHandler(filters=filters.Text(['Previous']), callback=handle_prev_stocks_page),
                MessageHandler(filters=filters.Text(['Next']), callback=handle_next_stocks_page),
                MessageHandler(filters=filters.Text(['Choose ticker']), callback=choose_another_ticker),
                MessageHandler(filters=filters.Text(['Exit']), callback=exit_to_main_menu)
            ]
        },
        fallbacks=[MessageHandler(filters=filters.ALL, callback=common.unrecognized_command_handler)]
    )


async def exit_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Exiting to main menu', reply_markup=menu_keyboard)
    await common.start(update, context)
    return ConversationHandler.END


async def choose_another_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await list_stocks_start(update, context)


async def list_stocks_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Enter the stock ticker or a left part of it.', reply_markup=ticker_keyboard)
    return BEFORE_TICKER_ENTERED


async def handle_entered_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['query'] = update.message.text
    context.user_data['page_num'] = 1
    return await list_stocks(update, context)


async def handle_prev_stocks_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await list_stocks(update, context, prev_page_requested=True)


async def handle_next_stocks_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await list_stocks(update, context, next_page_requested=True)


async def list_stocks(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      prev_page_requested: bool = False,
                      next_page_requested: bool = False) -> int:
    req = requests.get(f'{common.ALGO_API_URL}/stocks', params={'query': context.user_data['query']})
    if req.status_code != 200:
        await update.message.reply_text(f'Something went wrong, try again. Status code: {req.status_code}')
    stock_list = req.json()

    if len(stock_list) == 0:
        await update.message.reply_text('Nothing was found. Try entering another ticker.', reply_markup=ticker_keyboard)
        return BEFORE_TICKER_ENTERED

    if prev_page_requested:
        if context.user_data['page_num'] > 1:
            context.user_data['page_num'] -= 1

    if next_page_requested:
        if context.user_data['page_num'] * 10 <= len(stock_list):
            context.user_data['page_num'] += 1

    logger.info(context.user_data['page_num'])

    stock_table = []

    for i in range((context.user_data['page_num'] - 1) * 10, min(context.user_data['page_num'] * 10, len(stock_list))):
        stock = stock_list[i]

        ordered_dict = collections.OrderedDict()
        ordered_dict['#'] = i + 1
        ordered_dict['Ticker'] = stock['ticker']
        ordered_dict['Exchange name'] = stock['exchangeName']
        ordered_dict['Stock name'] = stock['stockName']

        stock_table.append(ordered_dict)

    # <code> tags to achieve monospaced font
    await update.message.reply_html('<code>' +
                                    tabulate.tabulate(stock_table, headers='keys') +
                                    '</code>')

    if len(stock_list) > 10:
        await update.message.reply_text('There are more than 10 results. Use buttons to navigate the pages.', reply_markup=next_prev_keyboard)
        return AFTER_TICKER_ENTERED

    return await exit_to_main_menu(update, context)
