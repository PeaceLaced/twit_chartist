"""
- TWIT CHAMBER game bot

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""
from random import randrange

import twitchio
from twitchio.ext import commands
from twitchio.ext import routines
from twit.twit_api.api_progress_handler import Progress as progress

from twit.twit_api.config.config_twitch import ROOM_LIST

from twit.twit_api.api_twitch_auth import get_user_token
from twit.twit_api.config.config_twitch import TWIT_AMBER_PORT as PORT
from twit.twit_api.config.config_twitch import TWIT_AMBER_URI as URI
from twit.twit_api.config.config_twitch import TWIT_AMBER_SCOPES as SCOPES
from twit.twit_api.config.config_twitch import TWIT_AMBER_CLIENT as CLIENT_ID
from twit.twit_api.config.config_twitch import TWIT_AMBER_SECRET as CLIENT_SECRET
from twit.twit_api.config.config_twitch import TWIT_AMBER_PATH_USER as USER_TOKEN_PATH

from decimal import Decimal, Context, ROUND_HALF_EVEN, localcontext, setcontext
setcontext(Context(prec=9, rounding=ROUND_HALF_EVEN))

user_access_token = get_user_token(USER_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET, SCOPES, URI, PORT)

class Bot(commands.Bot):
    '''main twitch bot class using TwitchIO
    
    :meth:`__init__` - sets auth, command prefix, and initial channel
    :meth:`event_ready` - prints message after successful connection
    
    @command.command() - the following are chat commands:
        
    - :meth:`about` - about the twit_champ bot
    '''
    def __init__(self):
        super().__init__(token=user_access_token, prefix='>', initial_channels=ROOM_LIST)
        
        # start the routines
        self.check_balance.start()
        self.make_trade.start()
        self.get_symbol_list.start()
        
        # set some bot values
        self.balance = Decimal(0.0)
        self.symbol_list = []
        
        # three variations, solo, comma, and period
        self.name_variations = ['TWIT_CHAMBER', 'TWIT_CHAMBER,', 'TWIT_CHAMBER.']

    # notify successful login/connect
    async def event_ready(self):
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        await self.wait_for_ready()
        
        await channel.send('/me is playing the game in mode: PREDICT')
        
        #await channel.send(f'{self.nick} has entered the room.')
        progress.clearly()
        progress.bot(f'TO: {self.nick} BOT')
        
    async def event_message(self, message: twitchio.Message) -> None:
        
        # messages from twit_chamber (this bot)
        if message.echo:
            return
        
        # build a list of words in each message, split, uppercase
        chat_message_split = []
        for message_item in message.content.split(' '):
            chat_message_split.append(message_item.upper())
        
        # TWIT_CHAMP bot
        if message.author.name in {'twit_champ'}:
            pass
        
        # TWIT_CHART bot
        if message.author.name in {'twit_chart'}:
            
            # all messages that have our name in it, posted by twit_chart
            for bot_name in self.name_variations:
                if bot_name in chat_message_split:
                    if 'WIT,' in chat_message_split:

                        try:
                            self.balance = Decimal(chat_message_split[chat_message_split.index('WIT,')-1])
                        except:
                            print('balance not set')
                    
            # set symbol list
            if chat_message_split[4] in {'SYMBOL'}:
                for message_item in message.content.split(' ')[6:]:
                    self.symbol_list.append(message_item.strip(','))
        
###############################################################################
# routines
    #if self.distribution.completed_iterations not in {0}:
        
    # get and set stock list for bot use
    @routines.routine(seconds=10, iterations=2)
    async def get_symbol_list(self):
        # does iterations need to be 2 if we skip the first iteration on boot?
        if self.get_symbol_list.completed_iterations not in {0}:
            await self.wait_for_ready()
            channel = self.get_channel('peacelaced')
            await channel.send('!trade list')
    
    # make a trade if our balance is over 1 WIT
    @routines.routine(seconds=60, iterations=None)
    async def make_trade(self):
        if self.balance >= Decimal(1):
            random_number = randrange(0, len(self.symbol_list)+1)
            random_time = randrange(25, 56) # seconds betwee 25 and 55
            for index, symbol in enumerate(self.symbol_list):
                if random_number == index:
                    random_stock = symbol
                    
            await self.wait_for_ready()
            channel = self.get_channel('peacelaced')
            await channel.send(f'!trade {random_stock} {random_time}')
            self.balance = self.balance - Decimal(1)
    
    # check bot_balance every five minutes
    @routines.routine(seconds=360, iterations=None)
    async def check_balance(self):
        
        await self.wait_for_ready()
        channel = self.get_channel('peacelaced')
        await channel.send('!balance')