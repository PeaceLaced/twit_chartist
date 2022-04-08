"""
- value command API.

"""

from twit.twit_api.api_command_handler import get_game_data

from decimal import Context, ROUND_HALF_EVEN, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

def run_value_command(command, player, args):
    
    game_data = get_game_data()
    
    wit_modifier = game_data['WIT']['modifier'].to_decimal()
    wit_total = game_data['WIT']['total'].to_decimal()
    
    # once the game logic is in place, this should never happen
    if not wit_total > 0:
        return [f'{player}, zero wit in the system means the game has not started.']
    
    wit_value = wit_modifier / wit_total
    
    return [f'{player}, the current WIT value is {wit_value} ({wit_modifier} / {wit_total}).']