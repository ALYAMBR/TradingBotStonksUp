import datetime
import logging
import re
import string

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

from api import api_get_prediction
from common import *

logger = logging.getLogger(__name__)

prediction_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('↩', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_GO_BACK_PREFIX}'),
        InlineKeyboardButton('x', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_DATE_X_PREFIX}'),
        InlineKeyboardButton('y', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_DATE_Y_PREFIX}'),
        InlineKeyboardButton('z', callback_data=f'{PREDICTION_CALLBACK_DATA_PREFIX} {PREDICTION_DATE_Z_PREFIX}')
     ]
])

# states
WAITING_FOR_INPUT = 1


async def entrypoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await context.bot.send_message(update.effective_message.chat_id, 'Выбор срока прогноза', reply_markup=prediction_keyboard)
    return WAITING_FOR_INPUT


async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass  # call handler that we are supposed to call
    return ConversationHandler.END


async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE, pred_timedelta: datetime.timedelta) -> int:
    ticker = '123'  # context.user_data['ticker']
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

    return ConversationHandler.END


async def prediction_keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    if update.callback_query.data.find(PREDICTION_GO_BACK_PREFIX) != -1:
        await go_back(update, context)
    elif update.callback_query.data.find(PREDICTION_DATE_X_PREFIX) != -1:
        await predict(update, context, datetime.timedelta(seconds=60 * 15))
    elif update.callback_query.data.find(PREDICTION_DATE_Y_PREFIX) != -1:
        await predict(update, context, datetime.timedelta(seconds=60 * 60 * 2))
    elif update.callback_query.data.find(PREDICTION_DATE_Z_PREFIX) != -1:
        await predict(update, context, datetime.timedelta(days=5))
    return await go_back(update, context)


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        pred_timedelta = parse_pred_timedelta(update.message.text)
    except:
        await context.bot.send_message(update.effective_message.chat_id, 'Срок прогноза указан неверно. Например, для прогноза на 3 минуты введите "3 мин".')
        return WAITING_FOR_INPUT

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
        ('часов', 'часа', 'час', 'ч'): datetime.timedelta(seconds=60*60),
        ('минут', 'минуты', 'минута', 'м', 'мин'): datetime.timedelta(seconds=60),
        ('секунд', 'секунды', 'секунда', 'с', 'сек'): datetime.timedelta(seconds=1)
    }.items():
        for key in k:
            unit_lookup_table[key] = v

    number = int(re.findall('\d+', text.strip())[0])
    unit = unit_lookup_table[text.lstrip(string.digits).rstrip('.').strip()]

    return datetime.timedelta(seconds=number * unit.total_seconds())


prediction_handler = ConversationHandler(entry_points=[CallbackQueryHandler(pattern=cb_pattern(MAIN_MENU_CALLBACK_DATA_PREFIX, MAIN_MENU_SEARCH_STOCKS_PREFIX), callback=entrypoint)],
                                         states={
                                             WAITING_FOR_INPUT: [
                                                 CallbackQueryHandler(pattern=cb_pattern(PREDICTION_CALLBACK_DATA_PREFIX), callback=prediction_keyboard_callback),
                                                 MessageHandler(filters=filters.TEXT, callback=handle_input)
                                             ]
                                         },
                                         fallbacks=[])
