"""
- live_trade command API.

"""

from twit.twit_api.api_trade_handler import trade_handler
from twit.twit_api.api_command_handler import get_game_data, update_game

from decimal import Decimal, Context, ROUND_HALF_EVEN, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

def run_live_trade_command(self, command, player, args, tda_client):
    ''' 
    make live trades through TD Ameritrade
    args validation happens in api_trade.py (twit_chart BOT)
    
    '''
    # get the symbol, seconds and player from args
    trade_symbol = args[0].upper()
    hold_seconds = args[1]
    player = args[4].strip('.')

    # process trade, capture profit, update modifier
    profit_response = trade_handler(tda_client, (trade_symbol, hold_seconds))
    
    # get the current modifier, calculate the new modifier based on p/l, update the database
    game_data = get_game_data()
    current_modifier = game_data['WIT']['modifier'].to_decimal()
    update_modifier = current_modifier + Decimal(profit_response)
    update_response = update_game(command, update_modifier, update_type='MODIFIER')
    
    # get data and report the updated wit value
    updated_total = update_response['WIT']['total'].to_decimal()
    updated_modifier = update_response['WIT']['modifier'].to_decimal()
    updated_wit_value = updated_modifier / updated_total
    
    # return a message with the new wit value
    return [f'{player}, {trade_symbol} was successfully traded. P/L was {profit_response}. ' +
            f'The new modifier is {updated_modifier} and the new WIT value is {updated_wit_value}.']