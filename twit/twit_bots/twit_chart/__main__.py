"""
- Main game bot that players interact with using TwitchIO

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

from twitchio.ext import commands

from twit.twit_commands.api_info import run_info_command
from twit.twit_commands.api_about import run_about_command
from twit.twit_commands.api_command import run_command_command
from twit.twit_commands.api_balance import run_balance_command
from twit.twit_commands.api_value import run_value_command
from twit.twit_commands.api_stats import run_stats_command
from twit.twit_commands.api_foss import run_foss_command
from twit.twit_commands.api_mic import run_mic_command
from twit.twit_commands.api_ad import run_ad_command
from twit.twit_commands.api_end import run_end_command
from twit.twit_commands.api_factorio import run_factorio_command
from twit.twit_commands.api_transfer import run_transfer_command
from twit.twit_commands.api_win import run_win_command
from twit.twit_commands.api_trade import run_trade_command

from twit.twit_api.api_progress_handler import Progress as progress
from twit.twit_api.config.config_twitch import ART_TOKEN, ROOM_LIST


class ChatPacketTypeException(TypeError):
    '''Command Function handler return should be a list of string(s).'''
    def __init__(self, msg=None, *args, **kwargs):
        super().__init__(msg or self.__doc__, *args, **kwargs)

async def send_chat_packet(self, chat_packet):
    ''' verify the chat packet and send the message'''
    if not isinstance(chat_packet, list):
        raise ChatPacketTypeException('The chat packet should be a list')
    for chat_message in chat_packet:
        if not isinstance(chat_message, str):
            raise ChatPacketTypeException('The chat packet should be a string')
        channel= self.get_channel('peacelaced')
        await channel.send(f'{chat_message}')

class Bot(commands.Bot):
    '''TWIT_CHART bot class using TwitchIO
    SOURCE: https://github.com/TwitchIO/TwitchIO/
    
    :meth:`__init__` - sets auth, command prefix, and initial channel
    :meth:`event_ready` - prints message after successful connection
    :meth:`event_message` - handle chat commands, ignore bot responses
    
    :meth:`@command.command()` - decorate functions that manage commands
    
    # use this to access points when the time comes
    https://github.com/paulsens/channelpointbot/blob/master/channelpointbot.py
    '''
    # TODO: this
    # look into ainit for database setup
    # self.loop.create_task(self.ainit())
    def __init__(self):
        super().__init__(token=ART_TOKEN,
                         #client_secret=CLIENT_SECRET,
                         prefix='!', 
                         initial_channels=ROOM_LIST,
                         case_insensitive=True)

    # look more into how I can do things similar to this
    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.errors.CommandNotFound):
            # beyond slow mode, think about how to limit people spam posting
            await ctx.send(f'{ctx.author.name}, USE: !command')
            
    async def event_ready(self):
        channel=self.get_channel('peacelaced')
        await channel.send(f'{self.nick} has entered the room.')
        progress.clearly()
        progress.s(f'TO: {self.nick} BOT')
    
    # TODO: pubsub will also need to check for user in database
    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)
               
# TODO: figure out what other modifier adjustment commands we are going to add (aside from !trade)
# TODO: investigate command delay response. sometimes it does not pick up written commands to chat
#       possible asyncio issue, need to convert run functions to async
# TODO: think about breaking out hardcoded values into constants (example: end command using 100)
# TODO: use update_game method to call app.py (dash app) any time modifier or total wit is changed
# TODO: check all activate_triggers for correctness
# TODO: create !add command maybe, to add wit to the system
# TODO: think more about !end fend, cost 1, trigger increase 100
# TODO: does int cast work for mongo INT32 and INT64????
# TODO: double check all end_game method casting
# TODO: investigate context for decimal chopping when over 10k using 0.25 decrease (low priority)
#       i dont think setting context at the top is doing anything, investigate further
#       possible rounding issue
# TODO: !balance <another_player> looks for chatter, use DB instead for player with wit > 0
# TODO: !transfer, same as above, look for active player
# TODO: rewrite INFO when I add to the ABOUT panel
# TODO: test TRADE and LIVE_TRADE tomorrow (monday 14 Feb 2022)
# TODO update the api_trade_handler for 0700 to 2000 (versus 10am to 4pm currently)
# TODO: get player data needs to return a message to either try command again
#       or invoke the command after being added to the database
# TODO: add the time slot to get_player_data method, as well as the other slots required for play (on pubsub)
# TODO: think more about default starting modifier (current is 0.1, steps 0.01)
#       because of the new system, way more wit will be given, but as that goes up, lower mod decreases value
#       ss some values to see what may happen over time etc etc
###############################################################################
# POOLS: ad, end, factorio, foss, live_trade, mic, trade, transfer, win
# WORKING: 
###############################################################################

    ###########################################################################
    # command functions
  
    @commands.command()
    async def info(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_info_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def about(self, ctx:commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_about_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    # cant use commands as function name, conflicts with @commands.command()
    async def command(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_command_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def value(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_value_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def stats(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_stats_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def foss(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_foss_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def mic(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_mic_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)   
    
    @commands.command()
    async def ad(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_ad_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def end(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_end_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
    
    @commands.command()
    async def factorio(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_factorio_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def trade(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_trade_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
 
    ###########################################################################
    # to access the bot, pass self to the run_<command>_command
    
    @commands.command()
    async def balance(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_balance_command(self, command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def transfer(self, ctx: commands.Context, *args):
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_transfer_command(self, command, author, command_args)
        await send_chat_packet(self, chat_packet)
    
    @commands.command()
    async def win(self, ctx: commands.Context, *args):
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_win_command(self, command, author, command_args)
        await send_chat_packet(self, chat_packet)
    


            
# everything has chat return,
#    AUTOMATICALLY PASSED,     is_SU      
# ((command, actual_p_name), (super_user ,(data, data)))
###############################################################################
# most complex, both are pretty much complete

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

###############################################################################
# pool only, also only (!end !factorio), other pools (!trade, !transfer)
# XXX: update wit value (all pools once triggered)

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

###############################################################################
# ends the game

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

###############################################################################
# no input (chat command) validation required (CURRENT)

# STATS     -   show game stats, current and overall
# !stats, show game stats

# VALUE     -   show wit value, calculation, explination
# !value, show current wit value

# BALANCE   -   let players see their balances
# !balance, show wit:x twit:x win:x

###############################################################################
# chat return only, no database access (DONE)

# COMMAND   -   !command
# !commands, both show the list of commands available

# INFO      -   three short info items
# !info, show game info

# ABOUT     -   (super user only)
# !about, long about message
###############################################################################
###############################################################################

# foss      - 1000 WIT   - release game code as free open sourece software
# mic       - 1000 WIT   - turn mic on for remainder of game
# ad        - 1000 WIT   - run an ad
# end       - 1000 WIT   - end the stream, no game winner, all WIT converts to TWIT
# factorio  - 1000 WIT   - play Factorio, end game, no winner, all WIT converts to TWIT
###############################################################################
# win       - 1 WIT (pool)     - increase the amount required to win the game by 0.1 WIT
# passing chan in win command
# - if sub, choice where to get gifted
# - if fol, choice where to get possible hosted
# THE OLD
# win       - 10 WIT    - amount required to win GIFTED or TWIT_CHAMP
# increase when pool is used
# if WIN, 
# - zero everything
# - convert wit to twit
# - write champ = true
###############################################################################
# pool_data = None 
    # FOSS      - release bot code as free open source software
    # - expand, after bot code release, next project release (algo bot strats)
    # MIC       - activate mic for remainder of GAME
    # - once per game
    # AD        - run an ad
    # - many per game
    # FACTORIO  -   play factorio
    # - once per stream, stop coding, play factorio, twit continues
###############################################################################
# trade     - 1 WIT(pool)      - trigger random live trade, change modifier based on profit/loss
###############################################################################
# transfer  - 1000 WIT (pool)  - increase the transfer amount by 0.01 WIT, 
#                                reduce trigger by 10 (max transfer rate 0.9)
# transfer WIT to another player, 1 to ratio 0.1/0.01/0.9 (start/step/max)
###############################################################################   
############################################################################### 
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

# future chat handler, maybe
''' I want to do this, but its a whole rewrite, colocate, validate in method
send print header when error, grab data with print header etc etc
# formatted like
# data_packet = ('print-header', 'data-to-print', etc, etc.)

# then straight down the line
print_header = data_packet[1]

print_headers = {
    ('print_header1', 'message_to_print'),
    ('print_header1', 'message_to_print'),
    ('print_header1', 'message_to_print'),
    ('print_header1', 'message_to_print'),
    # etc
    }
# have a set of all headers
# loop through the set
# 
for header in print_headers:
    if header[0] == print_header:
        return header[1]
'''