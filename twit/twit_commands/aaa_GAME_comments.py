###############################################################################
# TWITCH Info Pannels
# 
# TWIT Game About
'''
[UPDATE_ME] TWIT: The game of WITs. In this game players both work together and compete against each other to unlock events, make live stock trades, and ultimately win the game. 
FINISH ME:
(points to touch on)
+ WITs are the game currency
+ The value of WIT fluctuates based on a modifier of 0.01 divided by the total number of WIT in the system.
+ There are two ways to improve the value of WIT, spend them, or increase the modifier.
+ This can be accomplished by activating the live stock trade bot, after which, the profit or loss will be added to the modifier.
+ Work together, pool your resources, and gain more WIT.
+ The round starts when the first person makes the first purchase at a WIT value of 0.5.
+ This deems them the half-wit, forever displaying their name and current WIT total as a standard of measure.
+ Anyone that goes over the half-wit total WIT value also gets displayed, but as a nit-wit.
+ Keep an eye on these people as they are about to end the game.
+ When the game is over, everyone reaches their wits-end and all WIT is converted to TWIT, saved to the database, useless, begging for a future purpose.
+ The ultimate goal is to out-wit your opponents, collect as much WIT as possible, and claim the TWIT CHAMP title by activating the !win command. 
+ Winning the game affords you two privileges.
+ The first is a gift sub to my channel, or if already subbed, to any channel on twitch, paid for by the host. (
+ The second gives you control of the twit_champ bot that comes with special  abilities that can be used to influence the next game.
+ Will you hack, cheat, and steal your way to a friends victory, or spread evenly the power you hold over the other players
'''
# 
# TWIT Game Commands
'''
[UPDATE_ME]  #Command List
!command, !info, !value, !stats, !trade, !transfer 
!balance, !foss, !mic, !ad, !end, !factorio, !win
> **COMMAND**
>> !command
>>+ show the command list

> **INFO**
>> !info
>> + show information about the game

> **VALUE**
>> !value
>> + show the current WIT value, modifier and total

> **STATS**
>> !stats
>> + show total games played and total players overall

> **TRADE**
>> !trade
>> + show the trade pool balance and trigger

>> !trade list
>> + show the available symbols

>> !trade specs
>> + show how we obtained the symbols.

>> !trade [wit]
>> + add WIT to the trade pool

>> !trade [symbol] [seconds]
>> + live trade a symbol, holding the position for an amount of seconds

> **TRANSFER**
>> !transfer
>> + show the transfer pool balance and trigger

>> !transfer [wit]
>> + add WIT to the transfer pool

>> !transfer [active_player]
>> + transfer WIT to another player

> **BALANCE** 
>> !balance
>> + shows your balance stats (wit, twit, wins)

>> !balance [player_name]
>> + show the balance of another player

> **FOSS**
>> !foss
>> + show the foss pool balance and trigger

>> !foss [wit]
>> + add WIT to foss pool

> **MIC**
>> !mic
>> + show the mic pool balance and trigger

>> !mic [wit]
>> + add WIT to the mic pool

> **AD**
>> !ad
>> + show the ad pool balance and trigger

>> !ad [wit]
>> + add WIT to the ad pool

> **END**
>> !end
>> + show the end pool balance and trigger

>> !end fend
>> + increase the end pool trigger

>> !end [wit]
>> + add WIT to the end pool

> **FACTORIO**
>> !factorio
>> + show the factorio pool balance and trigger

>> !factorio [wit]
>> + add WIT to the factorio pool

> **WIN**
>> !win
>> + show the win pool balance and trigger

>> !win [wit]
>> + add WIT to the win pool

>> !win [valid_twitch_channel]
>> + win the game
'''
# 
# TWIT Game Rules
'''
[UPDATE_ME]  #Game Participation
> **Adding play time**
>> To start playing the game, select one of the four channel point icons to add play time. Options are 5 min, 15 min, 30 min and 60 min. Each icon cool down is the same as the length of play. This means you can have all four active at the same time, but never multiples of any one. When you have play time you are considered active, when you do not have play time you are considered inactive.

> **Active players**
>> Being active affords you privilege and ability. First, when you are active, you have access to all commands and parameters listed under TWIT Game Commands. Second, at the top of every minute you are given WITs at the current wit value. Finally, you must be active to use any command that cost WITs.

> **Inactive players**
>> Being inactive allows you to invoke commands that show stats and game state. Basically, every command is available, but you can not pass parameters. Having this ability allows you to gauge if you want to play or not.  

#Game Mechanics
> **Main game loop**
>> The main game loop consists of adding play time, earning WITs, spending WITs, live trading stock and winning or keeping others from winning.

> **WIT value, modifier, and total**
>> WIT value is determined by the formula WIT_modifier / WIT_total. The wit modifier starts at 0.1 and has the ability to fluctuate, however, it will never go above the current wit total or below 0.01. Therefore, the wit value will always be somewhere between 0 and 1. Wit total is very simply, the sum of all wit in the current game. This sum includes all player balance wit AND all pool balance wit.

> **Increasing WIT value [by total]**
>> By decreasing the amount of wit in the system you can increase the value of wit. This can be done by spending wit, transferring wit or triggering a pool. 

> **Increasing WIT value [by modifier]**
>> By increasing the wit modifier, you can increase the value of wit. The current method to increase the wit modifier is to make live trades. 

> **The trade command**
>> There are two ways to live trade stock in this game. The first is by invoking the trade command, followed by a symbol, followed by seconds. It looks like this (!trade AMC 45). It cost 1 wit to perform this action. The second way is to add to the trade pool. When the pool reaches 1 wit it will randomly select a stock and hold time. Use (!trade list) to see the available symbols. Use (!trade specs) to see the price range, net change, market cap and volume params used to select the symbols.

> **The transfer command**
>> Active players have the ability to transfer wit to other active players. The command to do this is (!transfer [active_player]) The transfer ratio starts at 1 to 0.1 wit, but can be increased by triggering the transfer pool (see pool mechanics below).

> **Winning/ending the game**
>> There are two ways to end the game. You can invoking the win command like this (!win [valid_twitch_chan]), or by adding to the end pool until the end pool trigger is activated.  In both cases, players can stop the game from ending (and should actively try and do this). In the case of win, it cost 10 wit, but players can add to the win pool to increase how much it cost to win the game. In the case of end, players can fend off attacks (!end fend) by spending 1 wit which adds 100 to the end pool trigger. At the end of every game, all wit is converted to twit, all pools are zeroed, and if win, game play begins again. If end, a new game will start next stream. 

#Pool Mechanics
> **Using Pools**
>> There are eight pools that can be added to and triggered. They are (win, trade, transfer, foss, mic, ad, end, and factorio). You can see the pool balance and trigger by invoking the command with no params like this (!foss) or (!trade). When a param of wit is added to the command, it adds to the pool, like this (!foss 0.25) or (!trade 0.33). Any float value between 0 and 1 (non-inclusive) will work, for example (0.00001 or 0.99).

> **Pool descriptions and triggers**
>> **trade pool**
>> + Triggering the trade pool will trade a random stock for a random amount of time. 
>> + The trade pool trigger is 1 wit.

>> **transfer pool**
>> + Triggering the transfer pool will increase the transfer ratio by 0.01 AND decrease the pool trigger by 10.
>> + The transfer pool trigger starts at 1000 wit.

>> **foss pool**
>> + Triggering the foss pool will release my current project as Free and Open Source Software. The game/trade bot source code will be first, followed by the play bots.
>> + The foss pool trigger is 1000 wit.

>> **mic pool**
>> + Triggering the mic pool will make me turn on my mic for the remainder of the game. Once a new game starts, the mic goes off.
>> + The mic pool trigger is 1000 wit.

>> **ad pool**
>> + Triggering the ad pool will make me play two minutes of twitch ads for all non subscribers.
>> + The ad pool trigger is 1000 wit.

>> **end pool**
>> + Triggering the end pool will make me end the stream. All wit will convert to twit, and there will be no twit champ. 
>> + The end pool trigger starts at 1000 wit.

>> **factorio pool**
>> + Triggering the factorio pool will make me play factorio for the remainder of the game. Once a new game starts, I go back to coding.
>> + The factorio pool trigger is 1000 wit.

>> **win pool**
>> + Triggering the win pool will increase the amount of wit required to win the game by 0.1 wit. 
>> + The win pool trigger is 1 wit.
'''

