
#############################################
#Update specific fields of multiple documents
'''db.customers.update(
  {"firstname": "Max"},
  {
    $set: {
      "email": "p.maier@example.com"
    }
  },
  {"multi": true}
);
'''

# Database Examples
###############################################################################
# EXAMPLES, update(), update_one()

# set multiple values in same document
db.core_pid.update({"_id": current_id},
       {"$set": {
           "status": "Completed",
           "endtime": datetime.now(pytz.timezone('EST'))}})

mongo_client['twit_chartist']["twit_champ"].update_one({f'{player_name}' : {'$exists' : True}},
                                                       {'$set':{f'{player_name}.WIT':wit_update}})

mongo_client['twit_chartist']['twit_chart'].update_one({},
                                                       {'$set':{'WIT.modifier':mod_update}})

mongo_client['twit_chartist']['twit_chart'].update_one({}, {'$set':{'WIT.total':wit_update}})

###############################################################################
# EXAMPLES, find_one(), find_one_and_update()

mongo_client['twit_chartist']['twit_champ'].find_one_and_update(
    {f'{player}' : {'$exists':True}}, 
    {'$set' : {f'{player}.WIT':update_to_balance}},
    return_document=ReturnDocument.AFTER)[player]['WIT'].to_decimal()

db.example.find_one_and_update(
    {'_id': 'userid'},
    {'$inc': {'seq': 1}},
    return_document=ReturnDocument.AFTER)

twit_data = mongo_client['twit_chartist']['twit_chart'].find_one()

mongo_client['twit_chartist']['twit_champ'].find_one({f'{player_name}' : {'$exists' : True}})

mongo_client['twit_chartist']['twit_champ'].find_one({f'{player_name}' : {'$exists' : True}
                                                             })[player_name]['WIT']

mongo_client['twit_chartist']['twit_champ'].find_one({f'{player_name}' : {'$exists' : True}
                                                             })[player_name]['TWIT']

###############################################################################
# EXAMPLES, aggregate()

agg_result= list(mongo_client['twit_chartist']['twit_champ'].aggregate(
    [{'$group': {'_id': '', 'total': { '$sum': '$WIT' }}
     }, {'$project': {'_id': 0, 'total': '$total'}
    }]))
agg_result[0]['total']

agg_result = mongo_client['twit_chartist']['twit_chart'].aggregate(
    [{'$match':{}},
     {'$group' : {'_id': '$symbol', 'count':{'$sum':1}}}
     ])

agg_result = mongo_client['twit_chartist']['twit_chart'].aggregate(
    [{'$match':{'timestamp': {'$gte': 111, '$lte': 777}}},
     {'$group' : {'_id': '$symbol', 'last_days_volume':{'$sum':'$volume'}}}
     ])       

db.collection.aggregate([{$match: {"project_id": "1","type": "Description"}},{$count: "count"}])

###############################################################################
# does not work
current_players = mongo_client['twit_chartist']['twit_champ'].count_documents({'WIT':{'$gt':0}})
