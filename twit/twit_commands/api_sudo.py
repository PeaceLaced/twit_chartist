"""
- sudo command API.

"""
from twit.twit_api.api_command_handler import get_game_data, get_player_data

# this is a TEMPLATE
def run_sudo_command(self, command, player, args):
    
    # - last_game prep db for no games after the next game
    '''
    def run_last_game_command(command, player, args):
        
        if not is_SUPERUSER(player.lower()):
            return [f'{player}, you do not have access to the last_game command.']
        is_last_game = update_game(command, None, update_type='COMMAND')
        if not is_last_game: #false
            return ['This is not the last game']
        return ['This is the last game']
    '''
    
    # - fresh_game
    # - new_game
    # -- something to zero everything
    
    # - last_call (five(something) minute notice before turning off point redemptions)

    # - think of some more super user commands to add, check notes
    # 
    
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

