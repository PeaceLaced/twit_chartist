"""
- trade_handler API. Anything involved with trading, picking symbols, tda, etc.

"""
import sys
import pytz
import httpx
from tqdm import tqdm
from enum import Enum
from time import sleep
from copy import deepcopy
from datetime import datetime as dt

from tda.utils import Utils
from tda.client.synchronous import Client as TDAClientClass
from tda.orders.equities import equity_buy_market, equity_sell_market

from twit.twit_api.api_database_handler import mongo_data_handler
from twit.twit_api.api_progress_handler import Progress as progress
from twit.twit_api.config.config_td_ameritrade import TOKEN_PATH, API_KEY_TDA, ACCOUNT_ID

from decimal import Decimal, setcontext, BasicContext
# set decimal context, precision = 9, rounding = round half even
setcontext(BasicContext)

# trade_author

MIN_PRICE = 2.00
MAX_PRICE = 5.00
MIN_NET_CHANGE = 0.10
MIN_MARKETCAP = 50000000 # 50 Million
MIN_VOLUME = 500000 # 500 Thousand

def trade_handler(tda_client, trade_author, trade_symbol, hold_seconds):
    ''' manage trades here '''
    
    # how about function call to actually trade
    STOP_TRYING_TO_BUY = 10
    SHARE_QUANTITY = 1

    progress.w(f'WE_WILL_TRADE_({trade_symbol})')
    order_response = order_place_equity_market(tda_client, OrderType.BUY, trade_symbol, SHARE_QUANTITY)
    order_json = order_get_details(tda_client, order_response, wait_for_fill=STOP_TRYING_TO_BUY, order_report=True)
    data_syndicate(order_json, report_data=True)
    
    progress.w(f'SLEEPING_(hold_position_({hold_seconds}_seconds))')
    sleep(int(hold_seconds))
    
    order_response = order_place_equity_market(tda_client, OrderType.SELL, trade_symbol, SHARE_QUANTITY)
    order_json = order_get_details(tda_client, order_response, wait_for_fill=True, order_report=True)
    profit_data = data_syndicate(order_json, report_data=True, report_profit=True, return_profit=True)
    
    mod_value = mongo_data_handler(None, profit_data[0][1], operation='MOD_TOTAL')
    
    ###########
    ##### TODO: using mod total/total wit, return new wit value after trade is compelte
    ###########
    
    return mod_value

class SymbolSelectTypeException(TypeError):
    '''Raised when there is a type error in the symbol select API.'''
    
class SymbolSelectValueException(ValueError):
    '''Raised when there is a value error in the symbol select API.'''
    
class TradeHandlerTypeException(TypeError):
    '''Raised when there is a type error'''
    
class TradeHandlerValueException(ValueError):
    '''Raised when there is a value error'''
    
class DataSyndicateTypeException(TypeError):
    '''Raised when there is a type error in :meth:`data_syndicate`'''
    
class OrderType(Enum):
    '''Used when placing orders and in other logic for standardization.'''
    BUY = 'BUY'
    SELL = 'SELL'
    PROFIT = 'PROFIT'

def throttle(sleep_time):
    '''Used to throttle certain endpoint calls
    :param sleep_time: an int
    :return: sleep yo
    '''
    if not isinstance(sleep_time, float):
        raise SymbolSelectTypeException('sleep_time must be an float')
    return sleep(sleep_time)
    
def get_client_session():
    '''Returns a tda-api asyncio client session for use throughout the program.
    TDA-API DOCS:     https://tda-api.readthedocs.io/en/latest/
    TDA-API SOURCE:   https://github.com/alexgolec/tda-api
    TDA-API DISCORD:  https://discord.gg/M3vjtHj
    :return: tda-api client object
    '''
    try:
        from tda.auth import client_from_token_file
        tda_client = client_from_token_file(TOKEN_PATH, API_KEY_TDA)
    except FileNotFoundError:
        from selenium import webdriver
        from tda.auth import client_from_login_flow
        from twit.twit_api.config.config_td_ameritrade import REDIRECT_URI
        with webdriver.Firefox() as DRIVER:
            tda_client = client_from_login_flow(
                DRIVER, API_KEY_TDA, REDIRECT_URI, TOKEN_PATH)
    except Exception as err:
        progress.e(f'Unexpected {err=}, {type(err)=} (catch_all_tda-api)')
        progress.w('EXITING')
        sys.exit()
    progress.s('TDA_TOKEN_(found)')
    
    return tda_client
    
