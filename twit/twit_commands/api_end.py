"""
- end command API.

"""
# END       -   end stream, end game, convert all wit to twit, no champ
# !end, command and pool/trigger info
# !end <wit>, add to end pool
# PLAYER COST: <wit>
# POOL TRIGGER: 1000
#------------------------------------------------------------------------------
# logic to end game
# - convert wit to twit
# - accumulate all pools (still deciding what to do with left over pools)
# - 
from twit.twit_api.api_command_handler import get_player_data, get_game_data, end_game
from twit.twit_api.api_command_handler import update_player, update_game

from decimal import Context, setcontext, Decimal
valuecontext = Context(prec=5)
setcontext(valuecontext)

def run_end_command(command, player, args):
    
    DEFAULT_FEND = 100
    FEND_COST = 1.00
    game_data = get_game_data()
    pool_balance = game_data['POOL'][command]['total'].to_decimal()
    pool_trigger = Decimal(game_data['POOL'][command]['trigger'])
    player_data = get_player_data(player)
    player_balance = player_data[player]['WIT'].to_decimal()
    
    # count number of args
    args_len = len(args)
    
    # return stats/description for the pool
    if args_len in {0}:
        return [f'{player}, the {command.lower()} POOL is at {pool_balance} ' +
                f'with a pool TRIGGER of {pool_trigger}']
    
    # first try float cast, then try fend
    if args_len in {1}:
        try: update_amt = Decimal(float(args[0]))
        except:
            
            # if not fend arg, error
            if not args[0] in {'fend'}:
                return [f'{player}, !{command.lower()} param must be fend or a float.']
            
            # fend checks player balance, then updates trigger
            if not player_balance >= Decimal(FEND_COST):
                return [f'{player}, you do not have enough wit for that transaction.']
            
            # subtract one wit from player balance
            update_player_balance = player_balance - Decimal(FEND_COST)
            player_new_balance = update_player(player, update_player_balance, update_type='PLAYER-WIT')
            
            # calculate new trigger if fend, update database
            update_end_trigger = pool_trigger + Decimal(DEFAULT_FEND)
            updated_trigger = update_game(command, update_end_trigger, update_type='COMMAND')
            
            return [f'{player}, the end pool trigger increased by {DEFAULT_FEND}, the ' +
                    f'new end pool trigger is {updated_trigger}. Your new balance ' +
                    f'is {player_new_balance}.']
        
        activate_trigger = False
        
        # update_amt is what they are adding to the pool, calculate then send to update player balance
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
        
        # when the trigger is activated, end the game
        if activate_trigger:
            if end_game(None, end_type='END'):
                return [f'{player} topped off the {command.lower()} POOL. The game is now over.']
        
        if not activate_trigger:
            return [f'{player}, {command.lower()} POOL is now at {pool_new_balance}. ' +
                    f'Your new balance is {player_new_balance}.']