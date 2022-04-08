"""
- TWIT CHAMP the previous winner interacts with this game bot.

- TwitchIO source: https://github.com/TwitchIO/TwitchIO
- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/
"""

import twitchio
from twitchio.ext import routines
from twitchio.ext import commands
from twit.twit_api.api_command_handler import get_game_data, update_active_players
from twit.twit_api.api_progress_handler import Progress as progress

from twit.twit_api.config.config_twitch import ROOM_LIST

from twit.twit_api.api_twitch_auth import get_user_token
from twit.twit_api.config.config_twitch import TWIT_CHAMP_PORT as PORT
from twit.twit_api.config.config_twitch import TWIT_CHAMP_URI as URI
from twit.twit_api.config.config_twitch import TWIT_CHAMP_SCOPES as SCOPES
from twit.twit_api.config.config_twitch import TWIT_CHAMP_CLIENT as CLIENT_ID
from twit.twit_api.config.config_twitch import TWIT_CHAMP_SECRET as CLIENT_SECRET
from twit.twit_api.config.config_twitch import TWIT_CHAMP_PATH_USER as USER_TOKEN_PATH

user_access_token = get_user_token(USER_TOKEN_PATH, CLIENT_ID, CLIENT_SECRET, SCOPES, URI, PORT)

class Bot(commands.Bot):
    '''main twitch bot class using TwitchIO'''
        
    # def __init__(self, access_token: str, prefix: str, initial_channels: List[str]):
    def __init__(self):
        super().__init__(token=user_access_token, prefix='$', initial_channels=ROOM_LIST)
        
        # start the routine
        self.distribution.start()
        
    # async def event_ready(self) -> None:
    async def event_ready(self):
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        await self.wait_for_ready()
        await channel.send('/me is distributing WIT and waiting for commands from the TWIT Champ')
        progress.clearly()
        progress.bot(f'TO: {self.nick} BOT')
        
    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            return
        #print(message.content)
        await self.handle_commands(message)  

###############################################################################
# commands
  
    
###############################################################################
# routines
    # TODO: get this to update only at top of minute
    # TODO: every five minutes NOT one minute
    @routines.routine(seconds=60, iterations=None)
    async def distribution(self):
        ''' distribute wit to active players'''
        
        await self.wait_for_ready()
        channel=self.get_channel('peacelaced')
        
        # dont run the routine on boot
        if self.distribution.completed_iterations not in {0}:
            
            # get game data and wit_total
            game_data = get_game_data()
            wit_total = game_data['WIT']['total'].to_decimal()
            
            # only process non zero wit_totals
            wit_added_to_system = 0
            if wit_total not in {0}:
                
                wit_modifier = game_data['WIT']['modifier'].to_decimal()
                current_wit_value = wit_modifier / wit_total
                
                update_return = update_active_players(current_wit_value)

                wit_added_to_system = update_return[0]
                updated_how_many_players = update_return[1]
                
                # this will run every minute
                progress.bot(f'{current_wit_value} x ({updated_how_many_players})')
                
                if channel is not None:
                    await channel.send(f'Added {wit_added_to_system} WIT to the system.')
                    
            '''
            # this will run every two minutes
            # possible chance this to every five minutes with an accumulation
            if self.distribution.completed_iterations % 2 in {0}:
                if channel is not None:
                    await channel.send(f'Added {wit_added_to_system} WIT to the system.')
            '''
        '''
        
        if channel is not None:
            await channel.send(f'Distributing {current_wit_value} wit to all active players.')
        '''
        '''
        if channel is not None:
            await channel.send("Hello, I'm the Champ Bot, I will distribute WIT to active " +
                               "players and perform command actions on behalf of the TWIT Champ.")
        '''

###############################################################################
# pubsub

