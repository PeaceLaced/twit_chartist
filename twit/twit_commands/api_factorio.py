"""
- factorio command API.
# fully tested 28 Feb 2022
"""
from twit.twit_api.api_command_handler import get_player_data, get_game_data
from twit.twit_api.api_command_handler import update_player, update_game

from decimal import Decimal, Context, ROUND_HALF_EVEN, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

def run_factorio_command(command, player, args):
    
    game_data = get_game_data()
    pool_balance = game_data['POOL'][command]['total'].to_decimal()
    pool_trigger = Decimal(game_data['POOL'][command]['trigger'])
    wit_system_total = game_data['WIT']['total'].to_decimal()
    
    # count number of args
    args_len = len(args)
    
    # return stats/description for the pool
    if args_len in {0}:
        return [f'{player}, the {command.lower()} POOL is at {pool_balance} ' +
                f'with a pool TRIGGER of {pool_trigger}']
    
    # one arg is float
    if args_len in {1}:
        
        # pools require float values
        try: 
            update_amt = Decimal(float(args[0]))
            
            activate_trigger = False
            
            # get player balance, calculate, send to update
            player_data = get_player_data(player, query_type='COMMAND')
            player_balance = player_data[player]['WIT'].to_decimal()
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
            
            # calculate system wit, send update to database
            if activate_trigger:
                update_system_wit = wit_system_total - pool_trigger
                update_game(command, update_system_wit, update_type='SYSTEM-WIT')

                return [f'Congradulations, {player} has activated the {command.lower()} POOL. ' +
                        f'Pool balance is now {pool_new_balance} and player balance is {player_new_balance}.']
            
            if not activate_trigger:
                return [f'{player}, {command.lower()} POOL is now at {pool_new_balance}. ' +
                        f'Your new balance is {player_new_balance}.']
        
        # error if arg is not a float
        except: return [f'{player}, !{command.lower()} param must be a float.']
        
    # assume anything over one arg was entered incorrectly        
    if args_len > 1:
        return [f'{player}, TRY: !factorio or !factorio <wit_amount>.']