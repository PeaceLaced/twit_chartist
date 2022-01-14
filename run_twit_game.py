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



opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

if "-twitchart" in opts:
    # for now this runs a dash chart, future, crate more opts
    import twit.data_visual.app
    
else:
    from twit.progress_report.api_progress_report import Progress as progress
    progress.w('IDENTIFY_SCRIPT_(run_twit_game.py)')
    from twit.__main__ import cli_main
    #asyncio.run(cli_main())
    cli_main()