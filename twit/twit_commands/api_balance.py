"""
- balance command API.

"""

from twit.twit_api.api_command_handler import get_player_data, is_valid_chatter

def run_balance_command(self, command, player, args):
    '''
    arg_len 0, return chat message
                - player balance, twit, and wins
    arg_len 1, return chat message
                - param player balance, wit, wins
    '''
    
    args_len = len(args)
    
    # return player balance
    if args_len in {0}:
        
        player_data = get_player_data(player)
        player_wit = str(player_data[player]['WIT'].to_decimal())
        player_twit = str(player_data[player]['TWIT'].to_decimal())
        player_win = player_data[player]['WIN']
        
        return [f'{player} has {player_wit} WIT, {player_twit} TWIT, and {player_win} WINs.']
    
    # return another players balance
    if args_len in {1}:
        
        # make sure the arg is a valid and active player
        active_player = args[0].upper()
        is_valid_player = is_valid_chatter(self, active_player)
        
        if not is_valid_player:
            return [f'{player}, !{command.lower()} param must be an active player. ',
                    'TRY: !transfer <name_of_player>.']
        
        # get the valid/active player data, parse, and return the chat message
        checked_player_data = get_player_data(active_player)
        checked_wit_balance = checked_player_data[active_player]['WIT'].to_decimal()
        checked_twit_balance = checked_player_data[active_player]['TWIT'].to_decimal()
        checked_win_balance = checked_player_data[active_player]['WIN']
        
        return [f'{player}, the balance for {active_player} is {checked_wit_balance} WIT, ' +
                f'{checked_twit_balance} TWIT, and {checked_win_balance} WINs.']
    
    # assume anything over one arg was entered incorrectly        
    if args_len > 1:
        return [f'{player}, TRY: !transfer OR !transfer <name_of_player>.']
    
    