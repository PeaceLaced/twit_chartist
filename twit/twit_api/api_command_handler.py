"""
- command functions API.

"""
import sys
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson.decimal128 import Decimal128, create_decimal128_context

from twit.twit_api.api_twitch_auth import validate_player
from twit.twit_api.config.config_twitch import SUPER_USER
from twit.twit_api.api_progress_handler import Progress as progress

from decimal import Decimal, Context, ROUND_HALF_EVEN, localcontext, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))
       
def toDecimal128(decimal_data):
    ''' used to convert back to decimal 128 for writing to database'''
    with localcontext(create_decimal128_context()) as ctx:
        return Decimal128(ctx.create_decimal(decimal_data))

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

def is_valid_player(valid_player):
    check_player = validate_player(valid_player)
    try:
        check_player['data'][0]['login']
        return True
    except:
        return False

def is_active_player(active_player):
    ''' see if the player is in the database'''
    with MongoClient(tz_aware=True) as mongo_client:
        player_data = mongo_client['twit_chartist']['twit_champ'].find_one(
            {f'{active_player}' : {'$exists':True}})
        if player_data is None:
            return False
        return player_data
    
def update_active_players(current_wit_value):
    ''' 
    update active players (players with play time)
    NOTE: this function also sets players to inactive
    '''
    update_total_wit = 0
    players_modified = 0
    with MongoClient(tz_aware=False) as mongo_client:
        # first, change all users who are expired to play_active false
        # then, update all play_active true with wit
        # 
        current_time = datetime.now()
        for document in mongo_client['twit_chartist']['twit_champ'].find():
            player_name = list(document.keys())[1]
            player_data = list(document.values())
            play_active = player_data[1]['play_active']
            play_until = player_data[1]['play_until']
            
            if play_active:
                if not play_until > current_time:
                    mongo_client['twit_chartist']['twit_champ'].update_one(
                        {f'{player_name}': {'$exists': True}},
                        {'$set': {f'{player_name}.play_active':False}}
                        )
                    
                if play_until > current_time:
                    update_total_wit = update_total_wit + current_wit_value
                    players_modified = players_modified + 1
                    mongo_client['twit_chartist']['twit_champ'].update_one(
                        {f'{player_name}': {'$exists':True}},
                        {'$inc': {f'{player_name}.WIT':toDecimal128(current_wit_value)}}
                        )
        #print(f'value:{current_wit_value}, round: {update_total_wit}, players:{players_modified}')   
        mongo_client['twit_chartist']['twit_chart'].update_one(
            {},
            {'$inc': {'WIT.total':toDecimal128(update_total_wit)}}
            )
        return (update_total_wit, players_modified)
                

        '''
        #######################################################################
        current_time = datetime.now()
        
        # start a total wit counter
        update_total_wit = 0
        updated_counter = 0
        
        # for document in mongo_client['twit_chartist']['twit_champ'].find():
        for document in mongo_client['twit_chartist']['twit_champ'].find():
            
            # only mess with play_active TRUE
            if play_active:
                # set play_active false for players who do not have time remaining
                    
                # add wit value for the rest   
                
                    # if we add wit to a player, add that value to update_total_wit
                    update_total_wit = update_total_wit + current_wit_value
                    updated_counter = updated_counter + 1
            # when all players are updated, write update_total_wit to total_wit
            
            return (update_total_wit, updated_counter)
                    
            # here is the tricky part. Adding to total_wit
            # how many players were added to
        #######################################################################     
        '''

def get_player_data(player, query_type=False):
    ''' query player data
    
    :return: player_data or False if player is not valid.
    '''
    # force all get_player_data calls to update and restart
    if not query_type:
        progress.e('update the get_player_data query_type to COMMAND or OTHER')
        input('UPDATE the program and restart it.')
        sys.exit()
     
    # false or data
    player_data = is_active_player(player)
    
    # anyone who issues a command (or pubsub convert) IS a valid user
    if query_type not in {'COMMAND'}:
        if not is_valid_player(player):
            return False
    
    # if they are not active, add them to the DB
    if not player_data:
        with MongoClient(tz_aware=True) as mongo_client:
            player_data = mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{player}' : {'$exists':True}}, 
                {'$set' : {f'{player}.WIT': Decimal128(Decimal('0.0')),
                           f'{player}.TWIT': Decimal128(Decimal('0.0')),
                           f'{player}.WIN': 0,
                           f'{player}.champ': False,
                           f'{player}.halfwit': False,
                           f'{player}.nitwit': False,
                           f'{player}.CHAN': 'None',
                           f'{player}.play_remaining': 0,
                           f'{player}.play_active': False,
                           f'{player}.play_until':datetime.strptime('1970-01-01T00:00', '%Y-%m-%dT%H:%M'),
                           f'{player}.play_total': 0,
                           f'{player}.guest':'None',
                           f'{player}.guests': [],
                           f'{player}.EMPTY': 'YO'}},
############################ XXX: add to player document here
                upsert=True,
                return_document=ReturnDocument.AFTER)
            progress.w(f'{player} has been granted access.')
    return player_data

def calc_play_time(play_active, play_until):
    '''
    strftime(format) creates a string from a datetime object

    datetime.strptime() creates a datetime object from a string
    
    using date object in mongo, it goes in as:
        datetime.strptime('1970-01-01T00:00', '%Y-%m-%dT%H:%M')
    '''
    if not play_active:
        calc_new_time = datetime.now() + timedelta(minutes=20)
        return calc_new_time
    
    if play_active:
        calc_new_time = play_until + timedelta(minutes=20)
        return calc_new_time

