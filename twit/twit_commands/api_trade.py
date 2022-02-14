"""
- trade command API.

"""
from pytz import timezone
from datetime import datetime
from random import randrange

from twit.twit_api.api_command_handler import get_game_data, get_player_data
from twit.twit_api.api_command_handler import update_game, update_player

from decimal import Context, setcontext, Decimal
valuecontext = Context(prec=5)
setcontext(valuecontext)

# TRADE     -   live trade a stock to increase the modifier
# !trade, command and pool/trigger info
# !trade <wit>, add to pool (triggers random trade)
# !trade list, return symbol list to chat
# !trade <symbol> <seconds>, update modifier
# PLAYER COST: player['wit'] = 1 WIT
# POOL TRIGGER: 1 WIT
# XXX: update wit value (because 1 WIT)
# XXX: update wit value (because modifier changes)

###############################################################################

# !trade
# !trade <w>
# !trade list
# !trade <sy> <se>

###############################################################################
# trade     - 1 WIT(pool)      - trigger random live trade, change modifier based on profit/loss
###############################################################################

# TODO: add a !trade specs (or something similar) so people can see volatility, price, volume, etc etc
def run_trade_command(command, player, args):

    tz = timezone('US/Eastern')

    # TODO: adjust these after setting trade time to 7AM and 8PM
    if datetime.now(tz).hour >= 15:
        if datetime.now(tz).hour >= 16:
             return [f'{player}, the market is closed for the day. If you want to adjust the ' +
                     'modifier, USE: !something or !something or !something']
        if datetime.now(tz).minute >= 40:
             return [f'{player}, the market is about to close. If you want to adjust the ' +
                     'modifier, USE: !something or !something or !something']
    
    args_len = len(args)
    
    # TODO: couple this data with the appropriate args_len block
    game_data = get_game_data()
    pool_balance = game_data['POOL'][command]['total'].to_decimal()
    pool_trigger = Decimal(game_data['POOL'][command]['trigger'])
    symbol_list = game_data['SYMBOL']['list']
    symbol_count = game_data['SYMBOL']['count']
    player_data = get_player_data(player)
    player_balance = player_data[player]['WIT'].to_decimal()
    wit_system_total = game_data['WIT']['total'].to_decimal()
    
    # return stats/description for the pool
    if args_len in {0}:
        return [f'{player}, the {command.lower()} POOL is at {pool_balance} ' +
                f'with a pool TRIGGER of {pool_trigger}.']
    
    # update pool, return a list of symbols, or error
    if args_len in {1}:
        
        symbol_list = game_data['SYMBOL']['list']
        symbol_count = game_data['SYMBOL']['count']
        
        try: update_amt = Decimal(float(args[0]))
        except:
            # send list of symbols to chat or error
            if not args[0] in {'list'}:
                return [f'{player}, TRY: !trade list, !trade <float> or !trade <symbol> <seconds>.']
            
            return [f'{player}, here is the symbol list: ' + ', '.join(symbol_list)]
            
        # add to pool
        if isinstance(update_amt, Decimal):
            
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
                    
                random_seconds = randrange(25, 55)
                
                # WARNING: do not change the first line of this message. IT TRIGGERS TRADING
                return [f'~live_trade {random_symbol} {random_seconds} seconds for {player}. ' +
                        f'Congratulations, {command.lower()} POOL activated, a random trade was processed. ' +
                        f'Pool balance is now {pool_new_balance} and player balance is {player_new_balance}.']
            
            if not activate_trigger:
                return [f'{player}, The {command.lower()} POOL is now at {pool_new_balance}. ' +
                        f'Your new balance is {player_new_balance}.']
    
    if args_len in {2}:
        
        trade_symbol = args[0]

        if trade_symbol.upper() not in symbol_list:
            return [f'{player}, {trade_symbol} is not in the trade list. TRY: !trade list.']
        
        try: hold_seconds = int(args[1])
        except: return [f'{player}, the seconds param must be an int']
        
        if hold_seconds not in range(25, 56):
            return [f'{player}, the seconds param must be between 25 and 55.']
        
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
    
    if args_len > 2:
        return [f'{player}, USE: !trade, !trade list or !trade <symbol> <seconds>']