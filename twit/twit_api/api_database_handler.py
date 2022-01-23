"""
- db_handler API. Anything connecting to the database goes here.

"""

from pymongo import MongoClient

# player_name

def mongo_data_handler(player_name=None, wit_ness=None, operation=None):
    ''' handle read/write of data to mongodb
    
    :param operation: 

    '''
    with MongoClient(tz_aware=True) as mongo_client:
        
        def get_wit_balance(player_name):
            '''return player WIT balance'''
            return mongo_client['twit_chart']['twit_champ'].find_one({'player':player_name})['WIT']
        
        def get_twit_balance(player_name):
            '''return player WIT balance'''
            return mongo_client['twit_chart']['twit_champ'].find_one({'player':player_name})['TWIT']
        
        def set_symbol_list(symbol_list):
            '''update the database with symbol list'''
            mongo_client["twit_chart"]["twit_data"].update_one({'document':'symbol_list'}, 
                                                               {'$set':{'symbol_list':symbol_list}})
            mongo_client["twit_chart"]["twit_data"].update_one({'document':'symbol_list'}, 
                                                               {'$set':{'symbol_count':len(symbol_list)}})
            return None
            
        def get_symbol_list():
            '''return the symbol list'''
            return mongo_client['twit_chart']['twit_data'].find_one({'document':'symbol_list'})['symbol_list']
        
        def get_wit_total():
            '''return the current wit total'''
            return mongo_client['twit_chart']['twit_data'].find_one({'document':'wit_mod'})['total_wit']
        
        def get_mod_total():
            '''return the current wit modifier'''
            return mongo_client['twit_chart']['twit_data'].find_one({'document':'wit_mod'})['modifier']
        
        def get_pool_list():
            '''return a list of pool available'''
            return ['trade', 'foss', 'mic', 'ad', 'end', 'win']
        
        #######################################################################
        # Operations
        
        if operation in {'BALANCE'}:
            return get_wit_balance(player_name)
        
        if operation in {'SYMBOLS'}:
            if isinstance(wit_ness, list):
                return set_symbol_list(wit_ness)
############# TODO: handle when the list is to big to go to chat (500 char)
            return get_symbol_list()
            
        if operation in {'PLAYER_TOTAL'}:
            if wit_ness is not None:
                wit_update = get_wit_balance(player_name) + wit_ness
                mongo_client["twit_chart"]["twit_champ"].update_one({'player':player_name}, {'$set':{'WIT':wit_update}})
            return get_wit_balance(player_name)
        
        if operation in {'WIT_TOTAL'}:
            if wit_ness is not None:
                wit_update = get_wit_total() + wit_ness
                mongo_client["twit_chart"]["twit_data"].update_one({'document':'wit_mod'}, {'$set':{'total_wit':wit_update}})
            return get_wit_total()
        
        if operation in {'MOD_TOTAL'}:
            if wit_ness is not None:
                mod_update = get_mod_total() + float(wit_ness)
                if mod_update < 0.01:
                    mod_update = 0.01
                mongo_client["twit_chart"]["twit_data"].update_one({'document':'wit_mod'}, {'$set':{'modifier':mod_update}})
            return get_mod_total()
        
        if operation in {'POOLS'}:
            return get_pool_list()
        
        if operation in {'TRADE'}:
            # update the trade pool
            return get_trade_pool()
        
        if operation in {'FOSS'}:
            # update the foss pool
            # update foss trigger
            # (pool, trigger)
            return get_foss_pool()
        
        if operation in {'MIC'}:
            # update the mic pool
            # update mic trigger
            # (pool, trigger)
            return get_mic_pool()
        
        if operation in {'AD'}:
            # update the ad pool
            # update ad trigger
            # (pool, trigger)
            return get_ad_pool()
        
        if operation in {'END'}:
            # update the yield pool
            # update yield trigger
            # (pool, trigger)
            return get_end_pool()
        
        if operation in {'WIN'}:
            # update the win pool
            # update win trigger
            # (pool, trigger)
            return get_win_pool()

  
        ''' 
        agg_result= list(mongo_client['twit_chart']['twit_champ'].aggregate(
            [{'$group': {'_id': '', 'total': { '$sum': '$WIT' }}
             }, {'$project': {'_id': 0, 'total': '$total'}
            }]))
        
        agg_result[0]['total']
                             
        twit_data = mongo_client['twit_chart']['twit_data'].find_one()
        
        agg_result = mongo_client['twit_chart']['twit_data'].aggregate(
            [{'$match':{}},
             {'$group' : {'_id': '$symbol', 'count':{'$sum':1}}}
             ])
        
        agg_result = mongo_client['twit_chart']['twit_data'].aggregate(
            [{'$match':{'timestamp': {'$gte': 111, '$lte': 777}}},
             {'$group' : {'_id': '$symbol', 'last_days_volume':{'$sum':'$volume'}}}
             ])       

          '''