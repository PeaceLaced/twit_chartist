"""
- TEMPLATE.

"""

from twit.twit_api.api_command_handler import get_game_data, get_player_data

# this is a TEMPLATE
def run_TEMPLATE_command(self, command, player, args):
    
    # count number of args
    args_len = len(args)
    
    player_data = get_player_data(player)
    

    if args_len in {0}:
        
        return [f'{player},  ' +
                f'{player}']
    
    if args_len in {1}:
        
        return [f'{player},  ' +
                f'{player}']
    
    if args_len in {2}:
        
        return [f'{player},  ' +
                f'{player}']