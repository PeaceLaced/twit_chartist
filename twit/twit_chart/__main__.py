"""
- Main game bot that players interact with using TwitchIO

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""
from twitchio.ext import commands
from twit.twit_api.api_chat_handler import chat_handler
from twit.twit_api.api_progress_handler import Progress as progress
from twit.twit_api.config.config_twitch import ART_TOKEN, ROOM_LIST

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
    '''TWIT_CHART bot class using TwitchIO
    
    :meth:`__init__` - sets auth, command prefix, and initial channel
    :meth:`event_ready` - prints message after successful connection
    :meth:`event_message` - handle chat commands, ignore bot responses
    
    :meth:`@command.command()` - call chat handlers that return chat data
    
    # use this to access points when the time comes
    https://github.com/paulsens/channelpointbot/blob/master/channelpointbot.py
    '''
    
    def __init__(self):
        super().__init__(token=ART_TOKEN, prefix='!', initial_channels=ROOM_LIST)

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
     
##### TODO: change new_chat_handler to chat_handler after rebuild        
    @commands.command()
    async def about(self, ctx:commands.Context, *args):
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
            
    @commands.command()
    async def rules(self, ctx: commands.Context, *args):
        ''' returns a list of game rules (simple)'''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def command(self, ctx: commands.Context, *args):
        ''' returns a list of commands or command details'''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def balance(self, ctx: commands.Context, *args):
        ''' return a string containing player WIT balance'''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
    
    @commands.command()
    async def pool(self, ctx: commands.Context, *args):
        ''' TODO '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def trade(self, ctx: commands.Context, *args):
        ''' return a string containing a live trade trigger and que message'''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def foss(self, ctx: commands.Context, *args):
        ''' TODO '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def mic(self, ctx: commands.Context, *args):
        ''' TODO '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def ad(self, ctx: commands.Context, *args):
        ''' TODO '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def end(self, ctx: commands.Context, *args):
        ''' TODO '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')
        
    @commands.command()
    async def win(self, ctx: commands.Context, *args):
        ''' TODO '''
        handler_return = chat_handler(ctx.author.name, ctx.command.name, args)
        check_return_list(handler_return)
        for handler_item in handler_return:
            check_return_string(handler_item)
            await ctx.send(f'{handler_item}')