"""
- MongoDB API.

"""

from pymongo import MongoClient
#from twit.game_bot.api_game_bot import modify_pool
from twit.progress_report.api_progress_report import Progress as progress

# this is going to be a function that we open and call
# pass data to it, have it save, and be done
        
def mongo_data_handler(champ, wit_ness, operation):
    ''' handle read/write of data to mongodb
    
    :param operation: CHAMP_READ   - read champ data only
                      CHAMP_WRITE  - write data to champ
                      
                      other options: WRITE_WIT  - write/update WIT data
                                     WRITE_TWIT - write/update TWIT data
                                     WITS_END   - returns current wit value
                                     BALANCE    - get users balance
                                     POOL       - all the pool operations, may breakout
                                     
                                     
                                     DELETE - delete data
                                     CLEAR  - clear data
                                     DROP   - drop all collections (for testing)
                                     INITIAL - some initial db settings (for testing)
                                     
    if we modify single value total, every call will have to write there
    otherwise we aggregate like current, though at a cost of speed see: WITS_END TODO
    
    return YES
    '''
    # MongoClient is always open. Allows us to write to DB everywhere.
    # use mongo_client.database[collection][collection].insert_one(data)
    with MongoClient(tz_aware=True) as mongo_client:
        
        def get_symbol_list():
            '''
            make a call to the database and return a list of symbols we are trading
            
            TESTING with symbol list containing AMC, GME
            '''
            return ['AMC', 'GME']
        
        def get_pool_list():
            '''
            return a list of pool available
            '''
            return ['TRADE', 'GIFTED']
        
        def get_champ_data(champ):
            return mongo_client['twit_chart']['twit_champ'].find_one({'champ':champ})
        
        def modify_champ_wit(champ, wit_ness):
            modification = 'modify champ WIT balance'
            return modification
        
        def modify_champ_twit(champ, wit_ness):
            modification = 'modify champ TWIT balance'
            return modification

        if operation in {'SYMBOL_LIST'}:
            return get_symbol_list()
        
        if operation in {'POOL_LIST'}:
            return get_pool_list()
        
        champ_data = get_champ_data(champ)
        
        if operation in {'CHAMP_READ'}:
            '''return champ data'''
            return champ_data
        
        if operation in {'CHAMP_WRITE'}:
            '''
            write champ data
            '''
            
        
        '''       

        # (pool_type, wit_amt)
        if operation in {'POOL'}:
            
            # we need to catch errors, if pool does not exist,
            # or balance is too low, it does not process
            
            # modify pool
            modify_pool(wit_ness[0], wit_ness[1])
            progress.s('POOL_UPDATED_(added ' + str(wit_ness[1]) + ' WIT to ' + wit_ness[0] + ')')
            
            # reduce user balance
            champ_data = get_champ_data(champ)
            mongo_client["twit_chart"]["twit_champ"].update_one({'champ':champ}, {'$set':{'WIT':champ_data['WIT'] - float(wit_ness[1])}})
            progress.s('WIT_UPDATED_(removed ' + str(wit_ness[1]) + ' WIT from ' + champ + ')')
        
        # get WIT balance
        if operation in {'BALANCE'}:
            champ_data = get_champ_data(champ)
            if not champ_data:
                champ_data = 'You have no WITs'
            else:
                champ_data = f"WIT: {champ_data['WIT']}"
            return (champ_data)
        
        # add WIT to user
        if operation in {'WRITE_WIT'}:
            champ_data = get_champ_data(champ)
            if champ_data is None:
                mongo_client['twit_chart']['twit_champ'].insert_one({'champ':champ, 'WIT':wit_ness, 'TWIT':0})
                progress.trace('CHAMP_ADDED_(add ' + str(wit_ness) + ' WIT to ' + champ + ')')
            if champ_data:
                mongo_client["twit_chart"]["twit_champ"].update_one({'WIT':champ_data['WIT']}, {'$set':{'WIT':champ_data['WIT'] + wit_ness}})
                progress.s('WIT_UPDATED_(add ' + str(wit_ness) + ' WIT to ' + champ + ')')
            champ_data = get_champ_data(champ)
            return (champ_data['champ'], champ_data['WIT'])
        
        # WRITE_TWIT will only be called when someone becomes GIFTED
        # convert all WIT to TWIT here
        if operation in {'WRITE_TWIT'}:
            champ_data = get_champ_data(champ)
            if champ_data:
                mongo_client["twit_chart"]["twit_champ"].update_one({'TWIT':champ_data['TWIT']}, {'$set':{'TWIT':champ_data['TWIT'] + wit_ness}})
                progress.s('TWIT_UPDATED_(add ' + str(wit_ness) + ' TWIT to ' + champ + ')')
            
            # get the data again, with update values and return (champ, wit)
            champ_data = get_champ_data(champ)
            return (champ_data['champ'], champ_data['TWIT'])

        if operation in {'WITS_END'}:
            agg_result= list(mongo_client['twit_chart']['twit_champ'].aggregate(
                [{'$group': {'_id': '', 'total': { '$sum': '$WIT' }}
                 }, {'$project': {'_id': 0, 'total': '$total'}
                }]))
            
            if not agg_result:
                agg_data = 0
                
            if agg_result:
                agg_data = agg_result[0]['total']
                     
            twit_data = mongo_client['twit_chart']['twit_data'].find_one()
############# TODO: turn agg_result inot twit_data['total_wit']
            return (agg_data, twit_data['modifier'])
        
        ##########################################################################################################
        ##########                USED FOR TESTING                     ###########################################
        ##########################################################################################################
        if operation in {'INITIAL'}:
            mongo_client['twit_chart']['twit_data'].insert_one({'total_wit':wit_ness[0], 'modifier':wit_ness[1]})

        if operation in {'DROP'}:
            mongo_client['twit_chart'].drop_collection()
            progress.s('DROP_COLLECTION')
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        '''
'''            

    agg_result = mongo_client[each_database]['minute_candles'].aggregate(
        [{'$match':{'timestamp': {'$gte': use_this_in_greaterthan, '$lte': use_this_in_lessthan}}},
         {'$group' : {'_id': '$symbol', 'last_days_volume':{'$sum':'$volume'}}}
         ])
    
    # crate a tuple (symbol, volume)
    for i in agg_result:
        vol_data.append((i['_id'], i['last_days_volume']))

############################################################################################
# aggregate and count minute_candle documents for every symbol in the database
count_data = []
for each_database in tqdm(databases_only, desc='AGGREGATING_DATA'):
    agg_result = mongo_client[each_database]['minute_candles'].aggregate(
        [{'$match':{}},
         {'$group' : {'_id': '$symbol', 'count':{'$sum':1}}}
         ])
    
    # crate a tuple (symbol, count)
    for i in agg_result:
        count_data.append((i['_id'], i['count']))
        
        '''
        
'''
from pymongo import MongoClient 
    
# creation of MongoClient 
client=MongoClient() 
    
writer_profiles = [
    {"_id":1, "user":"Amit", "title":"Python", "comments":8},
    {"_id":2, "user":"Drew",  "title":"JavaScript", "comments":15},
    {"_id":3, "user":"Amit",  "title":"C++", "comments":6},
    {"_id":4, "user":"Drew",  "title":"MongoDB", "comments":2},
    {"_id":5, "user":"Cody",  "title":"MongoDB", "comments":16}]
  
client['database4']['myTable'].insert_many(writer_profiles)

agg_result= client['twit_chart']['twit_champ'].aggregate(
    [{
    "$group" : 
        {"_id" : "$WIT",  
         "total" : {"$sum" : 1}
         }}
    ])
for i in agg_result:
    print(i)
    
    '''