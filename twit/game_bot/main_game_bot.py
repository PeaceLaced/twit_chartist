"""
- Main Game Bot. Jan 2022

- TwitchIO source: https://github.com/TwitchIO/TwitchIO

- TwitchIO docs: https://twitchio.readthedocs.io/en/latest/

"""

from twitchio.ext import commands
from twit.twitch_auth.config_twitch import ACCESS_TOKEN, ROOM_LIST

# bot API
from twit.game_bot.api_game_bot import chat_handler



class Bot(commands.Bot):
    '''main twitch bot class using TwitchIO
    
    :meth:`__init__` - sets auth, command prefix, and initial channel
    :meth:`event_ready` - prints message after successful connection
    
    @command.command() - the following are chat commands:
        
    - :meth:`commands` - returns a list of commands to the chat room
    - :meth:`balance` - return the WIT balance for the user
    - :meth:`trade` - trade a specific stock for a certain amt of time
    - :meth:`pool` - chat command used to interact with WIT pools
    
    balance
    - !pool [pool_type] [wit_amt]
    
    '''
    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=ROOM_LIST)

    # notify successful login/connect
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
    
##### TODO: bout command, make so only mod can trigger <>
    @commands.command()
    async def about(self, ctx: commands.Context):
        about_list = chat_handler(ctx.author.name, ctx.message.content)
        for about_section in about_list:
            await ctx.send(f'{about_section}')
        
    # get BOT commands
    @commands.command()
    async def command(self, ctx: commands.Context):
        command_list = chat_handler(ctx.author.name, ctx.message.content)
        for command_info in command_list:
            await ctx.send(f'{command_info}')
        
    # get WIT balance
    @commands.command()
    async def balance(self, ctx: commands.Context):
        handler_return = chat_handler(ctx.author.name, ctx.message.content)
        await ctx.send(f'{handler_return}')
        
    # make a specific trade
    @commands.command()
    async def trade(self, ctx: commands.Context):
        handler_return = chat_handler(ctx.author.name, ctx.message.content)
        await ctx.send(f'{handler_return}')
        
    # use WIT pool
    @commands.command()
    async def pool(self, ctx: commands.Context):
        handler_return = chat_handler(ctx.author.name, ctx.message.content)
        await ctx.send(f'{handler_return}')


''' (removed 13 Jan 2022, this prints chat to console)
async def event_message(self, message):
    # Ignore Messages with echo set to True, they are from teh bot
    if message.echo:
        return

    # Print the contents of our message to console...
    print(f'{message.author.name}:{message.content}')
    #print(message.content)
    #print(message.author.name + ": " + message.content)
    
    await self.handle_commands(message)
'''

