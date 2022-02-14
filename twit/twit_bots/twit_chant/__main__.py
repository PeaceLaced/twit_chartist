"""
- Game bot that handles trading with TD Ameritrade using TwitchIO

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

from twitchio.ext import commands
from twit.twit_commands.api_live_trade import run_live_trade_command
from twit.twit_api.config.config_twitch import ANT_TOKEN, ROOM_LIST, SUPER_USER
from twit.twit_api.api_trade_handler import get_client_session, update_symbol_list
from twit.twit_api.api_progress_handler import Progress as progress

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
        super().__init__(token=ANT_TOKEN, prefix='~', initial_channels=ROOM_LIST)
        self.tda_client = get_client_session()
        update_symbol_list(self.tda_client)

    async def event_ready(self):
        channel=self.get_channel('peacelaced')
        await channel.send(f'{self.nick} has entered the room.')
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
       
    # TODO: make new_symbol command
    '''    
    @commands.command()
    async def new_symbols(self, ctx: commands.Context, *args):
        # TODO: get a new Symbol List and write to database
        #if player in SUPER_USER:
        command, author, command_args = ctx.command.name.upper(), ctx.author.name.upper(), args
        chat_packet = run_new_symbol_command(command, author, command_args)
        await send_chat_packet(self, chat_packet)
    '''