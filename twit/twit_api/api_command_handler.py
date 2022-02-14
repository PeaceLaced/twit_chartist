"""
- command functions API.

"""
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson.decimal128 import Decimal128, create_decimal128_context

from twit.twit_api.config.config_twitch import SUPER_USER
from twit.twit_api.api_progress_handler import Progress as progress

from decimal import Context, setcontext, localcontext, Decimal, BasicContext
setcontext(BasicContext)
        
def toDecimal128(decimal_data):
    ''' used to convert back to decimal 128 for writing to database'''
    with localcontext(create_decimal128_context()) as ctx:
        return Decimal128(ctx.create_decimal(decimal_data))

# TODO: after chatter check, if None, try API call for twitch wide check before False
'''https://dev.twitch.tv/docs/v5/reference/users'''
def is_valid_chatter(self, chatter):
    ''' see if the user has a channel, valid channel = valid user'''
    chatter_test = self.get_channel('peacelaced').get_chatter(chatter)
    if chatter_test is None:
        return False
    return True

def is_valid_chan(self, chan):
    chan_test = self.get_channel(chan)
    if chan_test is None:
        return False
    return True

def get_player_count(count_type='total'):
    ''' return either total players over all or current players'''
    with MongoClient(tz_aware=True) as mongo_client:
        if count_type in {'current'}:
            current_player_count = 0
            for document in mongo_client['twit_chartist']['twit_champ'].find():
                player_data = list(document.values())
                player_wit = player_data[1]['WIT'].to_decimal()
                if player_wit > 0:
                    current_player_count += 1
            return current_player_count
        if count_type in {'total'}:
            return mongo_client['twit_chartist']['twit_champ'].count_documents({})

def get_game_data():
    ''' return the full game data object'''
    with MongoClient(tz_aware=True) as mongo_client:
        game_data = mongo_client['twit_chartist']['twit_chart'].find_one()
        return game_data
    
def is_SUPERUSER(player):
    ''' '''
    if player not in SUPER_USER:
        return False
    return True  

def is_USER(player):
    ''' return player data, call twice if new player'''
    # look into calling a function within itself to compress this and get_player_data()
    player_data = get_player_data(player)
    if player_data is None:
        player_data = get_player_data(player)
    return player_data

def get_player_data(player):
    ''' query player data, add player if None'''
    
    with MongoClient(tz_aware=True) as mongo_client:
        player_data = mongo_client['twit_chartist']['twit_champ'].find_one({f'{player}' : {'$exists' : True}})
        if player_data is None:
            mongo_client['twit_chartist']['twit_champ'].insert_one(
                {f'{player}':{'WIT': Decimal128(Decimal('0.0')),
                              'TWIT': Decimal128(Decimal('0.0')),
                              'WIN': 0,
                              'champ': False,
                              'halfwit':False,
                              'nitwit':False,
                              'CHAN':'None'}})
            progress.w(f'{player} has been granted access.')
            return None
        return player_data

def update_player(player, update_data, /, update_type):
    ''' '''
    # be sure to pass positive or negative, and decimal
    with MongoClient(tz_aware=True) as mongo_client:
        
        # TIME, TIMER, something for the time loop
        if update_type in {'TIME'}:
            pass
        
        # update player wit balance, pass calc only of decimal/decimal ($inc does not work)
        if update_type in {'PLAYER-WIT'}:
            update_to_balance = toDecimal128(update_data)
            return mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{player}' : {'$exists':True}}, 
                {'$set' : {f'{player}.WIT':update_to_balance}},
                return_document=ReturnDocument.AFTER)[player]['WIT'].to_decimal()
    
def update_game(command, update_data, /, update_type):
    ''' 
    When updating the database, perform calculations then use $set
    Tried $inc but continued to get floating point precision errors 
    Converting all Decimal128, may need to do INT/FLOAT as well, TBD.
    '''
    
    with MongoClient(tz_aware=True) as mongo_client:
        #######################################################################
        # command specific updates
        
        if update_type in {'COMMAND'}:
            
            # transfer ratio is D128, transfer trigger is INT
            if command in {'TRANSFER'}:
                # update_data = (update_ratio, update_trigger)
                transfer_ratio = toDecimal128(update_data[0])
                transfer_trigger = int(update_data[1])
                return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                    {},
                    {'$set' : {
                        'WIT.transfer':transfer_ratio,
                        'POOL.TRANSFER.trigger':transfer_trigger}},
                    return_document=ReturnDocument.AFTER)
            
            # win trigger is D128, system wit is D128
            if command in {'WIN'}:
                # update_data = (update_trigger, update_wit)
                update_win_trigger = toDecimal128(update_data[0])
                update_total_balance = toDecimal128(update_data[1])
                return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                    {},
                    {'$set' : {
                        'WIT.win':update_win_trigger,
                        'WIT.total':update_total_balance}},
                    return_document=ReturnDocument.AFTER)['WIT']['win'].to_decimal()
            
            # end trigger is INT
            if command in {'END'}:
                update_end_trigger = int(update_data)
                return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                    {},
                    {'$set' : {
                        'POOL.END.trigger':update_end_trigger}},
                    return_document=ReturnDocument.AFTER)['POOL']['END']['trigger']
        
        #######################################################################
        # type specific updates
        
        # is Decimal128, changed from $inc to $set, writing a calculation
        if update_type in {'POOL-WIT'}:
            update_to_total = toDecimal128(update_data)
            return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                {},
                {'$set' : {f'POOL.{command}.total':update_to_total}},
                return_document=ReturnDocument.AFTER)['POOL'][f'{command}']['total'].to_decimal()
        
        # app.py???
        if update_type in {'SYSTEM-WIT'}:
            update_to_balance = toDecimal128(update_data)
            return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                {},
                {'$set' : {'WIT.total':update_to_balance}},
                return_document=ReturnDocument.AFTER)['WIT']['total'].to_decimal()
        
        if update_type in {'MODIFIER'}:
            update_to_modifier = toDecimal128(update_data)
            return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                {},
                {'$set' : {'WIT.modifier':update_to_modifier}},
                return_document=ReturnDocument.AFTER)
        
        if update_type in {'SYMBOL-LIST'}:
            symbol_list = update_data
            mongo_client['twit_chartist']['twit_chart'].update_one(
                {},
                {'$set' : {
                    'SYMBOL.list':symbol_list, 
                    'SYMBOL.count':len(symbol_list)}})
            return None
        
