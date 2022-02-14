"""
- transfer command API.

"""
# TODO: once transfer ratio hits 0.9, revoke adding to transfer pool
###############################################################################
# TRANSFER  -   trasnfer wit to player or add to pool
# !transfer, command and pool/trigger info
# !transfer <wit>, add to pool (triggers increase ratio/decrease pool trigger)
# !transfer <to_player>, transfer wit to player
# PLAYER COST: player['wit'] = 1 WIT
# POOL TRIGGER: 1000 (minus 10 per activation)
# TRANSFER RATIO: 0.1/0.01/0.9 (start/step/max)
# XXX: update wit value (because ratio sink)
###############################################################################
# transfer - increase the transfer amount by 0.01 WIT, AND
#            reduce trigger by 10 (last trigger point 110, controlled by ratio)
# transfer WIT to another player, 1 to ratio 0.1/0.01/0.9 (start/step/max)
############################################################################### 
# !transfer         (DONE)
# !transfer <w>     
# !transfer <to>
###############################################################################

from twit.twit_api.api_command_handler import get_player_data, get_game_data
from twit.twit_api.api_command_handler import update_player, update_game
from twit.twit_api.api_command_handler import is_valid_chatter

from decimal import Context, setcontext, Decimal
valuecontext = Context(prec=5)
setcontext(valuecontext)

def run_transfer_command(self, command, player, args):
    
    # TODO: couple this data with the appropriate args_len block
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
    
    # make args useful
    if args_len in {1}:
        
        # get player data
        player_data = get_player_data(player)
        player_balance = player_data[player]['WIT'].to_decimal()
        is_valid_player = False
        
        try: update_amt = Decimal(float(args[0]))
        except:
            is_valid_player = is_valid_chatter(self, args[0])
            if not is_valid_player:
                return [f'{player}, !{command.lower()} param must be a float or an active player. ',
                        'TRY: !transfer <float_to_pool> OR !transfer <name_of_player>.']
        
        # handle the arg as a user, indicating transfer_to someone
        if is_valid_player:
            
            transfer_to = args[0].upper()
            
            # hardcoded 1 as cost per transfer
            if not player_balance >= Decimal(1.00):
                return [f'{player}, you do not have enough WIT for this transaction.']
            
            # calculate player balance for after purchase, update database
            update_player_balance = player_balance - Decimal(1.00)
            player_new_balance = update_player(player, update_player_balance, update_type='PLAYER-WIT')
            
            # get transfer to player data, calculate new balance for transfer to player, update database
            transfer_to_balance = get_player_data(transfer_to)[transfer_to]['WIT'].to_decimal()
            update_transfer_to = transfer_to_balance + transfer_ratio
            transfer_to_new_balance = update_player(transfer_to, update_transfer_to, update_type='PLAYER-WIT')
            
            # calculate new system wit total (sink = 1 minus transfer ratio), update database
            # cost is 1 wit to transfer, transfer ratio stays in the system, difference is removed
            update_system_wit = wit_system_total - (Decimal(1.00) - transfer_ratio)
            update_game(command, update_system_wit, update_type='SYSTEM-WIT')

            return [f'{player}, you transfered {transfer_ratio} to {transfer_to}, their balance is ' +
                    f'now {transfer_to_new_balance} and your balance is {player_new_balance}.']
        
        # standard pool logic
        if isinstance(update_amt, Decimal):
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