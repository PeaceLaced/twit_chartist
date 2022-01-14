"""
- Game Bot API.

"""

from twit.mongo_db.api_mongo_db import mongo_data_handler
    
def chat_handler(author_name, message_content):
    '''check command input, format return strings, call other handlers'''
    
    message_content = message_content.split(' ')
    if message_content[0] in {'!about'}:
        about_message = ['TWIT: The game of WITs. Buy WIT with earned channel ' +
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
        return about_message
    
    if message_content[0] in {'!command'}:
        if len(message_content) in {1}:
            return command_list_handler(message_content[0])
        if len(message_content) > 1:
            return command_list_handler(message_content[1])
        
    if message_content[0] in {'!balance'}:
        champ_data = champ_handler(author_name, None, action_type='READ')
        return f'{author_name} has {champ_data["WIT"]} WIT'
        
    if message_content[0] in {'!trade'}:
        if message_content[1].upper() not in mongo_data_handler(None, None, operation='SYMBOL_LIST'):
            return 'the symbol you selected is not in the list, try again'
        try:
            hold_seconds = int(message_content[2])
        except:
            return f'{author_name}, hold time must be a positive integer between 9 and 99'
        if hold_seconds not in range(9, 100):
            return f'{author_name}, hold time must be a positive integer between 9 and 99'
        
######### TODO: manage the remainder of this block <>
        handle_champ = champ_handler(author_name, wit_ness=1, action_type='WRITE')
        handle_wit = wit_handler()
        return trade_handler(author_name)
        
    if message_content[0] in {'!pool'}:
        if message_content[1].upper() not in mongo_data_handler(None, None, operation='POOL_LIST'):
            return f'{author_name}, that pool type does not exist, please try again'
        champ_data = champ_handler(author_name, None, action_type='READ')
        try:
            wit_for_pool = float(message_content[2])
        except:
            return f'{author_name}, WIT amount needs to be a positive float'
        if float(champ_data['WIT']) < float(message_content[2]):
            return f'{author_name}, you do not have enough WIT for this task'

######### TODO: manage the remainder of this block <>
        handle_champ = champ_handler(author_name, message_content[2], action_type='WRITE')
        handle_wit = wit_handler()
        return pool_handler(author_name)

def command_list_handler(a_command):
    '''gives a description of each command,  examples, use cases, etc.
    
    when adding a new command, there are three updates needed, see XXX.

    :return: LIST, always return a list
    '''
##### TODO: find a better way to do this, having to remember to add commands here will be annoying <>
##### TODO: possible need to make these all on the same line instead of separate post per <>

    # XXX: ADD new commands here <>
    if a_command.lower() not in {'!command', 'command', 
                               '!balance', 'balance',
                               '!trade', 'trade', 
                               '!pool', 'pool'
                               }:
        return ['invalid command', 'try: !command trade']
    
    if a_command.lower() in {'!command', 'command'}:
        # XXX: ADD new commands here <>
        return ['!about, !command, !balance, !trade, !pool', 'USE: !command <command> for description.']
    if a_command.lower() in {'!balance', 'balance'}:
        return ['The balance command will show you your current WIT balance.', 
                'Make sure you use your WITs, at the end they convert to TWITs.']
    if a_command.lower() in {'!trade', 'trade'}:
        return ['The trade command will live trade a stock. The P/L will be added to the WIT modifier.',
                'See the list of available symbols with the command: !trade list',
                'Seconds are how long the position is held before selling. Choose between 9 and 99.',
                'Trading with the trade command cost 1 WIT.',
                'USE: !trade <symbol> <seconds>']
    if a_command.lower() in {'!pool', 'pool'}:
        return ['The pool command is a group effort triggering of certain actions.',
                'See the list of available pools with the command: !pool list',
                'An example of this would be the combined effort to make a trade. ' + 
                'As the trade pool increases, once it reaches 1 WIT, it will trigger.',
                'USE: !pool <pool type> <wit amount>']
    # XXX: ADD new commands here <>
    
def champ_handler(author_name, wit_ness, action_type):
    '''champ handler will deal with reading and writing to the user document in DB'''
    
    # call the champ data, then do something with it (return or modify)
    champ_data = mongo_data_handler(author_name, wit_ness, 'CHAMP_' + action_type)
    if action_type in {'READ'}:
        return champ_data
        
    if action_type in {'WRITE'}:
        return 'write data to DB (increase/decrease wit/twit)'
    
    if action_type in {'WIT_CHECK'}:
        return champ_data['WIT']

def wit_handler():
    '''handle main wit value and modifier here'''

def trade_handler(author_name):
    '''handle the trades'''
    
    return f'{author_name} is trading SYMBOL for SECONDS seconds to try and increase the WIT gain modifier'

def pool_handler(author_name):
    '''handle the pools'''
    
    return f'{author_name} is adding WIT wit to the POOL pool, POOL pool now contains WIT wit, it needs WIT wit to trigger'





""" 
def chat_handler_commands():
    '''
    
    '''
    chat_data = ctx.message.content.split(' ')
    if chat_data[0] in {'!commands'}:
def chat_handler_balance(pool, wit):
    ''' modifies a pool by wit value
    
    :param pool: selects the pool to moidify
    :param wit: modifies pool by wit amt
    
    return None
    '''
    balance = mongo_data_handler(ctx.author.name, None, operation='BALANCE') 
    await ctx.send(f'{ctx.author.name}: {balance}')
    
    
def chat_handler_pool(pool, wit):
    ''' modifies a pool by wit value
    
    :param pool: selects the pool to moidify
    :param wit: modifies pool by wit amt
    
    return None
    '''
    chat_data = ctx.message.content.split(' ')
    if chat_data[0] in {'!pool'}:
        
        
            
        mongo_data_handler(ctx.author.name, (chat_data[1], chat_data[2]), operation='POOL')
    await ctx.send(f'Adding {chat_data[2]} WIT to {chat_data[1]} pool for {ctx.author.name}')
    
    if pool in {'trade'}:
        # trade pool will build up, then trade a stock
        # the profit/loss will increase/decrease the modifier
        
        # make trade
        # write to modifier db entry

        pass
    
    
    
    # generate a list of different pools and pass them here
    if not chat_data[1] in {'trade'}:
        
        if chart_data[]
        
        if not isinstance(chart_data[2], float)
        
"""