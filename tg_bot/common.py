def cb_pattern(id: str, value: str = None):
    if value is None:
        return rf'^{id}.*$'
    else:
        return rf'^{id}.*{value}.*$'


MAIN_MENU_CALLBACK_DATA_PREFIX = 'main_menu_keyboard'
MAIN_MENU_ALL_STOCKS_PREFIX = 'all_stocks'
MAIN_MENU_SEARCH_STOCKS_PREFIX = 'search_stocks'

ALL_STOCKS_CALLBACK_DATA_PREFIX = 'all_stocks_keyboard'
ALL_STOCKS_GO_BACK_PREFIX = 'go_back'
ALL_STOCKS_GO_LAST_PAGE_PREFIX = 'go_last_page'
ALL_STOCKS_SEARCH_PAGE_PREFIX = 'search_page'
ALL_STOCKS_GO_NEXT_PAGE_PREFIX = 'go_next_page'

TICKER_NAME_PREFIX = 'stock'

PREDICTION_CALLBACK_DATA_PREFIX = 'prediction_keyboard'
PREDICTION_GO_BACK_PREFIX = 'go_back'
PREDICTION_DATE_X_PREFIX = 'date_x'
PREDICTION_DATE_Y_PREFIX = 'date_y'
PREDICTION_DATE_Z_PREFIX = 'date_z'
