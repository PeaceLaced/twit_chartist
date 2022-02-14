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

There are three different bots for this game.
- OPTIONS:
    -twitchart, launches the main game bot that players interact with
    -twitchamp, launches the bot that the twit champ interacts with
    -twitchant, launches the bot that handles trading with TD Ameritrade
"""

import sys

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

if "-twitchart" in opts:
    '''TWIT CHART Bot'''
    from twit.twit_bots.twit_chart.__main__ import Bot
    bot = Bot()
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
    from twit.twit_misc.free.test import run
    run()
    
    