def get_symbols(tda_client):
    '''
    generates a symbol list for trading, :meth:`get_nasdaq_screener`  is required
                                         :meth:`final_symbol_filter` is required for 
                                                                     a symbol only list
    :param tda_client: The client object created by tda-api.
                       Required, even if not using :meth:`filter_by_top_volume`
                       
    return: write the symbols to the database
    
    
    NOTICE: :meth:`filter_by_volume` should be called after all other methods
                                     but before :meth:`final_symbol_filter` 
                                     because it connects to TDA at 0.5 seconds
                                     per symbol. Less symbols = Less time.      
            :meth:`filter_by_price` set MIN_PRICE, MAX_PRICE
            :met:`filter_by_netchange` set MIN_NET_CHANGE
                                       POSITIVE indicates a positive net change
                                       NEGATIVE is possible, use with caution
            :meth:`filter_by_top_marketcap` set MIN_MARKETCAP
            :meth:`filter_by_top_volume` set MIN_VOLUME
            :var:`ADD_AVOID takes a tuple of lists
                  first list adds to tradable
                  second list makes sure those symbols are removed from tradable
    '''
    if not isinstance(tda_client, TDAClientClass):
        raise SymbolSelectTypeException('tda client object required')
    
    symbol_list = get_nasdaq_screener(full_clean=True)
    
    symbol_list = filter_by_price(symbol_list, MIN_PRICE, MAX_PRICE)
    
    symbol_list = filter_by_netchange(symbol_list, 'POSITIVE', MIN_NET_CHANGE)
    
    symbol_list = filter_by_top_marketcap(symbol_list, MIN_MARKETCAP)
    
    symbol_list = filter_by_top_volume(tda_client, symbol_list, MIN_VOLUME)
    
    ADD_AVOID = ([], ['ARDS', 'TUYA', 'ARMP'])
    
    symbol_list = final_symbol_filter(symbol_list, add_avoid=ADD_AVOID, strip_data=True)
    
    return mongo_data_handler(None, symbol_list, operation='SYMBOLS')

def get_nasdaq_screener(full_clean=True, dump_raw=False):
    '''connect to and download the nasdaq screener from api.nasdaq.com/api/screener/stocks
    
    :param full_clean: default is True, removes (NA, slash, carrot, spaces)
    :param dump_raw: default is False, creates an aware datetime tupled with the data
                     - NOT IMPLEMENTED YET (1Jan2022)
                     
    :return: list of symbol data
    '''
##### TODO: list comprehension the appends<>    
    initial_symbol_list = []
    if not isinstance(dump_raw, bool):
        raise SymbolSelectTypeException('dump_raw must be a bool')
    
    if not isinstance(full_clean, bool):
        raise SymbolSelectTypeException('full_clean must be a bool')

    nasdaq_screener_json = httpx.get('https://api.nasdaq.com/api/screener/stocks', 
                                   params={'tableonly' : 'true', 'limit' : 15000,'exchange' : 'all'}, 
                                   headers={"User-Agent": "Mozilla/5.0 (x11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"}
                                   ).json()
    
    asof_trimmed = nasdaq_screener_json['data']['asof'].replace('Last price as of','').replace(',','').split()
    
    new_asof = dt.strptime(asof_trimmed[1] + ' ' + asof_trimmed[0] + ' ' + asof_trimmed[2], "%d %b %Y")
    nasdaq_screener_aware = pytz.timezone('US/Eastern').localize(dt(new_asof.year, new_asof.month, new_asof.day, 20))
    
##### TODO: figure out what to do with this, file, db, etc. <>    
    if dump_raw:
        pass
        #nasdaq_screener_tuple = (nasdaq_screener_json, nasdaq_screener_aware)

    for symbol_data in tqdm(nasdaq_screener_json['data']['table']['rows'], desc='Cleaning Data'): #this is looping through 0, 1, 2, 3...
        if not full_clean:
            initial_symbol_list.append({'symbol':symbol_data['symbol'], 'last_price':symbol_data['lastsale'].replace('$',''), 'net_change':symbol_data['netchange'], 'market_cap':symbol_data['marketCap']})
        else:
            if symbol_data['marketCap'] != 'NA':
                if symbol_data['symbol'].find('^') == -1 and symbol_data['symbol'].find('/') == -1 and symbol_data['symbol'].find(' ') == -1:
                    initial_symbol_list.append({'aware_datetime':nasdaq_screener_aware,
                                                'symbol':symbol_data['symbol'],
                                                'last_price':symbol_data['lastsale'].replace('$',''),
                                                'net_change':symbol_data['netchange'].replace('UNCH', '0.00'),
                                                'market_cap':symbol_data['marketCap'].replace(',', '')})

    return initial_symbol_list

