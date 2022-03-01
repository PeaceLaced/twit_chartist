#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue 11 Jan 13:07:45 2022

- NOTICE:
    - for educational purposes only
    - not financial advice

- SUPPORT:
    - https://www.twitch.tv/peacelaced
    - https://www.patreon.com/peacelaced
    - Donate Crypto:
        - WAX: rd2wo.wam
        - CoinBase: @peacelaced
        - MetaMask: 0x567ec43065991e4269Be19F4aEcac8C93c587619
    
@author: Brandon Black (PeaceLaced)
"""

import sys
import asyncio

'''
import logging
logging.basicConfig(level=logging.DEBUG)
'''
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

if "-chart" in opts:
    
    # for now this runs a dash chart, future, crate more opts
    import twit.twit_bots.twit_champ.data_visual.app
    
if "-twitchart" in opts:
    '''TWIT CHART Bot'''
    from twit.twit_bots.twit_chart.__main__ import Bot

    from twit.twit_api.api_twitch_auth import get_user_token
    from twitchio import Client
    from twitchio.ext import pubsub
    from twit.twit_api.config.config_twitch import ROOM_LIST
    from twit.twit_api.config.config_twitch import TWIT_PUBSUB_URI as URI
    from twit.twit_api.config.config_twitch import TWIT_PUBSUB_PORT as PORT
    from twit.twit_api.config.config_twitch import TWIT_PUBSUB_SCOPES as SCOPES
    from twit.twit_api.config.config_twitch import TWIT_PUBSUB_PATH_USER as USER_TOKEN_PATH
    from twit.twit_api.config.config_twitch import TWIT_PUBSUB_CLIENT as CLIENT_ID
    from twit.twit_api.config.config_twitch import TWIT_PUBSUB_SECRET as CLIENT_SECRET
    
    user_access_token = get_user_token(USER_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET, SCOPES, URI, PORT)
    
    #client = Client(token=user_access_token, initial_channels=ROOM_LIST, client_secret=CLIENT_SECRET)
    client = Client(token=user_access_token, initial_channels=ROOM_LIST)
    
    client.pubsub = pubsub.PubSubPool(client)
    bot = Bot()
    bot.pubsub_client = client
    
    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        await bot.event_pubsub_channel_points(event)
    
    bot.run()

if "-twitchamp" in opts:
    '''TWIT CHAMP Bot'''
    
    from twit.twit_bots.twit_champ.__main__ import Bot
    bot = Bot()
    bot.run()

if "-twitchant" in opts:
    '''TWIT CHANT Bot'''
    from twit.twit_bots.twit_chant.__main__ import Bot
    bot = Bot()
    bot.run()

if "-twitchartist" in opts:
    '''TWIT CHARTIST Bot'''
    from twit.twit_bots.twit_chartist.__main__ import Bot
    bot = Bot()
    bot.run()

if "-twitchalice" in opts:
    '''TWIT CHALICE Bot'''
    from twit.twit_bots.twit_chalice.__main__ import Bot
    bot = Bot()
    bot.run()

if "-twitchamber" in opts:
    '''TWIT CHAMBER Bot'''
    from twit.twit_bots.twit_chamber.__main__ import Bot
    bot = Bot()
    bot.run()
    
if "-fish" in opts:
    '''Terminal Fish Tank'''
    from twit.twit_misc.fish.__main__ import main
    main()
    
if "-fire" in opts:
    '''Terminal Fire'''
    from twit.twit_misc.fire.fire import run
    run()
    
if "-free" in opts:
    '''Terminal 256colour'''
    from twit.twit_misc.free.free import run
    run()
    
if "-test" in opts:
    '''test'''
    '''pubsub test'''
    from twit.twit_bots.test.test import run_test
    run_test()
    
if "-pubsub" in opts:
    '''pubsub test'''
    from twit.twit_bots.pubsub.pubsub import run_pubsub
    run_pubsub()

    
    