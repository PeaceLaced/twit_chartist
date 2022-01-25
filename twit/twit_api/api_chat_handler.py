"""
- chat_handler API. Anything returning to chat comes from here. Create here or from DB.

"""
import pytz
from datetime import datetime
from twit.twit_api.config.config_twitch import SUPER_USER
from twit.twit_api.api_trade_handler import trade_handler
from twit.twit_api.api_database_handler import mongo_data_handler

# decimal cast at calculation
from decimal import Decimal
from bson.decimal128 import Decimal128

###########################################################################
# INPUT logic for commands as chat_handler()

# TODO: think more about SUPER_USER, when to use, how to implement, etc.
# TODO: COMMAND:TRADE(datetime.now), setup trade time 7AM and 8PM, then adjust these
# TODO: SWITCH:TRADE(Decimal128), turn new modifier into new wit value once set up
# TODO: SWITCH:COMMAND, add/update descriptions, double check prior to launch

def chat_handler(author_name, command_name, command_args, tda_client=None):
    ''' handler for every chat command, always return a list of strings
        
        SWITCH is for _chat_handler in (this file)
        
        OPERATION is for database in api_database_handler
    '''
    COMMAND_NAME = command_name 
    try:
        command_arg_one = command_args[0]
    except:
        command_arg_one = False
    try:
        command_arg_two = command_args[1]
    except:
        command_arg_two = False
    
    
    ###########################################################################
    # WIN, TRADE, TRANSFER
    ''' '''
    if COMMAND_NAME in {'win'}:
        
        # win       - 10 WIT    - amount required to win GIFTED or TWIT_CHAMP
        # increase when pool is used, info only, method will give correct data
        
        # require this command to be !win gifted or !win champ
        # call a get WIN function to tell us what is required in order to win the game
        # if they have enough WIT, all zero out logic goes here
        # write author_name to db, if champ, give access to champ bot
        # otherwise, whatever logic for gifted logic
        
        pass
        
    if COMMAND_NAME in {'trade', 'live_trade'}:
        
        if COMMAND_NAME in {'live_trade'}:
            
            if author_name.lower() not in SUPER_USER:
                return _chat_handler(author_name, switch='AUTH')
            
            trade_author = command_args[4].strip('.')
            trade_symbol = command_args[0]
            hold_seconds = command_args[1]
            mod_value = trade_handler(tda_client, trade_author, trade_symbol, hold_seconds)
            
            return _chat_handler(trade_author, (trade_symbol, mod_value), switch='TRADE')
            
        timezone = pytz.timezone('US/Eastern')

        if datetime.now(timezone).hour >= 15:
            if datetime.now(timezone).hour >= 16:
                return _chat_handler(author_name, switch='CLOSED')
            if datetime.now(timezone).minute >= 40:
                return _chat_handler(author_name, switch='CLOSE')

        if not command_arg_one:
            return _chat_handler(author_name, switch='MISSING')
        
        if command_arg_one.lower() in {'list'}:
            return [', '.join(mongo_data_handler(operation='SYMBOLS'))]
            
        if not command_arg_two:
            return _chat_handler(author_name, switch='MISSING')
        
        trade_symbol = command_arg_one
        hold_seconds = command_arg_two
        
        if trade_symbol.upper() not in mongo_data_handler(operation='SYMBOLS'):
            return _chat_handler(author_name, trade_symbol, switch='SYMBOLS')
        
        try:
            hold_seconds = int(hold_seconds)
        except:
            return _chat_handler(author_name, switch='SECONDS')
        
        if hold_seconds not in range(9, 100):
            return _chat_handler(author_name, switch='SECONDS')

        if not mongo_data_handler(author_name, operation='BALANCE') > Decimal(1):
            return _chat_handler(author_name, switch='BALANCE')
        
        mongo_data_handler(author_name, (-1.00), operation='PLAYER_TOTAL')
        mongo_data_handler(author_name, (-1.00), operation='WIT_TOTAL')
        
        return _chat_handler(author_name, (trade_symbol, hold_seconds), switch='TRADE')
    
    if COMMAND_NAME in {'transfer'}:
        
        # transfer WIT to another player, 1 to ratio 0.1/0.01/0.9 (start/step/max)
        
        pass
    
    ###########################################################################
    # ABOUT, INFO, RULES
    ''' '''
    if COMMAND_NAME in {'about'}:
        
        # about  - LONG (DONE, fix though)
        
        return _chat_handler(author_name, switch='ABOUT')
    
    if COMMAND_NAME in {'info'}:
        
        # info   - SHORT (use current 3 rules)
        
        pass
    
    if COMMAND_NAME in {'rules'}:
        
        # rules  - build better set
        
        return _chat_handler(switch='RULES')
    
    ###########################################################################
    # BALANCE, VALUE, STATS
    ''' '''
    if COMMAND_NAME in {'balance'}:
        
        # balance       - return user balance 
        
        balance_return = mongo_data_handler(author_name, operation='BALANCE')
        return _chat_handler(author_name, balance_return, switch='BALANCE')
    
    if COMMAND_NAME in {'value'}:
        
        # value         - return current WIT value
        
        pass

    if COMMAND_NAME in {'stats'}:
        
        # stats         - generate some sort of stats to display
        
        pass
    
    ###########################################################################
    # COMMAND, POOL
    ''' '''
    if COMMAND_NAME in {'command'}:
        
        if not command_arg_one:
            return _chat_handler(author_name, 'command', switch='COMMAND')
        if command_arg_one:
            return _chat_handler(author_name, command_arg_one, switch='COMMAND')
    
    if COMMAND_NAME in {'pool'}:
        
        ###########################################################################
        # WIN, TRADE, TRANSFER, FOSS, MIC, AD, END, FACTORIO
        ''' POOL'''
        
        if {'win'}:
            
            # win       - 1 WIT (pool)     - increase the amount required to win the game by 0.1 WIT   
            
            pass
        
        if {'trade'}:
            
            # trade     - 1 WIT(pool)      - trigger random live trade, change modifier based on profit/loss
            
            pass
        
        if {'transfer'}:
            
            # transfer  - 1000 WIT (pool)  - increase the transfer amount by 0.01 WIT, 
            #                                reduce trigger by 10 (max transfer rate 0.9)
            
            pass
        
        if {'foss'}:
            
            # foss      - 1000 WIT   - release game code as free open sourece software
            
            pass

        if {'mic'}:
            
            # mic       - 1000 WIT   - turn mic on for remainder of game
            
            pass
        
        if {'ad'}:
            
            # ad        - 1000 WIT   - run an ad
            
            pass
        
        if {'end'}:
            
            # end       - 1000 WIT   - end the stream, no game winner, all WIT converts to TWIT
            
            pass
        
        if {'factorio'}:
            
            # factorio  - 1000 WIT   - play Factorio, end game, no winner, all WIT converts to TWIT
            
            pass

    ###########################################################################
    # commands to return the pool balance and trigger point
    # foss, mic, ad, end, factorio
    ''' COMMANDS'''
    
    if COMMAND_NAME in {'foss'}:
        
        # foss  - return foss pool balance and trigger point
        
        pass
    
    if COMMAND_NAME in {'mic'}:
        
        # mic   - return mic pool balance and trigger point
        
        pass
    
    if COMMAND_NAME in {'ad'}:
        
        # ad    - return ad pool balance and trigger point
        
        pass
    
    if COMMAND_NAME in {'end'}:
        
        # end   - return end pool balance and trigger point
        
        pass
    
    if COMMAND_NAME in {'factorio'}:
        
        # factorio  - return factorio pool balance and trigger point
        #             possible, spawn a whole new situation for FACTORIO
        #             naming of entities, figure out how to control game from chat, etc.
        
        pass
    
    # XXX: ADD new commands here <>
    
    if not COMMAND_NAME:
        return ['COMMAND_NAME not set, something went wrong']
    
    return ['end of chat_handler, something went wrong']

