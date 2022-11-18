def cb_pattern(id: str, value: str = None):
    if value is None:
        return rf'^{id}.*$'
    else:
        return rf'^{id}.*{value}.*$'


MAIN_MENU_CALLBACK_DATA_PREFIX = 'main_menu_keyboard'
MAIN_MENU_ALL_STOCKS_PREFIX = 'all_stocks'
MAIN_MENU_SEARCH_STOCKS_PREFIX = 'search_stocks'
