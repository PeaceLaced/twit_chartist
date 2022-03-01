"""
- TWIT CHALICE game bot

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""
import twitchio
from twitchio.ext import commands
from twitchio.ext import routines
from twit.twit_api.api_progress_handler import Progress as progress

from twit.twit_api.config.config_twitch import ROOM_LIST

from twit.twit_api.api_twitch_auth import get_user_token
from twit.twit_api.config.config_twitch import TWIT_ALICE_PORT as PORT
from twit.twit_api.config.config_twitch import TWIT_ALICE_URI as URI
from twit.twit_api.config.config_twitch import TWIT_ALICE_SCOPES as SCOPES
from twit.twit_api.config.config_twitch import TWIT_ALICE_CLIENT as CLIENT_ID
from twit.twit_api.config.config_twitch import TWIT_ALICE_SECRET as CLIENT_SECRET
from twit.twit_api.config.config_twitch import TWIT_ALICE_PATH_USER as USER_TOKEN_PATH

user_access_token = get_user_token(USER_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET, SCOPES, URI, PORT)

class Bot(commands.Bot):
    '''main twitch bot class using TwitchIO
    
    :meth:`__init__` - sets auth, command prefix, and initial channel
    :meth:`event_ready` - prints message after successful connection
    
    @command.command() - the following are chat commands:
        
    - :meth:`about` - about the twit_champ bot
    '''
    def __init__(self):
        super().__init__(token=user_access_token, prefix='<', initial_channels=ROOM_LIST)
        self.randomlogic.start()

    # notify successful login/connect
    async def event_ready(self):
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        await self.wait_for_ready()
        
        await channel.send('/me is playing the game in mode: RANDOM')
        
        #await channel.send(f'{self.nick} has entered the room.')
        progress.clearly()
        progress.bot(f'TO: {self.nick} BOT')
        
    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            return
        
        if not message.echo:
            return
        
        #print(message.content)
        await self.handle_commands(message) 
        
###############################################################################
# routines
    
    @routines.routine(seconds=360, iterations=None)
    async def randomlogic(self):
        ''' '''
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        
        if self.distribution.completed_iterations not in {0}:
            
            if channel is not None:
                await channel.send("Hello, I'm Alice, a bot that will play TWIT using Random Logic.")