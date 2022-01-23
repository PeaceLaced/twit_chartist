"""
- Game bot that handles trading with TD Ameritrade using TwitchIO

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

from twitchio.ext import commands
from twit.twit_api.api_chat_handler import chat_handler
from twit.twit_api.config.config_twitch import ANT_TOKEN, ROOM_LIST
from twit.twit_api.api_trade_handler import get_client_session, get_symbols
from twit.twit_api.api_progress_handler import Progress as progress

class CommandHandlerTypeException(TypeError):
    '''Command Function handler return should be a list of string(s).'''
    def __init__(self, msg=None, *args, **kwargs):
        super().__init__(msg or self.__doc__, *args, **kwargs)

def check_return_list(handler_return):
    if not isinstance(handler_return, list):
        raise CommandHandlerTypeException('Command Function handler_return should be a list')

def check_return_string(handler_item):
    if not isinstance(handler_item, str):
        raise CommandHandlerTypeException('Command Function handler_item should be a string')
        
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ANT_TOKEN, prefix='~', initial_channels=ROOM_LIST)
        self.tda_client = get_client_session()
        
        # possible add a time check here so it doesnt grab after 4pm
        self.symbol_list = get_symbols(self.tda_client)

    # notify successful login/connect
    async def event_ready(self):
        channel=self.get_channel('peacelaced')
        await channel.send(f'{self.nick} has entered the room.')
        progress.clearly()
        progress.s(f'TO: {self.nick} BOT')
        
    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)
        
    @commands.command()
    async def live_trade(self, ctx: commands.Context, *args):
        ''' live-trade command, this is blocking '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args, self.tda_client)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')