# todo's and things to think about moving forward

###############################################################################
################       TODOs from all files    ################################
###############################################################################

###############################################################################
### WORKING
###################################################

# TODO[refactor]:               update all functions to reflect what they return, see example below.
#                               EXAMPLE: async def event_message(self, message: twitchio.Message) -> None:
#                               EXAMPLE: def __init__(self, access_token: str, prefix: str, initial_channels: List[str]):

###############################################################################
### HIGH priority and/or things I really want to do
###################################################
# TODO[trade_api]:              fix times back to market hours only
# TODO[wit modifier]:           find more modifier adjustment commands besides !trade <symbol> <seconds>

# XXX[typing in standard lib]:  similarly, type hints for function/method params
# TODO[error_handling]:         look into similar functions, see example below
#                               EXAMPLE: async def event_command_error(self, ctx: commands.Context, error: Exception):
    # TODO[initialization]:         instead of __init__, look into ainit for database setup
#                               EXAMPLE: self.loop.create_task(self.ainit())
# TODO[sudo command]:           buildout sudo command (last_game, fresh_game, new_game, etc etc)
# TODO[play_remaining]:         end of stream, convert bought time to minutes
#                               on next game (new day) player may !enable? or something, to resume their time
# TODO[transfer command]:       once transfer ratio hits 0.9, revoke adding to transfer pool
# TODO[command_handler]:        mongodb $pull operator, then combine GUEST and GUEST_LIST