def end_game(win_packet, /, end_type='WIN'):

    with MongoClient(tz_aware=True) as mongo_client:
        
        game_data = get_game_data()
        p_trade = game_data['POOL']['TRADE']['total'].to_decimal()
        p_transfer = game_data['POOL']['TRANSFER']['total'].to_decimal()
        p_win = game_data['POOL']['WIN']['total'].to_decimal()
        p_foss = game_data['POOL']['FOSS']['total'].to_decimal()
        p_mic = game_data['POOL']['MIC']['total'].to_decimal()
        p_ad = game_data['POOL']['AD']['total'].to_decimal()
        p_end = game_data['POOL']['END']['total'].to_decimal()
        p_factorio = game_data['POOL']['FACTORIO']['total'].to_decimal()
        current_wit_pool = game_data['WIT']['pool'].to_decimal()
        
        pool_acc = p_trade + p_transfer + p_win + p_foss + p_mic + p_ad + p_end + p_factorio
        update_game_end_pool = current_wit_pool + pool_acc
        
        # update the game
        mongo_client['twit_chartist']['twit_chart'].update_one(
            {}, 
            {
                # these are resets
                '$set' : {
                    'WIT.total':Decimal128(Decimal('0.0')),
                    # TODO: possible change to 0.01 depending which way next phase pans
                    'WIT.modifier':Decimal128(Decimal('0.1')),
                    'WIT.transfer':Decimal128(Decimal('0.1')),
                    'WIT.win':Decimal128(Decimal('10.0')),
                    'POOL.TRANSFER.trigger':int(1000),
                    'POOL.TRADE.total':Decimal128(Decimal('0.0')),
                    'POOL.TRANSFER.total':Decimal128(Decimal('0.0')),
                    'POOL.WIN.total':Decimal128(Decimal('0.0')),
                    'POOL.FOSS.total':Decimal128(Decimal('0.0')),
                    'POOL.MIC.total':Decimal128(Decimal('0.0')),
                    'POOL.AD.total':Decimal128(Decimal('0.0')),
                    'POOL.END.total':Decimal128(Decimal('0.0')),
                    'POOL.END.trigger':int(1000),
                    'POOL.FACTORIO.total':Decimal128(Decimal('0.0')),
                    'WIT.pool':toDecimal128(update_game_end_pool)},
                
                # these are increments
                '$inc' : {
                    'WIT.game': 1
                    }})
        
        # update all the players
        for document in mongo_client['twit_chartist']['twit_champ'].find():
                
            player_name = list(document.keys())[1]
            
            player_data = list(document.values())
            player_wit = player_data[1]['WIT']
            
            if player_wit.to_decimal() > Decimal(0.0):
                mongo_client['twit_chartist']['twit_champ'].update_one(
                    {f'{player_name}' : {'$exists' : True}}, 
                    {
                        '$inc' : {
                            f'{player_name}.TWIT':player_wit
                            },
                        '$set' : {
                            f'{player_name}.WIT':Decimal128(Decimal('0.0')),
                            f'{player_name}.CHAN':'None',
                            f'{player_name}.champ':False,
                            f'{player_name}.halfwit':False,
                            f'{player_name}.nitwit':False},
                        })
        
        if end_type in {'WIN'}:
            
            winner = win_packet[0]
            win_choice = win_packet[1]
            
            # update the winner
            mongo_client['twit_chartist']['twit_champ'].update_one(
                {f'{winner}' : {'$exists' : True}}, 
                {
                    '$set' : {
                        f'{winner}.CHAN':win_choice, 
                        f'{winner}.champ':True},
                    '$inc' : {
                        f'{winner}.WIN':1
                        }})
        # TODO: catch errors and return false or something
        return True