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
    '''Load the CHART bot, to play the game!'''
    from twit.twit_chart.__main__ import Bot
    bot = Bot()
    bot.run()

if "-twitchamp" in opts:
    '''Load the CHAMP bot, to be used by the winner of the previous game!'''
    from twit.twit_champ.__main__ import Bot
    bot = Bot()
    bot.run()

if "-twitchant" in opts:
    '''Load the CHANT bot, to post messages, rules, etc. to chat!'''
    from twit.twit_chant.__main__ import Bot
    bot = Bot()
    bot.run()
    
if "-empty" in opts:
    '''
    a placeholder for later use
    '''
    