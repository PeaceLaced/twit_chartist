"""
- TWIT CHAMBER game bot

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

from twitchio.ext import commands
from twit.twit_api.api_progress_handler import Progress as progress
from twit.twit_api.config.config_twitch import AMP_TOKEN, ROOM_LIST

class Bot(commands.Bot):
    '''main twitch bot class using TwitchIO
    
    :meth:`__init__` - sets auth, command prefix, and initial channel
    :meth:`event_ready` - prints message after successful connection
    
    @command.command() - the following are chat commands:
        
    - :meth:`about` - about the twit_champ bot
    '''
    def __init__(self):
        super().__init__(token=AMP_TOKEN, prefix='$', initial_channels=ROOM_LIST)

    # notify successful login/connect
    async def event_ready(self):
        channel=self.get_channel('peacelaced')
        await channel.send(f'{self.nick} has entered the room.')
        progress.clearly()
        progress.bot(f'TO: {self.nick} BOT')