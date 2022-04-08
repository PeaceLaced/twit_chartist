"""
- balance command API.
# fully tested 28 Feb 2022
"""
from twit.twit_api.api_command_handler import get_player_data

def run_balance_command(command, player, args):
    '''
    arg_len 0, return chat message
                - player balance, twit, and wins
    arg_len 1, return chat message
                - param player balance, wit, wins
    '''
    args_len = len(args)
    
    # return player balance
    if args_len in {0}:
        
        player_data = get_player_data(player, query_type='COMMAND')
        player_wit = str(player_data[player]['WIT'].to_decimal())
        player_twit = str(player_data[player]['TWIT'].to_decimal())
        player_win = player_data[player]['WIN']
        
        return [f'{player} has {player_wit} WIT, {player_twit} TWIT, and {player_win} WINs.']

    # return another players balance
    if args_len in {1}:

        # make sure the arg is a valid player
        arg_player = args[0].upper()
        arg_player_data = get_player_data(arg_player, query_type='OTHER')
        
        if not arg_player_data:
            return [f'{player}, !balance param must be a valid player. TRY: !balance <valid_player>']
        
        # get the valid/active player data, parse, and return the chat message
        arg_player_wit_balance = arg_player_data[arg_player]['WIT'].to_decimal()
        arg_player_twit_balance = arg_player_data[arg_player]['TWIT'].to_decimal()
        arg_player_win_balance = arg_player_data[arg_player]['WIN']
        
        return [f'{player}, balance data for {arg_player} is {arg_player_wit_balance} WIT, ' +
                f'{arg_player_twit_balance} TWIT, and {arg_player_win_balance} WINs.']
    
    # assume anything over one arg was entered incorrectly        
    if args_len > 1:
        return [f'{player}, TRY: !balance OR !balance <valid_player>.']

    
    