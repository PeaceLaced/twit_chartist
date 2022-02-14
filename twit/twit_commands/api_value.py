"""
- value command API.

"""

from twit.twit_api.api_command_handler import get_game_data

from decimal import Context, setcontext, ROUND_DOWN
valuecontext = Context(prec=5, rounding=ROUND_DOWN)
setcontext(valuecontext)

def run_value_command(command, player, args):
    
    game_data = get_game_data()
    
    wit_modifier = game_data['WIT']['modifier'].to_decimal()
    wit_total = game_data['WIT']['total'].to_decimal()
    
    wit_value = wit_modifier / wit_total
    
    return [f'{player}, the current WIT value is {wit_value} ({wit_modifier} / {wit_total}).']