def update_player(player, update_data, /, update_type):
    ''' '''
    # be sure to pass positive or negative, and decimal
    with MongoClient(tz_aware=True) as mongo_client:
        
        if update_type in {'PURGE'}:
            
            # first remove player from purge_from_player's list
            purge_from_player = update_data
            purge_from_player_data = get_player_data(purge_from_player, query_type='COMMAND')
            purge_from_player_guest_list = purge_from_player_data[purge_from_player]['guests']
            purge_from_player_guest_list.remove(player)
            
            # crit purge to detect any abuse
            progress.crit(f'purge {player} from {purge_from_player} list.')
            
            mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{purge_from_player}' : {'$exists':True}},
                {'$set':{f'{purge_from_player}.guests':purge_from_player_guest_list}})
            
            return mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{player}' : {'$exists':True}},
                {'$set' : {f'{player}.guest': 'None'}},
                return_document=ReturnDocument.AFTER)[player]['guest']
        
        if update_type in {'TIME'}:
            update_play_until = update_data[0]
            channel_point_cost = update_data[1]
            progress.trace(f'{player}: add 20 min play time ({channel_point_cost})')
            mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{player}' : {'$exists':True}},
                {'$set' : {f'{player}.play_active':True,
                           f'{player}.play_until':update_play_until},
                 '$inc' : {f'{player}.play_total':20}})
        
        if update_type in {'GUEST'}:
            return mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{player}' : {'$exists':True}},
                {'$set' : {f'{player}.guest':update_data}},
                return_document=ReturnDocument.AFTER)[player]['guest']
        
######### TODO: TIL, figure this out with the $pull operator, then combine GUEST and GUEST_LIST
        if update_type in {'GUEST_LIST'}:
            return mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
                {f'{player}' : {'$exists':True}},
                {'$set' : {f'{player}.guests':update_data}},
                return_document=ReturnDocument.AFTER)[player]['guests']
        
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
            
            if command in {'LAST_GAME'}:
                is_last_game = get_game_data()['WIT']['last_game']
                if not is_last_game:
                    return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                        {},
                        {'$set':{
                            'WIT.last_game':True}},
                        return_document=ReturnDocument.AFTER)['WIT']['last_game']
                if is_last_game:
                    return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                        {},
                        {'$set':{
                            'WIT.last_game':False}},
                        return_document=ReturnDocument.AFTER)['WIT']['last_game']
            
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
        
        if update_type in {'POOL-WIT'}:
            update_to_total = toDecimal128(update_data)
            return mongo_client['twit_chartist']['twit_chart'].find_one_and_update(
                {},
                {'$set' : {f'POOL.{command}.total':update_to_total}},
                return_document=ReturnDocument.AFTER)['POOL'][f'{command}']['total'].to_decimal()
        
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
    
    
    # when we end the game, either by win or end, if last_game mode is active
    # what propigates to the next game
    # convert active player time to minutes/seconds remaining and store
    # TODO: (1)add time functionality

    with MongoClient(tz_aware=True) as mongo_client:
        
        # TODO (2)need future use for these pool dumps
        # get pools, write to db
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
                    # TODO: (3)possible change to 0.01 depending which way next phase pans
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
                    'WIT.pool':toDecimal128(update_game_end_pool),
                    'WIT.last_game':False},
                
                # these are increments
                '$inc' : {
                    'WIT.game': 1
                    }})
        
        # query all the player documents, get their name, wit for test
        for document in mongo_client['twit_chartist']['twit_champ'].find():
            player_name = list(document.keys())[1]
            player_data = list(document.values())
            player_wit = player_data[1]['WIT']
            
            # only zero players that have wit balance to reduce db calls
            if player_wit.to_decimal() > Decimal(0.0):
                mongo_client['twit_chartist']['twit_champ'].update_one(
                    {f'{player_name}' : {'$exists' : True}}, 
                    {
                        '$inc' : {f'{player_name}.TWIT':player_wit},
                        '$set' : {f'{player_name}.WIT': Decimal128(Decimal('0.0')),
                                  f'{player_name}.TWIT': Decimal128(Decimal('0.0')),
                                  f'{player_name}.WIN': 0,
                                  f'{player_name}.champ': False,
                                  f'{player_name}.halfwit': False,
                                  f'{player_name}.nitwit': False,
                                  f'{player_name}.CHAN': 'None',
                                  f'{player_name}.play_remaining': 0,
                                  f'{player_name}.play_active': False,
                                  f'{player_name}.play_until':datetime.strptime('1970-01-01T00:00', '%Y-%m-%dT%H:%M'),
                                  f'{player_name}.play_total': 0,
                                  f'{player_name}.guests': [],
                                  f'{player_name}.guest':'None',
                                  f'{player_name}.EMPTY': 'YO'}})
############################ XXX: add to player document here

        
        if end_type in {'WIN'}:
            
            winner = win_packet[0]
            win_choice = win_packet[1]
            
            # update the winner, win choice is the chan they pass for host list or gift sub
            mongo_client['twit_chartist']['twit_champ'].update_one(
                {f'{winner}' : {'$exists' : True}}, 
                {
                    '$set' : {
                        f'{winner}.CHAN':win_choice, 
                        f'{winner}.champ':True},
                    '$inc' : {
                        f'{winner}.WIN':1
                        }})
        return True