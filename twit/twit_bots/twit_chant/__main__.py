"""
- Game bot that handles trading with TD Ameritrade using TwitchIO

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

from twitchio.ext import commands, routines
from twit.twit_commands.api_live_trade import run_live_trade_command
from twit.twit_api.api_trade_handler import get_client_session, update_symbol_list
from twit.twit_api.api_progress_handler import Progress as progress

from twit.twit_api.config.config_twitch import ROOM_LIST, STREAM_ID

from twit.twit_api.api_twitch_auth import get_user_token
from twit.twit_api.config.config_twitch import TWIT_CHANT_PORT as PORT
from twit.twit_api.config.config_twitch import TWIT_CHANT_URI as URI
from twit.twit_api.config.config_twitch import TWIT_CHANT_SCOPES as SCOPES
from twit.twit_api.config.config_twitch import TWIT_CHANT_CLIENT as CLIENT_ID
from twit.twit_api.config.config_twitch import TWIT_CHANT_SECRET as CLIENT_SECRET
from twit.twit_api.config.config_twitch import TWIT_CHANT_PATH_USER as USER_TOKEN_PATH

user_access_token = get_user_token(USER_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET, SCOPES, URI, PORT)

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

    def __init__(self):
        super().__init__(token=user_access_token, prefix='~', initial_channels=ROOM_LIST)
        self.tda_client = get_client_session()
        update_symbol_list(self.tda_client)
        self.livetradebot.start()

    async def event_ready(self):
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        await self.wait_for_ready()
        await channel.send('/me is ready to live trade. Lets make $ome money$.')
        progress.clearly()
        progress.s(f'TO: {self.nick} BOT')
        
    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    ###########################################################################
    # command functions
    @commands.command()
    async def live_trade(self, ctx: commands.Context, *args):
        ''' live-trade command, this is blocking '''
        
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_live_trade_command(self, command, author, command_args, self.tda_client)
        await send_chat_packet(self, chat_packet)
       
    '''    
    @commands.command()
    async def new_symbols(self, ctx: commands.Context, *args):
        # TODO: get a new Symbol List and write to database
        #if player in SUPER_USER:
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_new_symbol_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
    '''
    
###############################################################################
# routines
    
    @routines.routine(seconds=360, iterations=None)
    async def livetradebot(self):
        ''' '''
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        
        if self.distribution.completed_iterations not in {0}:

            if channel is not None:
                await channel.send("Hello, I'm the Chant Bot, I handle all the live stock trades.")