def filter_by_price(symbol_list, price_low, price_high):
    '''return a list of symbol data between price_low and price_high
    
    :param symbol_list: symbol list with attached data
    :param price_low: select stocks greater than this price
    :param price_high: select stocks lower than this price
    
    :return: list of symbol data
    '''
    if not isinstance(symbol_list, list):
        raise SymbolSelectTypeException('symbol_list must be a list')
        
    if not isinstance(price_low, float):
        raise SymbolSelectTypeException('price_low must be a float')
        
    if not isinstance(price_high, float):
        raise SymbolSelectTypeException('price_high must be a float')
        
    filtered_price_symbols = []
    for symbol_data in tqdm(symbol_list, desc='Applying Price Filter'):
        if float(symbol_data['last_price']) > price_low:
            if float(symbol_data['last_price']) < price_high:
                filtered_price_symbols.append(symbol_data)
    symbol_list.clear()
    
    return filtered_price_symbols

def filter_by_netchange(symbol_list, net_direction, net_thresh):
    '''return a list of symbol data within net_change params
    
    :param symbol_list: symbol list with attached data
    :param net_direction: net change in the positve or negative direction
    :param net_thresh: the amount of change
                       POSITIVE net_direction is above net_thresh
                       NEGATIVE net_direction is below negative net_thresh
    
    :return: list of symbol data
    '''
    
    if not isinstance(symbol_list, list):
        raise SymbolSelectTypeException('symbol_list must be a list')
        
    if not isinstance(net_direction, str):
        raise SymbolSelectTypeException('net_direction must be a string')
        
    if not isinstance(net_thresh, float):
        raise SymbolSelectTypeException('net_thresh must be a float')
        
    if net_direction not in {'POSITIVE', 'NEGATIVE'}:
        raise SymbolSelectValueException('net_direction must be either POSITIVE or NEGATIVE')
        
    filtered_netchange_symbols = []
    for symbol_data in tqdm(symbol_list, desc='Applying Netchange Filter'):
        if net_direction in {'POSITIVE'}:
            if float(symbol_data['net_change']) >= net_thresh:
                filtered_netchange_symbols.append(symbol_data)
 
        if net_direction in {'NEGATIVE'}:
            if float(symbol_data['net_change']) <= (0 - net_thresh):
                filtered_netchange_symbols.append(symbol_data)

    return filtered_netchange_symbols

def filter_by_top_marketcap(symbol_list, cap_thresh):
    '''return a list of symbol data within market_cap params
    
    :param symbol_list: symbol list with attached data
    :param cap_thresh: market cap will be greater than this number
    
    :return: list of symbol data
    '''
    if not isinstance(symbol_list, list):
        raise SymbolSelectTypeException('symbol_list must be a list')
        
    if not isinstance(cap_thresh, int):
        raise SymbolSelectTypeException('cap_thresh must be an int')
         
    filtered_marketcap_symbols = []
    for symbol_data in tqdm(symbol_list, desc='Applying Marketcap Filter'):
        if int(symbol_data['market_cap']) > cap_thresh:
            filtered_marketcap_symbols.append(symbol_data)
    
    return filtered_marketcap_symbols

