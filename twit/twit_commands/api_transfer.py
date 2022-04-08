"""
- transfer command API.

"""
from twit.twit_api.api_command_handler import get_player_data, get_game_data
from twit.twit_api.api_command_handler import update_player, update_game

from decimal import Decimal, Context, ROUND_HALF_EVEN, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

def run_transfer_command(command, player, args):

    game_data = get_game_data()
    pool_balance = game_data['POOL'][command]['total'].to_decimal()
    pool_trigger = Decimal(game_data['POOL'][command]['trigger'])
    transfer_ratio = game_data['WIT']['transfer'].to_decimal()
    wit_system_total = game_data['WIT']['total'].to_decimal()
    
    # count number of args
    args_len = len(args)
    
    # return stats/description for the pool
    if args_len in {0}:
        return [f'{player}, the {command.lower()} POOL is at {pool_balance} ' +
                f'with a pool TRIGGER of {pool_trigger}. The transfer ratio ' +
                f'is currently {transfer_ratio}.']
    
    # one arg is float or valid_player
    if args_len in {1}:
        
        # get player data
        player_data = get_player_data(player, query_type='COMMAND')
        player_balance = player_data[player]['WIT'].to_decimal()
        
        # float arg is adding to pool
        try: 
            update_amt = Decimal(float(args[0]))
            
            activate_trigger = False
            
            # check palyer balance, format update, send update
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
                
                # calculate update to ratio and trigger, update database
                # transfer ratio is D128(0.01), transfer trigger is INT(10)
                update_ratio = transfer_ratio + Decimal(0.01) # increase the ratio on trigger
                update_trigger = pool_trigger - Decimal(10) # decrease cost for next trigger
                updated_game = update_game(command, (update_ratio, update_trigger), update_type='COMMAND')
                
                # get new valuse from update and report
                transfer_ratio = updated_game['WIT']['transfer']
                transfer_trigger = updated_game['POOL']['TRANSFER']['trigger']
    
                return [f'Congradulations, {player} has activated the {command.lower()} POOL. ' +
                        f'The new RATIO is {transfer_ratio}. The new TRIGGER is {transfer_trigger}. ' +
                        f'Pool balance is now {pool_new_balance} and player balance is {player_new_balance}.']
            
            if not activate_trigger:
                return [f'{player}, The {command.lower()} POOL is now at {pool_new_balance}. It needs ' +
                        f'{pool_trigger} to trigger. The transfer RATIO is {transfer_ratio}. ' +
                        f'Your new balance is {player_new_balance}.']
        
        # valid_player is an attempt to transfer
        except:
            
            # test if valid player, get their data to use if valid
            transfer_to = args[0].upper()
            transfer_to_data = get_player_data(transfer_to, query_type='OTHER')
            
            # player not valid, and failed float cast, so error
            if not transfer_to_data:
                return [f'{player}, !transfer param must be a float or an active player. ' +
                        'TRY: !transfer <float_to_pool> OR !transfer <valid_player>.']
            
            # hardcoded 1 as cost per transfer
            if not player_balance >= Decimal(1.00):
                return [f'{player}, you do not have enough WIT for this transaction.']
            
            # calculate player balance for after purchase, update database
            update_player_balance = player_balance - Decimal(1.00)
            player_new_balance = update_player(player, update_player_balance, update_type='PLAYER-WIT')
            
            # get transfer to player data, calculate new balance for transfer to player, update database
            transfer_to_balance = get_player_data(transfer_to, query_type='COMMAND')[transfer_to]['WIT'].to_decimal()
            update_transfer_to = transfer_to_balance + transfer_ratio
            transfer_to_new_balance = update_player(transfer_to, update_transfer_to, update_type='PLAYER-WIT')
            
            # calculate new system wit total (sink = 1 minus transfer ratio), update database
            # cost is 1 wit to transfer, transfer ratio stays in the system, difference is removed
            update_system_wit = wit_system_total - (Decimal(1.00) - transfer_ratio)
            update_game(command, update_system_wit, update_type='SYSTEM-WIT')

            return [f'{player}, you transfered {transfer_ratio} to {transfer_to}, their balance is ' +
                    f'now {transfer_to_new_balance} and your balance is {player_new_balance}.']
        
    # assume anything over one arg was entered incorrectly        
    if args_len > 1:
        return [f'{player}, TRY: !transfer, !transfer <wit_amount> OR !transfer <valid_player>.']