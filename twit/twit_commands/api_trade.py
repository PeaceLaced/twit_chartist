"""
- trade command API.

"""
from pytz import timezone
from datetime import datetime
from random import randrange

from twit.twit_api.api_command_handler import get_game_data, get_player_data
from twit.twit_api.api_command_handler import update_game, update_player

from decimal import Decimal, Context, ROUND_HALF_EVEN, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

# hardcode times for easy adjustment
HOLD_MIN = 25
HOLD_MAX = 55

def run_trade_command(command, player, args):
    
    tz = timezone('US/Eastern')
    if datetime.now(tz).hour < 7:
        return [f'{player}, the market is not open, please wait until 7AM eastern.']
    if datetime.now(tz).hour >= 19:
        if datetime.now(tz).hour >= 20:
             return [f'{player}, the market is closed for the day. If you want to adjust the ' +
                     'modifier, USE: !something or !something or !something']
        if datetime.now(tz).minute >= 40:
             return [f'{player}, the market is about to close. If you want to adjust the ' +
                     'modifier, USE: !something or !something or !something']
    
    args_len = len(args)
    
    game_data = get_game_data()
    pool_balance = game_data['POOL'][command]['total'].to_decimal()
    pool_trigger = Decimal(game_data['POOL'][command]['trigger'])
    symbol_list = game_data['SYMBOL']['list']
    symbol_count = game_data['SYMBOL']['count']
    player_data = get_player_data(player, query_type='COMMAND')
    player_balance = player_data[player]['WIT'].to_decimal()
    wit_system_total = game_data['WIT']['total'].to_decimal()
    
    # return stats/description for the pool
    if args_len in {0}:
        return [f'{player}, the {command.lower()} POOL is at {pool_balance} ' +
                f'with a pool TRIGGER of {pool_trigger}.']
    
    # one arg is adding to pool or returning the symbol list
    if args_len in {1}:
        
        symbol_list = game_data['SYMBOL']['list']
        symbol_count = game_data['SYMBOL']['count']
        
        # convert to float and add to pool
        # this is still failing for some reason
        try: 
            update_amt = Decimal(float(args[0])) # some sort of issue here (0.99)
        
            activate_trigger = False
            
            # check that the player has enough wit for the transaction
            if not player_balance >= update_amt:
                return [f'{player}, you do not have enough WIT for this transaction.']
            
            # check that the transaction is not greater than the pool_trigger
            if update_amt >= pool_trigger:
                return [f'{player}, You may only add less than {pool_trigger} WIT at a time ' +
                        f'to the {command.lower()} POOL or USE: !trade <symbol> <seconds>. ']
            
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
                
                # send a message to trade bot for random trade
                for key, symbol in enumerate(symbol_list):
                    if randrange(1, symbol_count) == key:
                        random_symbol = symbol
                    
                random_seconds = randrange(HOLD_MIN, HOLD_MAX+1)
                
                # WARNING: do not change the first line of this message. IT TRIGGERS TRADING
                return [f'~live_trade {random_symbol} {random_seconds} seconds for {player}. ' +
                        f'Congratulations, {command.lower()} POOL activated, a random trade was processed. ' +
                        f'Pool balance is now {pool_new_balance} and player balance is {player_new_balance}.']
            
            if not activate_trigger:
                return [f'{player}, The {command.lower()} POOL is now at {pool_new_balance}. ' +
                        f'Your new balance is {player_new_balance}.']
        
        # return a list of tradable symbols
        except:
            if not args[0] in {'list'}:
                return [f'{player}, TRY: !trade list, !trade <float> or !trade <symbol> <seconds>.']
            
            return [f'{player}, here is the symbol list: ' + ', '.join(symbol_list)]
            

    # two args is a manual trade
    if args_len in {2}:
        
        trade_symbol = args[0].upper()

        if trade_symbol.upper() not in symbol_list:
            return [f'{player}, {trade_symbol} is not in the trade list. TRY: !trade list.']
        
        try: hold_seconds = int(args[1])
        except: return [f'{player}, the seconds param must be an int']
        
        if hold_seconds not in range(HOLD_MIN, HOLD_MAX+1):
            return [f'{player}, the seconds param must be between {HOLD_MIN} and {HOLD_MAX}.']
        
        # update player balance
        if not player_balance >= Decimal(1.00):
            return [f'{player}, you do not have enough WIT for this transaction.']
        
        update_player_balance = player_balance - Decimal(1.00)
        player_new_balance = update_player(player, update_player_balance, update_type='PLAYER-WIT')
        
        # update total wit balance
        update_total_balance = wit_system_total - Decimal(1.00)
        update_game(command, update_total_balance, update_type='SYSTEM-WIT')

        # WARNING: do not change the first line of this message. IT TRIGGERS TRADING
        return [f'~live_trade {trade_symbol} {hold_seconds} seconds for {player}.']
    
    # assume anything over two arg was entered incorrectly 
    if args_len > 2:
        return [f'{player}, USE: !trade, !trade list or !trade <symbol> <seconds>']