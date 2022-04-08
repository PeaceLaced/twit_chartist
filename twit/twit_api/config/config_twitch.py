'''
- Settings for Twitch.
'''

##############################################################################
#######    Twitch Credentials, each bot has a unique set              ########
#######    --------------------------------------------------------   ########
##############################################################################

##############################################################################
###                                                                        ###
###   Data for                                                             ###
###                                                                        ###   
STREAM_ID = xxxxxxxx       # add streamers steam id here                   ###
STREAM_NAME = ''           # add streamers name here                       ###
ROOM_LIST = ['']           # add room for bots to join here                ###
SUPER_USER = {'', '', ''}  # add super users here                          ###
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_pubsub                                                ###
###   App Loc:                                                             ###
###   For Bot:  pubsub                                                     ###
###                                                                        ###
TWIT_PUBSUB_PORT = 8888                                                    ###
TWIT_PUBSUB_URI = 'http://localhost:' + str(TWIT_PUBSUB_PORT)              ###
TWIT_PUBSUB_SCOPES = 'channel:read:redemptions chat:edit chat:read'        ###
TWIT_PUBSUB_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                      ###
TWIT_PUBSUB_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                      ###
TWIT_PUBSUB_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_pubsub.json'
TWIT_PUBSUB_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_pubsub.json'
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_bot_chart                                             ###
###   App Loc:                                                             ###
###   For Bot:  twit_chart                                                 ###
###                                                                        ###
TWIT_CHART_PORT = 8887                                                     ###
TWIT_CHART_URI = 'http://localhost:' + str(TWIT_CHART_PORT)                ###
TWIT_CHART_SCOPES = 'chat:edit chat:read user:read:email'                  ###
TWIT_CHART_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_CHART_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_CHART_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_chart.json'
TWIT_CHART_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_chart.json'
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_bot_champ                                             ###
###   App Loc:                                                             ###
###   For Bot:  twit_champ                                                 ###
###                                                                        ###
TWIT_CHAMP_PORT = 8886                                                     ###
TWIT_CHAMP_URI = 'http://localhost:' + str(TWIT_CHAMP_PORT)                ###
TWIT_CHAMP_SCOPES = 'chat:edit chat:read'                                  ###
TWIT_CHAMP_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_CHAMP_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_CHAMP_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_champ.json'
TWIT_CHAMP_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_champ.json'
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_bot_chant                                             ###
###   App Loc:                                                             ###
###   For Bot:  twit_chant                                                 ###
###                                                                        ###
TWIT_CHANT_PORT = 8885                                                     ###
TWIT_CHANT_URI = 'http://localhost:' + str(TWIT_CHANT_PORT)                ###
TWIT_CHANT_SCOPES = 'chat:edit chat:read'                                  ###
TWIT_CHANT_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_CHANT_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_CHANT_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_chant.json'
TWIT_CHANT_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_chant.json'
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_bot_chalice                                           ###
###   App Loc:                                                             ###
###   For Bot:  twit_chalice                                               ###
###                                                                        ###
TWIT_ALICE_PORT = 8884                                                     ###
TWIT_ALICE_URI = 'http://localhost:' + str(TWIT_ALICE_PORT)                ###
TWIT_ALICE_SCOPES = 'chat:edit chat:read'                                  ###
TWIT_ALICE_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_ALICE_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_ALICE_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_alice.json'
TWIT_ALICE_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_alice.json'
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_bot_chamber                                           ###
###   App Loc:                                                             ###
###   For Bot:  twit_chamber                                               ###
###                                                                        ###
TWIT_AMBER_PORT = 8883                                                     ###
TWIT_AMBER_URI = 'http://localhost:' + str(TWIT_AMBER_PORT)                ###
TWIT_AMBER_SCOPES = 'chat:edit chat:read'                                  ###
TWIT_AMBER_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_AMBER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       ###
TWIT_AMBER_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_amber.json'
TWIT_AMBER_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_amber.json'
##############################################################################

##############################################################################
###                                                                        ###
###   App Name: twit_testv                                                 ###
###   App Loc:                                                             ###
###   For Bot:  NONE at the moment, this is for testing eventually         ###
###                                                                        ###
TWIT_TEST_PORT = 8882                                                      ###
TWIT_TEST_URI = 'http://localhost:' + str(TWIT_TEST_PORT)                  ###
TWIT_TEST_SCOPES = ('analytics:read:extensions analytics:read:games ' +    ###
                    'bits:read channel:edit:commercial ' +                 ###
                    'channel:manage:broadcast channel:manage:extensions ' +###
                    'channel:manage:polls channel:manage:predictions ' +   ###
                    'channel:manage:redemptions channel:manage:schedule ' +###
                    'channel:manage:videos channel:read:editors ' +        ###
                    'channel:read:goals channel:read:hype_train ' +        ###
                    'channel:read:polls channel:read:predictions ' +       ###
                    'channel:read:redemptions channel:read:stream_key ' +  ###
                    'channel:read:subscriptions clips:edit ' +             ###
                    'moderation:read moderator:manage:banned_users ' +     ###
                    'moderator:read:blocked_terms moderator:manage:blocked_terms ' +
                    'moderator:manage:automod moderator:read:automod_settings ' +
                    'moderator:manage:automod_settings moderator:read:chat_settings ' +
                    'moderator:manage:chat_settings user:edit ' +          ###
                    'user:manage:blocked_users user:read:blocked_users ' + ###
                    'user:read:broadcast user:read:email ' +               ###
                    'user:read:follows user:read:subscriptions' +          ###
                    'channel:moderate chat:edit chat:read ' +              ###
                    'whispers:read whispers:edit')                         ###
TWIT_TEST_CLIENT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                        ###
TWIT_TEST_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                        ###
TWIT_TEST_PATH_APP = 'twit/twit_api/config/bot_credentials/apptoken_test.json'
TWIT_TEST_PATH_USER = 'twit/twit_api/config/bot_credentials/usertoken_test.json'
##############################################################################
