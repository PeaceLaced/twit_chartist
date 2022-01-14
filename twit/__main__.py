"""
- Main Application Logic.

for current command list type !commands in chat:

"""


from twit.game_bot.main_game_bot import Bot

#from twit.game_bot.game_testing import test_game


def cli_main():
#async def cli_main():
    
    bot = Bot()
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.