'''
https://github.com/paulsens/channelpointbot/blob/master/channelpointbot.py
'''
# subscribing to pubsub for channel points
'''
from twitchio.ext import commands
import json

#oauth token with channel:read:redemptions scope, DO NOT pad with 'oauth:' like you do with the irc_token below
oauth = '<your redemption scoped oauth token>'

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:<your irc oauth token>', client_id='<your client id>', nick='<your bot name>', prefix='!',
                         initial_channels=['<your channel name>'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        print("Subscribing to channel points...\n\n")

        #to obtain your channel id, use Postman to send a GET to https://api.twitch.tv/helix/users?login=<your channel name>
            #with a header whose key is "client-id" and the corresponding value is your app's client id on the dev console
        await self.pubsub_subscribe(oauth, "channel-points-channel-v1.<your_channel_id>")

    # built to only process ! messages
    async def event_message(self, message):
        print(message.content)
        if(message.content[0]=="!"):
            await self.handle_commands(message)
    
    # original event_raw_pubsub method for this class
    async def event_raw_pubsub(self,  data):
        #data is given to us as a dictionary
        if data['type'] == 'MESSAGE':
            payload = data['data']['message']
            #but this payload is a json string
            payload = json.loads(payload)
            #now the payload is a dictionary, but it's nested as hell, so getting to the name of the reward is clunky

            title = payload['data']['redemption']['reward']['title']
            print("title is "+str(title))
            #title will exactly match the name of the reward that was redeemed
            #Now you can easily write if-statements to handle your different rewards. Enjoy!

    # extracted event_Raw_pubsub method from
    # https://github.com/EBraceyIV/Billager-Bot-TTV/blob/main/bbot-ttv.py
    async def event_raw_pubsub(self, data):
        # Server response, just let it happen
        if data["type"] == "PONG":
            pass
        # Handle channel point redemptions
        elif data["type"] == "MESSAGE":
            # The content of the pubsubs come through as JSON data, convert to a dict and then sorted through
            message = json.loads(data["data"]["message"])
            if message["type"] == "reward-redeemed":
                # Parse relevant info from the data received
                user = message["data"]["redemption"]["user"]["display_name"]
                user_input = message["data"]["redemption"]["user_input"]
                user_input_chars = len(user_input)
                reward = message["data"]["redemption"]["reward"]["title"]
                # Clatterbox messages are split up by character count for quality control / spam prevention / etc
                # More characters require more points to redeem
                # Users are notified if they are using too many characters for their redemption tier
                if reward == "Clatter S":
                    if user_input_chars <= 100:
                        chatter(user_input)
                    else:
                        await self.channel.send(f"@{user}, too many characters! This tier is only for 100 characters "
                                                "or less. You need to redeem a higher tier for that many.")
                elif reward == "Clatter M":
                    if user_input_chars <= 250:
                        chatter(user_input)
                    else:
                        await self.channel.send(f"@{user}, too many characters! This tier is only for 250 characters "
                                                "or less. You need to redeem a higher tier for that many.")
                elif reward == "Clatter L":
                    chatter(user_input)
                else:
                    pass
            else:
                # Print other MESSAGE messages to console for sorting through later
                pprint(data)
        # Print other events to console for sorting through later
        else:
            pprint(data)


    # Commands use a decorator...
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()

'''
# data returned from channel point message
'''
Example: Channel Points Event Message

{
"type": "reward-redeemed",
"data": {
  "timestamp": "2019-11-12T01:29:34.98329743Z",
  "redemption": {
    "id": "9203c6f0-51b6-4d1d-a9ae-8eafdb0d6d47",
    "user": {
      "id": "30515034",
      "login": "davethecust",
      "display_name": "davethecust"
    },
    "channel_id": "30515034",
    "redeemed_at": "2019-12-11T18:52:53.128421623Z",
    "reward": {
      "id": "6ef17bb2-e5ae-432e-8b3f-5ac4dd774668",
      "channel_id": "30515034",
      "title": "hit a gleesh walk on stream",
      "prompt": "cleanside's finest \n",
      "cost": 10,
      "is_user_input_required": true,
      "is_sub_only": false,
      "image": {
        "url_1x": "https://static-cdn.jtvnw.net/custom-reward-images/30515034/6ef17bb2-e5ae-432e-8b3f-5ac4dd774668/7bcd9ca8-da17-42c9-800a-2f08832e5d4b/custom-1.png",
        "url_2x": "https://static-cdn.jtvnw.net/custom-reward-images/30515034/6ef17bb2-e5ae-432e-8b3f-5ac4dd774668/7bcd9ca8-da17-42c9-800a-2f08832e5d4b/custom-2.png",
        "url_4x": "https://static-cdn.jtvnw.net/custom-reward-images/30515034/6ef17bb2-e5ae-432e-8b3f-5ac4dd774668/7bcd9ca8-da17-42c9-800a-2f08832e5d4b/custom-4.png"
      },
      "default_image": {
        "url_1x": "https://static-cdn.jtvnw.net/custom-reward-images/default-1.png",
        "url_2x": "https://static-cdn.jtvnw.net/custom-reward-images/default-2.png",
        "url_4x": "https://static-cdn.jtvnw.net/custom-reward-images/default-4.png"
      },
      "background_color": "#00C7AC",
      "is_enabled": true,
      "is_paused": false,
      "is_in_stock": true,
      "max_per_stream": { "is_enabled": false, "max_per_stream": 0 },
      "should_redemptions_skip_request_queue": true
    },
    "user_input": "yeooo",
    "status": "FULFILLED"
    }
  }
}

'''