def filter_by_top_volume(tda_client, symbol_list, volume_thresh):
    '''return a list of symbol data within volume params
    
    :param tda_client: The client object created by tda-api.
    :param symbol_list: symbol list with attached data
    :param volume_thresh: volume will be greater than this number
    
    :return: list of symbol data
    '''
    if not isinstance(tda_client, TDAClientClass):
        raise SymbolSelectTypeException('tda client object is required')
    
    if not isinstance(symbol_list, list):
        raise SymbolSelectTypeException('symbol_list must be a list')
        
    if not isinstance(volume_thresh, int):
        raise SymbolSelectTypeException('volume_thresh must be an int')
    
    if len(symbol_list) > 120:
        report_time = len(symbol_list)*0.7
    else:
        report_time = 10
        
    progress.slowly(f'Volume filter for {len(symbol_list)} stocks will take ~{report_time} seconds to process.')
    progress.slowly('YES to continue, NO to exit, SKIP to bypass.')
    
    continue_input = input().upper()
    if continue_input in {'YES'}:
        filtered_volume_symbols = []
        for symbol_data in tqdm(symbol_list, desc='Getting Volume Data'):
            r = tda_client.get_price_history(symbol_data['symbol'],
                                             period_type=tda_client.PriceHistory.PeriodType.MONTH,
                                             period=tda_client.PriceHistory.Period.ONE_MONTH,
                                             frequency_type=tda_client.PriceHistory.FrequencyType.DAILY,
                                             frequency=tda_client.PriceHistory.Frequency.DAILY,
                                             need_extended_hours_data=False)
            
            if isinstance(r, httpx.Response):
                if r.status_code in {200, 201, 202}:
                    try:
                        symbol_volume = r.json()['candles'].pop()['volume']
                        if symbol_volume > volume_thresh:
                            filtered_volume_symbols.append({'aware_datetime':symbol_data['aware_datetime'],
                                                            'symbol':symbol_data['symbol'], 
                                                            'last_price':symbol_data['last_price'],
                                                            'net_change':symbol_data['net_change'],
                                                            'market_cap':symbol_data['market_cap'],
                                                            'volume':symbol_volume})
                    except Exception as err:
######################### TODO: should we remove the symbol if it fails volume data check <>
                        pass

            if len(symbol_list) > 120:
                throttle(0.5)
            
        return filtered_volume_symbols
    
    if continue_input in {'SKIP'}:
        return symbol_list
    
    if continue_input in {'NO'}:
        progress.w('EXITING')
        sys.exit()

def final_symbol_filter(symbol_list, add_avoid=False, strip_data=True):
    '''returns the final symbol list based on params
    
    :param symbol_list: symbol list with attached data
    :param manual_add: takes a list and adds the symbols 
                       default is False, True only works if strip_data=True
    :param manual_avoid: takes a list and removes the symbols 
                         default is False, True only works if strip_data=True
    :param strip_data: remove all data and return ONLY the symbol list
    
    :return: symbol list with or without data attached
    '''
        
    if not isinstance(symbol_list, list):
        raise SymbolSelectTypeException('symbol_count must be a list')
        
    if not isinstance(strip_data, bool):
        raise SymbolSelectTypeException('strip_data must be a bool')
        
    if not isinstance(add_avoid, bool):
        if not isinstance(add_avoid, tuple):
            raise SymbolSelectTypeException('add_avoid must be a bool or tuple')
    
    if not isinstance(add_avoid[0], list):
        raise SymbolSelectTypeException('add_avoid[0] must be a list')
        
    if not isinstance(add_avoid[1], list):
        raise SymbolSelectTypeException('add_avoid[1] must be a list')
    
    final_symbol_list = []

    if strip_data:
        for symbol_data in symbol_list:
            final_symbol_list.append(symbol_data['symbol'])
            
        if add_avoid[0]:
            for symbol_to_add in add_avoid[0]:
                if symbol_to_add in final_symbol_list:
                    final_symbol_list.append(symbol_to_add)
        
        if add_avoid[1]:
            for symbol_to_avoid in add_avoid[1]:
                if symbol_to_avoid in final_symbol_list:
                    final_symbol_list.remove(symbol_to_avoid)
                    
    if not strip_data:
        final_symbol_list = symbol_list
        
    return final_symbol_list
    
def _order_report(order_data, order_type=False, order_symbol=False, order_shares=False):
    '''Used by methods that set order_report=True

    :param order_data: can be order_json (`order_get_details`)
                       or an order_response (`order_place_equity_market`)
    :param order_type: default is False, REQUIRED when order_data is httpx.Response
    :param order_symbol: default is False, REQUIRED when order_data is httpx.Response
    :param order_shares: default is False, REQUIRED when order_data is httpx.Response
    '''
    if not isinstance(order_data, (dict, httpx.Response)):
        raise TradeHandlerTypeException('order_data should be an order_json dict or httpx.Reponse object')
    
    if isinstance(order_data, dict):
        order_type = str(order_data['orderLegCollection'][0]['instruction'])
        order_symbol = str(order_data['orderLegCollection'][0]['instrument']['symbol'])
        order_shares = str(int(order_data['quantity']))
        if int(order_data['quantity']) == int(order_data['filledQuantity']):
            #MARKET_ORDER_FILLED_(BUY_(AAPL, 25))
            progress.s(f'MARKET_ORDER_FILLED_({order_type}_({order_symbol}, {order_shares}))')
        if int(order_data['quantity']) != int(order_data['filledQuantity']):
            #WAITING_FOR_FILL_(BUY_(AAPL, 25))
            progress.w(f'WAITING_FOR_FILL_({order_type}_({order_symbol}, {order_shares}))')
    