# TODO[pubsub]:         there is pause/unpause and accept/reject options in pubsub
#                       USE: (PATCH https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions)
#                       further automate reward redemptions
# TODO[pubsub]:         look into event.reward.image for custom bouncing icons on redemption etc etc
# TODO[info panels]:    rewrite and update the twitch info pannels, (new commands), (20min vs old)
# TODO[pool wit]:       champs use of end game pool wit
# TODO[pool wit]:       change pool code to remove 50% from total_wit when adding to pool
#                       and the last 50% when the pool is activated (incentivize pool use)
# TODO[player twit]:    each player accumulates twit, which has no use. 
#                       ive thought about conversion back to wit(lame), need something interesting!!!
# TODO[stats command]:  add total play time to player stats return
# TODO[trade command]:  !trade specs, volatility, price, volume, etc etc
#                       create a way for users to adjust (pool) these values
# TODO[sudo command]:   refresh trade list (call nasdaq script) possible player activated (pool)
# TODO[routines]:       figure out how to get WIT distribute at the top of every minute
# TODO[twit_champ]:     wit added to system, send to chat every five minutes instead of every one minute

###############################################################################
# refactor trade handler
#
# TODO[trade command]:  tda-api, equity_buy_market, "session": "SEAMLESS", "duration": "DAY"
#                       change to 7AM to 8PM (pre/post market) session/duration etc etc.
#                       get a limit price and change equity_buy_market to equity_buy_limit
'''
client.place_order(1000,  int(ACCOUNT_ID) equity_buy_limit('GOOG', 1, 1250.0)
        .set_duration(Duration.GOOD_TILL_CANCEL)
        .set_session(Session.SEAMLESS)
        .build())

tda_client.place_order(int(ACCOUNT_ID), equity_buy_market(order_symbol, order_shares))
'''

###############################################################################
### LOW priority and/or things I dont really want to do
#######################################################

# TODO[all pools]:          hard test adding to pool for each command
#                           decimal/float cast may be having issues (keeps missing 0.99, and others)
# TODO[!command command]:   do we want to add this?
# TODO[pubsub]:             move out of twit_commands? and into twit_pubsub?
# TODO[fucking asyncio]:    look into converting all code to asyncio

###############################################################################

###############################################################################
### COMMENTS TO KEEP, psudo code from built, etc etc...
#######################################################
# TRADE     -   live trade a stock to increase the modifier
# !trade, command and pool/trigger info
# !trade <wit>, add to pool (triggers random trade)
# !trade list, return symbol list to chat
# !trade <symbol> <seconds>, update modifier
# PLAYER COST: player['wit'] = 1 WIT
# POOL TRIGGER: 1 WIT
# XXX: update wit value (because 1 WIT)
# XXX: update wit value (because modifier changes)