###############################################################################
# OUTPUT logic for commands as _chat_handler()
    
def _chat_handler(author_name=None, wit_ness=None, *, switch):
    
    ###########################################################################
    # misc, not specific to command or pool
    
    if switch in {'AUTH'}:
        return ['{author_name} you are not authorized to use that command.']
    
    ###########################################################################
    # win, trade, transfer (command/pool)
    ''' '''
    
    if switch in {'TRADE'}:
        if isinstance(wit_ness[1], Decimal128):
            return [f'{author_name}, after live trading {wit_ness[0]}, the new modifier is {wit_ness[1]}']
        if isinstance(wit_ness[1], int):
            return [f'~live_trade {wit_ness[0]} {wit_ness[1]} seconds for {author_name}.']
        
    if switch in {'CLOSED'}:
        return [f'{author_name}, no more trades, market is closed for the day.']
    
    if switch in {'CLOSE'}:
        return [f'{author_name}, no new trades, market is about to close.']
    
    if switch in {'MISSING'}:
        return [f'{author_name}, USE: !trade list or !trade <symbol> <seconds>']
    
    if switch in {'SYMBOLS'}:
        return [f'{author_name}, {wit_ness} is not in the list, try again']
    
    if switch in {'SECONDS'}:
        return [f'{author_name}, hold time must be a positive integer between 9 and 99']
    
    ###########################################################################
    # about, info, rules (command ONLY)
    ''' '''
    
    if switch in {'ABOUT'}:
        if not author_name.lower() in SUPER_USER:
            return [f'{author_name}: you are not authorized to use the about command.']

        return ['TWIT: The game of WITs. Buy WIT with earned channel ' +
        'points. The value of WIT fluctuates based on a modifier of 0.01 divided ' +
        'by the total number of WIT in the system. There are two ways to improve ' +
        'the value of WIT, spend them, or increase the modifier. This can be ' +
        'accomplished by activating the live stock trade bot, after which, the ' +
        'profit or loss will be added to the modifier.', 
        'Work together, pool your resources, and gain more WIT. The round starts ' +
        'when the first person makes the first purchase at a WIT value of 0.5. ' +
        'This deems them the `half-wit`, forever displaying their name and current ' +
        'WIT total as a standard of measure. Anyone that goes over the half-wit ' +
        'total WIT value also gets displayed, but as a nit-wit. Keep an eye on ' +
        'these people as they are about to end the game.', 
        'When the game is over, everyone reaches their wits-end and all WIT is ' +
        'converted to TWIT, accumulated by the twit_chart bot, useless, begging ' +
        'for a future purpose. The ultimate goal is to out-wit your opponents, ' +
        'collect as much WIT as possible, and claim one of two titles, GIFTED or ' +
        'TWIT CHAMP. The first title gets you a gifted sub to any channel on ' +
        'twitch, paid for by the host.',
        'The second title gives you control of the twit_champ bot, and comes with ' +
        'special abilities that can be used to influence the next round. Will you ' +
        'hack, cheat, and steal your way to a friends victory, or spread evenly ' +
        'the power you hold over the other players. Remember, you can only pick ' +
        'one title because this game does not afford you the opportunity of both ' +
        'money and power. Choose wisely, and dont be a dim-wit.']
    
    if switch in {'RULES'}:
        #create new rules, this is now info
        return ['Rule 1) Watch the stream to earn channel points.',
                'Rule 2) Invest your channel points in WIT.', 
                'Rule 3) TWIT takes WIT to play.']
    
    ###########################################################################
    # balance, value, stats
    ''' '''
    
    if switch in {'BALANCE'}:
        if wit_ness is None:
            return [f'{author_name}, you do not have enough WIT to make this trade.']
        return [f'{author_name} has {wit_ness} WIT']
    
    ###########################################################################
    # command, pool
    ''' '''
    
    if switch in {'COMMAND'}:
        # XXX: ADD new commands here <> UPDATE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if wit_ness.lower() not in {'!rules', 'rules', 
                                   '!command', 'command', 
                                   '!balance', 'balance',
                                   '!trade', 'trade', 
                                   '!pool', 'pool',
                                   '!foss', 'foss', 
                                   '!mic', 'mic',
                                   '!ad', 'ad',
                                   '!end', 'end',
                                   '!win', 'win',
                                   '!top', 'top',
                                   '!factorio', 'factorio'}:
            
            return [f'{author_name}, !{wit_ness} is not a command. TRY: !command for a list of valid commands.']
        
        if wit_ness.lower() in {'!command', 'command', '!commands', 'commands'}:
            # XXX: ADD new commands here <> UPDATE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return ['!rules, ' +
                    '!command, ' +
                    '!balance, ' +
                    '!trade, ' +
                    '!pool, ' +
                    '!foss, ' +
                    '!mic, ' +
                    '!ad, ' +
                    '!end, ' +
                    '!win, ' +
                    '!top, ' +
                    '!factorio', 
                    'USE: !command <command> for description.']
        if wit_ness.lower() in {'!balance', 'balance'}:
            return ['The balance command will show you your current WIT balance. ' + 
                    'Make sure you use your WIT as spending them will increase ' +
                    'their value. All unused WIT will be converted to TWIT at the ' +
                    'end of the game, also known as `wits-end`']
        if wit_ness.lower() in {'!trade', 'trade'}:
            return ['The trade command will live trade a stock and the P/L will be ' +
                    'added to the WIT modifier. Seconds are how long the position ' +
                    'is held and can be between 9 and 99. Trading with the trade ' +
                    'command cost 1 WIT. To see a list of tradable symbols type: ' +
                    '!trade list',
                    'To use the command type: !trade <symbol> <seconds>']
        if wit_ness.lower() in {'!pool', 'pool'}:
            return ['The pool command is a group effort triggering of certain actions. ' +
                    'An example of this would be the combined effort to make a trade. ' + 
                    'As the trade pool increases, once it reaches 1 WIT, it will ' +
                    'trigger. To see the list of available pools type: !pool list ',
                    'USE: !pool <pool type> <wit amount>']
        if wit_ness.lower() in {'!rules', 'rules'}:
            return ['The rules command will show you the rules of the game.']
        
        if wit_ness.lower() in {'!foss', 'foss'}:
            return ['foss return']
        if wit_ness.lower() in {'!mic', 'mic'}:
            return ['mic return']
        if wit_ness.lower() in {'!ad', 'ad'}:
            return ['ad return']
        if wit_ness.lower() in {'!end', 'end'}:
            return ['end return']
        if wit_ness.lower() in {'!win', 'win'}:
            return ['win return']
        if wit_ness.lower() in {'!top', 'top'}:
            return ['top return']
        if wit_ness.lower() in {'!factorio', 'factorio'}:
            return ['factorio return']
        # XXX: ADD new commands here <>
    
    ###########################################################################
    # foss, mic, ad, end, factorio
    ''' '''