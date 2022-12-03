import datetime
import logging
import re
import string

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler

from api import api_get_prediction
from common import *
from main_menu import start_callback

logger = logging.getLogger(__name__)

prediction_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('↩', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_GO_BACK_PREFIX}'),
        InlineKeyboardButton('15 минут', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_DATE_X_PREFIX}'),
        InlineKeyboardButton('2 часа', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_DATE_Y_PREFIX}'),
        InlineKeyboardButton('5 дней', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_DATE_Z_PREFIX}')
    ]
])


async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE, pred_timedelta: datetime.timedelta) -> None:
    ticker = context.user_data['ticker']
    date = str(datetime.datetime.utcnow() + pred_timedelta)

    try:
        req = api_get_prediction(ticker=ticker, date=date)
    except:
        await context.bot.send_message(update.effective_message.chat_id, 'Шаблон что-то пошло не так')
        return ConversationHandler.END

    if req.status_code != 200:
        await context.bot.send_message(update.effective_message.chat_id, 'Шаблон что-то пошло не так')
        return ConversationHandler.END

    await context.bot.send_message(update.effective_message.chat_id, 'Шаблон предсказания ' + req.text)


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pred_timedelta = parse_pred_timedelta(update.message.text)
    except:
        await context.bot.send_message(update.effective_message.chat_id,
                                       'Срок прогноза указан неверно. Например, для прогноза на 3 минуты введите "3 мин".')
        return

    return await predict(update, context, pred_timedelta)


def parse_pred_timedelta(text: str) -> datetime.timedelta:
    """
    Parse user input to get the prediction time inputted by user
    Input consists of 2 parts: number and unit (abbreviated or not, followed by an optional dot)
    :param text: user input
    :return: parsed datetime.timedelta
    """
    unit_lookup_table = {}
    for k, v in {
        ('дней', 'день', 'д'): datetime.timedelta(days=1),
        ('часов', 'часа', 'час', 'ч'): datetime.timedelta(seconds=60 * 60),
        ('минут', 'минуты', 'минута', 'м', 'мин'): datetime.timedelta(seconds=60),
        ('секунд', 'секунды', 'секунда', 'с', 'сек'): datetime.timedelta(seconds=1)
    }.items():
        for key in k:
            unit_lookup_table[key] = v

    number = int(re.findall('\d+', text.strip())[0])
    unit = unit_lookup_table[text.lstrip(string.digits).rstrip('.').strip()]

    return datetime.timedelta(seconds=number * unit.total_seconds())


async def entrypoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await context.bot.send_message(update.effective_message.chat_id, 'Выбор срока прогноза',
                                   reply_markup=prediction_keyboard)


async def prediction_go_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await start_callback(update, context)


async def prediction_x_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await predict(update, context, datetime.timedelta(seconds=60 * 15))


async def prediction_y_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await predict(update, context, datetime.timedelta(seconds=60 * 60 * 2))


async def prediction_z_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await predict(update, context, datetime.timedelta(days=5))


async def predict_ticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['ticker'] = update.callback_query.data.removeprefix(TICKER_NAME_PREFIX).lstrip()
    await entrypoint(update, context)


prediction_handler = CallbackQueryHandler(
    pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_SEARCH_STOCKS_PREFIX), callback=entrypoint)

prediction_go_back_handler = CallbackQueryHandler(
    pattern=cb_pattern(PREDICTION_CALLBACK_DATA_PREFIX, PREDICTION_GO_BACK_PREFIX),
    callback=prediction_go_back_callback)

prediction_date_x_handler = CallbackQueryHandler(
    pattern=cb_pattern(PREDICTION_CALLBACK_DATA_PREFIX, PREDICTION_DATE_X_PREFIX), callback=prediction_x_callback)

prediction_date_y_handler = CallbackQueryHandler(
    pattern=cb_pattern(PREDICTION_CALLBACK_DATA_PREFIX, PREDICTION_DATE_Y_PREFIX), callback=prediction_y_callback)

prediction_date_z_handler = CallbackQueryHandler(
    pattern=cb_pattern(PREDICTION_CALLBACK_DATA_PREFIX, PREDICTION_DATE_Z_PREFIX), callback=prediction_z_callback)

predict_ticker_handler = CallbackQueryHandler(pattern=cb_pattern(TICKER_NAME_PREFIX), callback=predict_ticker)