# TRANSFER  -   trasnfer wit to player or add to pool
# !transfer, command and pool/trigger info
# !transfer <wit>, add to pool (triggers increase ratio/decrease pool trigger)
# !transfer <to_player>, transfer wit to player
# PLAYER COST: player['wit'] = 1 WIT
# POOL TRIGGER: 1000 (minus 10 per activation)
# TRANSFER RATIO: 0.1/0.01/0.9 (start/step/max)
# XXX: update wit value (because ratio sink)

# FOSS      -   release bot code as free open source software
# !foss, command and pool/trigger info
# !foss <wit>, add to foss pool
# PLAYER COST: <wit>
# POOL TRIGGER: 1000

# MIC       -   activate mic for remainder of GAME
# !mic, command and pool/trigger info
# !mic <wit>, add to mic pool
# PLAYER COST: <wit>
# POOL TRIGGER: 1000

# AD        -   run an ad
# !ad, command and pool/trigger info
# !ad <wit>, add to ad pool
# PLAYER COST: <wit>
# POOL TRIGGER: 1000

# FACTORIO  -   play factorio
# !factorio, command and pool/trigger info
# !factorio <wit>, add to factorio pool
# PLAYER COST: <wit>
# POOL TRIGGER: 1000

# WIN       -   get info or win the game
# !win, command and pool/trigger info
# !win <wit>, add to pool (triggers increase player cost)
# !win <twitch_chan>, gifted or listed
# PLAYER COST: player['wit'] = WIT['win']
# POOL TRIGGER: 1 WIT
# POOL STEP: 0.1, increase player cost

# END       -   end stream, end game, convert all wit to twit, no champ
# !end, command and pool/trigger info
# !end <wit>, add to end pool
# PLAYER COST: <wit>
# POOL TRIGGER: 1000
# added functionality, fend is a way to keep people from ending the stream, 
# adds 100 to trigger, does it make sense that it cost 1 wit to add 100 to the trigger???

# STATS     -   show game stats, current and overall
# !stats, show game stats

# VALUE     -   show wit value, calculation, explination
# !value, show current wit value

# BALANCE   -   let players see their balances
# !balance, show wit:x twit:x win:x

# COMMAND   -   !command
# !commands, both show the list of commands available

###############################################################################

# foss      - 1000 WIT   - release game code as free open sourece software
# mic       - 1000 WIT   - turn mic on for remainder of game
# ad        - 1000 WIT   - run an ad
# end       - 1000 WIT   - end the stream, no game winner, all WIT converts to TWIT
# factorio  - 1000 WIT   - play Factorio, end game, no winner, all WIT converts to TWIT

###############################################################################
# ACTUAL COMMAND LIST (w=wit, sy=symbol, se=seconds, to=valid_user)
###############################################################################  
# CURRENT using (if not db_required) (NO VALIDATION REQUIRED)
# !command, !info, !about
###############################################################################
# CURRENT using (if arg_count is None) (NO VALIDATION REQUIRED)
# !stats, !value, !balance
# !trade, !transfer, !foss, !mic, !ad, !win, !end, !factorio
###############################################################################
# CURRENT using (if isinstance(arg[1], WIT)) (DONE)
# !foss <w>, !mic <w>, !ad <w>, !end <w>, !factorio <w>
#
# !transfer <w>, !win <w>
# !trade <w>
###############################################################################
# CURRENT using (if valid_chan:) (DONE)
# !transfer <to>, !win <to>, !balance <to>
###############################################################################
# CURRENT using (if command in {trade, live_trade}) (DONE)
# !trade specs
# !trade list
# !trade <sy> <se>
###############################################################################

# twit_chart, this bot, (main trigger bot)
# - takes in chat commands
# - updates database
# - returns chat messages
# - pubsub to start people playing
#
# twit_champ, (main routine bot)
# - takes commands from champ (only ever one person at a time)
# - main game logic (@routines.routine)
#
# twit_chant, (main trade, live_trade bot)
# - handles all live_trade commands
# - sleeps (blocks) often
#
# twit_chalice, (player, randomly plays)
#
# twit_chamber, (player, plays using AI)

###############################################################################