##### TODO: this is a duplicate, it is being handled twice, keep for now (3Jan2022) <>
    if isinstance(order_data, httpx.Response):
        
        if not order_type:
            raise ('passing order_response requires order_type to be set')
        if not isinstance(order_type, OrderType):
            raise TradeHandlerTypeException('order_type must be of type OrderType')
        if isinstance(order_type, OrderType.BUY):
            order_type = OrderType.BUY.value
        if isinstance(order_type, OrderType.SELL):
            order_type = OrderType.SELL.value
            
        if not order_symbol:
            raise TradeHandlerValueException('passing order_response requires order_symbol to be set')
            
        if not order_shares:
            raise TradeHandlerValueException('passing order_response requires order_shares to be set')
            
        if isinstance(order_symbol, str):
            order_symbol = order_symbol
        if isinstance(order_shares, int):
            order_shares = str(order_shares)
        #PLACING_MARKET_ORDER_(BUY_(AAPL, 25))
        progress.i(f'PLACING_MARKET_ORDER_({order_type}_({order_symbol}, {order_shares}))')
    
def order_get_details(tda_client, order_response, wait_for_fill=False, order_report=False):
##### TODO: create a RAW log in progress_report <>
##### TODO: think about using a tuple for wait_for_fill (sec_to_wait, sec_between_wait)
    ''' Get the detials of an order

    :param tda_client: The client object created by tda-api.
    :param `order_response`: The response object from a TDA order.
                           An order ID may also be passed.
    :param `wait_for_fill`: default is False, wait `int` seconds before canceling the order.
                          Passing True (or 1) will wait for fill indefinetly.
                          Checks status every 1 second (see wait_for_fill TODO:)
    :param `order_report`: default is False, 
                           True: reports fill status to MAIN
                                 and dumps raw json to DEBUG
    '''
    if not isinstance(tda_client, TDAClientClass):
        raise TradeHandlerTypeException('tda client object required to get order details')
    
    if order_response is None:
        raise TradeHandlerValueException('at least one, an order response or ID, must be passed')
        
    if isinstance(order_response, httpx.Response):
        order_response = Utils(tda_client, int(ACCOUNT_ID)).extract_order_id(order_response)
        throttle(0.3)
    
    if isinstance(order_response, int):
        order_json = tda_client.get_order(order_response, int(ACCOUNT_ID)).json()
        throttle(0.3)
        
    if isinstance(order_json['orderLegCollection'][0]['instrument']['symbol'], str):
        order_symbol = order_json['orderLegCollection'][0]['instrument']['symbol']
        
    if wait_for_fill: # everything but False
        if not isinstance(wait_for_fill, int): # cap non True/int
            raise TradeHandlerTypeException('wait for fill must be False, True, or an int')
        else: # True and int
            cycle_count = 0

            while int(order_json['quantity']) != int(order_json['filledQuantity']):
                if cycle_count < wait_for_fill:
                    if order_report:
                        _order_report(order_json)
                    sleep(1)
                    order_json = tda_client.get_order(order_response, int(ACCOUNT_ID)).json()
                    if wait_for_fill != 1:
                        cycle_count = cycle_count + 1
                    else:
                        pass # wait for fill indefinetly (useful mostly when selling)
                else:
                    try:
######################### TODO: think about how to handle symbols that do not fill, possible removal, see remove_symbol()
                        order_response = tda_client.cancel_order(order_json['orderId'], int(ACCOUNT_ID))
                        order_json = order_response.json()
                    except Exception as err:
######################### TODO: what exceptions can we expect here, to catch and handle properly
                        progress.e(f'Unexpected {err=}, {type(err)=} (order_response)_({order_symbol})')
                        progress.e(f'order_response, {order_response}')
                        order_json = order_response.json()
                        progress.e(f'order_json, {order_json}')
            if int(order_json['quantity']) == int(order_json['filledQuantity']):
                if order_report:
                    _order_report(order_json)
                    
    if order_report:
        progress.debug(order_json)
    
    return order_json

