"""
- guest command API.
# fully tested 28 Feb 2022
"""
from twit.twit_api.api_command_handler import get_player_data, update_player

def run_guest_command(command, player, args):
    
    # player data for the person triggering the command
    player_data = get_player_data(player, query_type='COMMAND')
    player_guest_list = player_data[player]['guests']
    player_guest_status = player_data[player]['guest']
    player_guest_count = len(player_guest_list)
    
    # count number of args
    args_len = len(args)
    
    # !guest with no arguments returns str(None) or a player name who added you as a guest
    if args_len in {0}:
        
        if player_guest_status in {'None'}:
            return [f'{player}, you are not on a guest list.']
        return [f'{player}, you are a guest of {player_guest_status}.']
    
    # !guest with one argument returns a list of your guests or if another person is a guest
    if args_len in {1}:
        
        if args[0] in {'list'}:
            # !guest list
            if player_guest_count in {0}:
                return [f'{player}, you do not have anyone on your guest list.']
            return [f'{player}, your current guest list is {player_guest_list}.']
        
        # remove yourself from a guest list (in order to add game time)
        if args[0] in {'purge'}:
            if player_guest_status in {'None'}:
                return [f'{player}, nothing to purge, you are not on a guest list.']
            purge_response = update_player(player, player_guest_status, update_type='PURGE')
            if purge_response in {'None'}:
                return [f"{player}, you've been purged of guest status. You are no longer on a guest list."]
            return ['@peacelaced something went wrong with the guest PURGE function.']
        
        # see the guests of another player, must pass a valid player
        if args[0] not in {'list'}:
            arg_player = args[0].upper()
            arg_player_data = get_player_data(arg_player, query_type='OTHER')
            
            # arg_player_data returns false means not Valid Player
            if not arg_player_data:
                return [f'{player}, please provide a valid player to check their guest status.']
            
            arg_player_guest_status = arg_player_data[arg_player]['guest']
            
            if arg_player_guest_status in {'None'}:
                return [f'{player}, the player {arg_player} is not on any guest list.']
            return [f'{player}, the player {arg_player} is on {arg_player_guest_status} guest list.']
            
    if args_len in {2}:
        
        # arg_action is add or remove, error otherwise
        arg_action = args[0].lower()
        if arg_action not in {'add', 'remove'}:
            return [f'{player}, USE: !guest add <valid_player> OR !guest remove <your_guest>']
        
        # player being added to the guest list
        arg_player = args[1].upper()
        
        if arg_action in {'remove'}:
            
            # check if has any to remove
            if player_guest_count in {0}:
                return [f'{player}, you do not have any guests to remove. ' +
                        'USE: !guest add <valid_player> to add some guests.']
            
            # check if want to remove exists
            if arg_player not in player_guest_list:
                return [f'{player}, {arg_player} is not in your guest list.']
            
            # remove player from arg_player, remove arg_player from player, return updated
            update_player(arg_player, 'None', update_type='GUEST')
            player_guest_list.remove(arg_player)
            updated_guest_list = update_player(player, player_guest_list, update_type='GUEST_LIST')
            
            if len(updated_guest_list) in {0}:
                return [f'{player}, {arg_player} was removed from your guest list, your list is now empty.']
            
            return [f'{player}, {arg_player} was removed from your guest list, ' +
                    f'your updated list is {updated_guest_list}.']

        if arg_action in {'add'}:
            
            if player == arg_player:
                return [f"{player}, why add yourself when you can add a bot? That's kinda the point."]
            
            # is arg_player valid, error if False
            valid_arg_player = get_player_data(arg_player, query_type='OTHER')
            if not valid_arg_player:
                return [f'{player}, {arg_player} is not a valid player, please try again.']
            
            # does player have 2 guests
            if player_guest_count in {2}:
                return [f'{player}, you may only have two guests. Your current list is ' + 
                        f'{player_guest_list}. USE: !guest remove <your_guest> to remove one and try again.']
            
            # is arg_player already on a list
            arg_player_status = valid_arg_player[arg_player]['guest']
            if  arg_player_status not in {'None'}:
                return [f'{player}, players may only be in one guest list. {arg_player} is ' +
                        f'currently a guest of {arg_player_status}']

            # update arg_player['guest'] with player
            update_player(arg_player, player, update_type='GUEST')
            
            # update player['guests'] with arg_player
            player_guest_list.append(arg_player)
            updated_guest_list = update_player(player, player_guest_list, update_type='GUEST_LIST')
            
            return [f'{player}, your guest list updated successfully. The new guest list is {player_guest_list}']
        
    # assume anything over two arg was entered incorrectly        
    if args_len > 2:
        return [f'{player}, TRY: !guest, !guest list, !guest purge, ' +
                '!guest add <valid_player> OR !guest remove <valid_player>.']