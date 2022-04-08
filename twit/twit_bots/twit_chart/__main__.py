"""
- Main game bot that players interact with using TwitchIO

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

# twitch io imports
from twitchio.ext import commands, pubsub, routines

# logging and stderr
from twit.twit_api.api_progress_handler import Progress as progress

# all admin commands (as sudo)
from twit.twit_commands.api_sudo import run_sudo_command

# pubsub import
from twit.twit_commands.api_pubsub import run_pubsub_point_redemption

# all player commands
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
from twit.twit_commands.api_guest import run_guest_command
from twit.twit_commands.api_trade import run_trade_command

# twitch auth stuff and stream specific stuff
from twit.twit_api.config.config_twitch import ROOM_LIST, STREAM_ID
from twit.twit_api.api_twitch_auth import get_user_token, get_app_token
from twit.twit_api.config.config_twitch import TWIT_CHART_PORT as PORT
from twit.twit_api.config.config_twitch import TWIT_CHART_URI as URI
from twit.twit_api.config.config_twitch import TWIT_CHART_SCOPES as SCOPES
from twit.twit_api.config.config_twitch import TWIT_CHART_CLIENT as CLIENT_ID
from twit.twit_api.config.config_twitch import TWIT_CHART_SECRET as CLIENT_SECRET
from twit.twit_api.config.config_twitch import TWIT_CHART_PATH_USER as USER_TOKEN_PATH
from twit.twit_api.config.config_twitch import TWIT_CHART_PATH_APP as APP_TOKEN_PATH

user_access_token = get_user_token(USER_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET, SCOPES, URI, PORT)
get_app_token(APP_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET)

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
    '''
    def __init__(self):
        super().__init__(token=user_access_token,
                         #client_secret=CLIENT_SECRET,
                         prefix='!', 
                         initial_channels=ROOM_LIST,
                         case_insensitive=True)
        #self.main_game.start()
        self.pubsub_client = None
        
    async def event_command_error(self, ctx: commands.Context, error: Exception):
        ''' catch commands that do not exist and report to chat'''
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(f'{ctx.author.name}, Invalid command. USE: !command')
            
    async def event_ready(self):
        ''' 
        1) wait for bot chache to load, then send a message to chat
        2) clear terminal and print message that bot has loaded
        3) prep and connect to pubsub for channel point redemptions
        '''
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        await channel.send('/me has loaded the main game logic. Let the games begin.')
        
        progress.clearly()
        progress.s(f'TO: {self.nick} BOT')
        
        topics = [pubsub.channel_points(self.pubsub_client._http.token)[STREAM_ID]]
        await self.pubsub_client.pubsub.subscribe_topics(topics)
        await self.pubsub_client.connect()
        
    async def event_message(self, message):
        ''' ignore bot messages (echo), handle everything else'''
        if message.echo:
            return
        await self.handle_commands(message)

###############################################################################
# pubsub

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        ''' pubsub event handler, 20 min cost 100 points'''
        reward, cost, player = event.reward.title, event.reward.cost, event.user.name.upper()
        chat_packet = run_pubsub_point_redemption(reward, cost, player)
        await send_chat_packet(self, chat_packet)

###############################################################################
# routines
    
    @routines.routine(seconds=360, iterations=None)
    async def main_game(self):
        ''' '''
    
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        
        if self.distribution.completed_iterations not in {0}:
            
            if channel is not None:
                await channel.send("Hello, I'm the Chart Bot, I handle all the game commands, " +
                                   "most of the database updates, and the channel point redemptions. " +
                                   "I will be the first bot released when the FOSS pool is reached.")

###############################################################################
# commands
    
    @commands.command()
    async def sudo(self, ctx:commands.Context, *args):
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_sudo_command(command, author, command_args)
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
        
    @commands.command()
    async def balance(self, ctx: commands.Context, *args):
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_balance_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def transfer(self, ctx: commands.Context, *args):
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_transfer_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
        
    @commands.command()
    async def guest(self, ctx: commands.Context, *args):
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_guest_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)

    @commands.command()
    async def win(self, ctx: commands.Context, *args):
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_win_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)