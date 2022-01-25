"""
- db_handler API. Anything connecting to the database goes here.

"""

from pymongo import MongoClient

# decimal cast at calculation
from decimal import Decimal, localcontext
from bson.decimal128 import Decimal128, create_decimal128_context

# TODO: OPERATIONS:SYMBOL handle when the list is to big to go to chat (500 char)

def mongo_data_handler(player_name=None, wit_ness=None, *, operation=None):
    ''' handle read/write of data to mongodb'''
    
    with MongoClient(tz_aware=True) as mongo_client:
        
        #######################################################################
        # FUNCTIONS block header
        
        #######################################################################
        # MISC, not specific to any command/pool
        
        def toDecimal128(decimal_data):
            ''' used to convert back to decimal 128 for writing to database'''
            with localcontext(create_decimal128_context()) as ctx:
                return Decimal128(ctx.create_decimal(decimal_data))
            
        def get_wit_balance(player_name):
            '''return player WIT balance'''
            return mongo_client['twit_chartist']['twit_champ'].find_one()[player_name]['WIT']

        def get_twit_balance(player_name):
            '''return player WIT balance'''
            return mongo_client['twit_chartist']['twit_champ'].find_one()[player_name]['TWIT']
        
        def get_wit_total():
            '''return the current wit total'''
            return mongo_client['twit_chartist']['twit_chart'].find_one()['WIT']['total']
        
        def get_mod_total():
            '''return the current wit modifier'''
            return mongo_client['twit_chartist']['twit_chart'].find_one()['WIT']['modifier']
        
        #######################################################################
        # WIN, TRADE, TRANSFER
        
        def get_symbol_count():
            ''' get current symbol count'''
            return mongo_client['twit_chartist']['twit_chart'].find_one()['SYMBOL']['count']
        
        def get_symbol_list():
            '''return the symbol list'''
            return mongo_client['twit_chartist']['twit_chart'].find_one()['SYMBOL']['list']
        
        def set_symbol_list(symbol_list):
            '''update database with the symbol list'''
            mongo_client['twit_chartist']['twit_chart'].update_one({'SYMBOL.list':get_symbol_list()},
                                                                   {'$set':{'SYMBOL.list':symbol_list}})
            mongo_client['twit_chartist']['twit_chart'].update_one({'SYMBOL.count':get_symbol_count()}, 
                                                                   {'$set':{'SYMBOL.count':len(symbol_list)}})
            return None
        
        #######################################################################
        # ABOUT, INFO, RULES
        
        
        #######################################################################
        # BALANCE, VALUE, STATS
        
        
        #######################################################################
        # COMMAND, POOL
        
        def get_pool_list():
            '''return a list of pool available'''
            return ['trade', 'foss', 'mic', 'ad', 'end', 'win']
        
        #######################################################################
        # FOSS, MIC, AD, END, FACTORIO


        #######################################################################
        # OPERATIONS block header
        ''' '''

        if operation in {'BALANCE'}:
            return get_wit_balance(player_name).to_decimal()
        
        if operation in {'SYMBOLS'}:
            if isinstance(wit_ness, list):
                # OPERATIONS:SYMBOL, TODO reference
                return set_symbol_list(wit_ness)
            return get_symbol_list()
            
        if operation in {'PLAYER_TOTAL'}:
            if wit_ness:
                wit_update = toDecimal128(get_wit_balance(player_name).to_decimal() + Decimal(wit_ness))
                mongo_client['twit_chartist']["twit_champ"].update_one({f'{player_name}.WIT':get_wit_balance(player_name)},
                                                                       {'$set':{f'{player_name}.WIT':wit_update}})
            return get_wit_balance(player_name)
        
        if operation in {'WIT_TOTAL'}:
            if wit_ness:
                wit_update = toDecimal128(get_wit_total().to_decimal() + Decimal(wit_ness))
                mongo_client['twit_chartist']['twit_chart'].update_one({'WIT.total':get_wit_total()}, 
                                                                       {'$set':{'WIT.total':wit_update}})
            return get_wit_total()
        
        if operation in {'MOD_TOTAL'}:
            if wit_ness:
                mod_update = get_mod_total().to_decimal() + Decimal(wit_ness)
                if mod_update < Decimal(0.01):
                    mod_update = Decimal(0.01)
                mod_update = toDecimal128(mod_update)
                mongo_client['twit_chartist']['twit_chart'].update_one({'WIT.modifier':get_mod_total()}, 
                                                                       {'$set':{'WIT.modifier':mod_update}})
            return get_mod_total()
        
        if operation in {'POOLS'}:
            return get_pool_list()
        
        if operation in {'TRADE'}:
            # update the trade pool
            return #get_trade_pool()
        
        if operation in {'FOSS'}:
            if wit_ness:
                
                pass
            # update the foss pool
            # update foss trigger
            # (pool, trigger)
            return #get_foss_pool()
        
        if operation in {'MIC'}:
            # update the mic pool
            # update mic trigger
            # (pool, trigger)
            return #get_mic_pool()
        
        if operation in {'AD'}:
            # update the ad pool
            # update ad trigger
            # (pool, trigger)
            return #get_ad_pool()
        
        if operation in {'END'}:
            # update the yield pool
            # update yield trigger
            # (pool, trigger)
            return #get_end_pool()
        
        if operation in {'WIN'}:
            # update the win pool
            # update win trigger
            # (pool, trigger)
            return #get_win_pool()

        #######################################################################
        # EXAMPLES, database access
        ''' 
        agg_result= list(mongo_client['twit_chartist']['twit_champ'].aggregate(
            [{'$group': {'_id': '', 'total': { '$sum': '$WIT' }}
             }, {'$project': {'_id': 0, 'total': '$total'}
            }]))
        
        agg_result[0]['total']
                             
        twit_data = mongo_client['twit_chartist']['twit_chart'].find_one()
        
        agg_result = mongo_client['twit_chartist']['twit_chart'].aggregate(
            [{'$match':{}},
             {'$group' : {'_id': '$symbol', 'count':{'$sum':1}}}
             ])
        
        agg_result = mongo_client['twit_chartist']['twit_chart'].aggregate(
            [{'$match':{'timestamp': {'$gte': 111, '$lte': 777}}},
             {'$group' : {'_id': '$symbol', 'last_days_volume':{'$sum':'$volume'}}}
             ])       

          '''