def order_place_equity_market(tda_client, order_type, order_symbol, order_shares, order_report=False):
    ''' Place an equity market order, either buy or sell.

    :param tda_client: The client object created by tda-api.
    :param order_type: BUY or SELL
    :param order_symbol: the symbol to buy or sell
    :param order_shares: share quantity to buy or sell
    :param order_report: default is False, when True, dumps a raw json to the MAIN log
    
    :return: order_response, to extract order details USE :meth:`order_get_details` 
    '''
    if not isinstance(tda_client, TDAClientClass):
        raise TradeHandlerTypeException('tda_client object required to place an order')
        
    if not isinstance(order_type, OrderType):
        raise TradeHandlerTypeException('order type must be OrderType.BUY/OrderType.SELL')
       
    if not isinstance(order_shares, int) or order_shares < 1:
        raise TradeHandlerValueException('order shares must be an int that is greater than zero')
    
    if isinstance(order_type, OrderType) and order_type == OrderType.BUY:
        order_response = tda_client.place_order(int(ACCOUNT_ID), equity_buy_market(order_symbol, order_shares))
     
    if isinstance(order_type, OrderType) and order_type == OrderType.SELL:
        order_response = tda_client.place_order(int(ACCOUNT_ID), equity_sell_market(order_symbol, order_shares))
     
    if isinstance(order_response, httpx.Response):
        if order_response.status_code not in {200, 201, 202}:
            progress.e((order_response.status_code, order_response))
        elif order_report:
            _order_report(order_response, order_type, order_symbol, order_shares)
          
    return order_response

buy_list = []
sell_list = []
profit_list = []
def data_syndicate(data_point, report_data=False, report_profit=False, return_profit=False):
    ''' 
    Turn BUY and SELL items into PROFIT 
    - primairly used for turning data points into a profit format 
      useful for further processing (ie. a spreadsheet, another function, etc.)
    
    :param data_point: takes an order_response json file.
    :param report_data: default is False.
                          - True reports every datapoint as it is consumed
                          - reports to Trace Log
    :param report_profit: default is False.
                          - True reports PROFIT after it has been calculated
                          - reports to Trace Log
    :param return_profit: default is False. 
                          True returns a list of tuples (symbol, profit)
    
    :return: depends
    '''
    if not isinstance(data_point, dict):
        raise DataSyndicateTypeException('data_point must be of type dict (an order_json)')

    if not isinstance(report_data, bool):
        raise DataSyndicateTypeException('report_data must be of type bool')
    
    if not isinstance(report_profit, bool):
        raise DataSyndicateTypeException('report_profit must be of type bool')
    
    if not isinstance(return_profit, bool):
        raise DataSyndicateTypeException('return_profit must be of type bool')
    
    order_type = data_point['orderLegCollection'][0]['instruction']
    if not isinstance(order_type, str):
        raise DataSyndicateTypeException('the extracted order_type is not a string')
        
    order_symbol = data_point['orderLegCollection'][0]['instrument']['symbol']
    if not isinstance(order_symbol, str):
        raise DataSyndicateTypeException('the extracted order_symbol is not a string')
    
    order_price = data_point['orderActivityCollection'][0]['executionLegs'][0]['price']
    if not isinstance(order_price, float):
        raise DataSyndicateTypeException('the extracted order_price is not a float')
    
    data_point = (order_type, order_symbol, str(order_price))
    if not isinstance(data_point, tuple):
        raise DataSyndicateTypeException('the newly created data_point is not a tuple')
    
    if data_point[0] == OrderType.BUY.value:
        buy_list.append(data_point)
        if report_data:
            progress.trace(f'{data_point[0]} | {data_point[1]} | {data_point[2]} | ')
        return None
    if data_point[0] == OrderType.SELL.value:
        sell_list.append(data_point)
        if report_data:
            progress.trace(f'{data_point[0]} | {data_point[1]} | {data_point[2]} | ')
        if len(buy_list) == len(sell_list):
            for buy_item in buy_list:
                for sell_item in sell_list:
                    if buy_item[1] == sell_item[1]:
                        profit = Decimal(sell_item[2]) - Decimal(buy_item[2])
                        profit_list.append((sell_item[1], str(profit)))
                        if report_profit:
                            progress.trace(f'{OrderType.PROFIT.value} | {sell_item[1]} | {profit} | ')
            if not return_profit:
                buy_list.clear()
                sell_list.clear()
                profit_list.clear()
                return None
            if return_profit:
                temp_profit_list = deepcopy(profit_list)
                buy_list.clear()
                sell_list.clear()
                profit_list.clear()
                return temp_profit_list # returned as a list of tuples (symbol, profit)