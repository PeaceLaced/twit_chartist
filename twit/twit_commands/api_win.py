"""
- win command API.

"""
from twit.twit_api.api_command_handler import get_player_data, get_game_data
from twit.twit_api.api_command_handler import update_player, update_game, end_game

from decimal import Decimal, Context, ROUND_HALF_EVEN, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

def run_win_command(command, player, args):
    
    game_data = get_game_data()
    pool_balance = game_data['POOL'][command]['total'].to_decimal()
    pool_trigger = Decimal(game_data['POOL'][command]['trigger'])
    win_trigger = game_data['WIT']['win'].to_decimal()
    game_count = game_data['WIT']['game']
    wit_system_total = game_data['WIT']['total'].to_decimal()
    
    # count number of args
    args_len = len(args)
    
    # return stats/description for the pool
    if args_len in {0}:
        return [f'{player}, the {command.lower()} POOL is at {pool_balance} ' +
                f'with a pool TRIGGER of {pool_trigger}. The WIN trigger is {win_trigger}.']
    
    # one arg is wit amount or valid player (a channel really)
    if args_len in {1}:
        
        # get player data
        player_data = get_player_data(player, query_type='COMMAND')
        player_balance = player_data[player]['WIT'].to_decimal()
        is_validCHAN = False
        
        # float is adding to pool
        try: 
            update_amt = Decimal(float(args[0]))
            
            activate_trigger = False
            
            # does the player have enough wit?
            if not player_balance >= update_amt:
                return [f'{player}, you do not have enough WIT for this transaction.']
            
            # check that the transaction is not greater than the pool_trigger
            if update_amt >= pool_trigger:
                return [f'{player}, You may only add less than {pool_trigger} WIT at a time ' +
                        f'to the {command.lower()} POOL. ']
            
            # calculate player balance and update database (working)
            update_player_balance = player_balance - update_amt
            player_new_balance = update_player(player, update_player_balance, update_type='PLAYER-WIT')
            
            # calculate pool balance, check for trigger, send update to database
            update_pool_balance = pool_balance + update_amt
            if update_pool_balance >= pool_trigger:
                activate_trigger = True
                update_pool_balance = update_pool_balance - pool_trigger
            pool_new_balance = update_game(command, update_pool_balance, update_type='POOL-WIT')
            
            # trigger the win pool, add 0.1 to win trigger and subtract 1 from system total
            if activate_trigger:
                
                # calculate update to trigger and system wit, update database
                # win trigger is D128(add 0.1), system wit is D128 (sub 1.00)
                update_trigger = win_trigger + Decimal(0.1)
                update_wit = wit_system_total - Decimal(1.00)
                updated_win = update_game(command, (update_trigger, update_wit), update_type='COMMAND')
    
                return [f'Congradulations, {player} has activated the {command.lower()} POOL. ' +
                        f'It now cost {updated_win} WITs to win the game. ' +
                        f'Pool balance is now {pool_new_balance} and player balance is {player_new_balance}.']
            
            if not activate_trigger:
                return [f'{player}, {command.lower()} POOL is now at {pool_new_balance}. ' +
                        f'Your new balance is {player_new_balance}.']
        
        # valid player
        except:
            
            # arg player is a valid player passed as an arg, added to raid list/gift sub list etc etc.
            arg_player = args[0].upper()
            arg_player_data = get_player_data(arg_player, query_type='OTHER')
            
            if not arg_player_data:
                return [f'{player}, !win param must be a float or a valid twitch channel. ',
                        'TRY: !win <float_to_pool> OR !win <valid_channel>.']
            
            # make sure they are allowed to win the game
            if not player_balance > win_trigger:
                return [f'{player}, you do not have enough WITs to WIN the game.']
            
            updated_game_count = Decimal(game_count) + Decimal(1)
            
            # call end_game to win, pass player and arg_player
            if end_game((player, arg_player), end_type='WIN'):
                return [f'{player} has won the game, all wit has been converted to TWIT, ' +
                        f'all settings reset to default. Starting game number {int(updated_game_count)}.']
            
    # assume anything over one arg was entered incorrectly        
    if args_len > 1:
        return [f'{player}, TRY: !win <wit_amount> OR !win <valid_twitch_chan>.']
    
            