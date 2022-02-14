"""
- about command API.

"""
from twit.twit_api.api_command_handler import is_SUPERUSER

# TODO: handle when the list is to big to go to chat (500 char)

def run_about_command(command, player, args):
    
    if not is_SUPERUSER(player):
        return [f'{player}: you are not authorized to use the about command.']
    
    return ['TWIT: The game of WITs. Buy the game currency WIT with earned channel ' +
    'points. The value of WIT fluctuates based on a modifier of 0.01 divided ' +
    'by the total number of WIT in the system. There are two ways to improve ' +
    'the value of WIT, spend them, or increase the modifier. This can be ' +
    'accomplished by activating the live stock trade bot, after which, the ' +
    'profit or loss will be added to the modifier.', 
    'Work together, pool your resources, and gain more WIT. The round starts ' +
    'when the first person makes the first purchase at a WIT value of 0.5. ' +
    'This deems them the `half-wit`, forever displaying their name and current ' +
    'WIT total as a standard of measure. Anyone that goes over the half-wit ' +
    'total WIT value also gets displayed, but as a nit-wit. Keep an eye on ' +
    'these people as they are about to end the game.', 
    'When the game is over, everyone reaches their wits-end and all WIT is ' +
    'converted to TWIT, saved to the database, useless, begging ' +
    'for a future purpose. The ultimate goal is to out-wit your opponents, ' +
    'collect as much WIT as possible, and claim the TWIT CHAMP title ' +
    'by activating the !win command. Winning the game affords you two privelages.',
    'The first is a gift sub to my channel, or if already subbed, to any channel ' +
    'on twitch, paid for by the host. The second gives you control of the ' +
    'twit_champ bot that comes with special abilities that can be used to ' +
    'influence the next round. Will you hack, cheat, and steal your way to a ' +
    'friends victory, or spread evenly the power you hold over the other players.']

    # fix to three paragraphs, all less than 500 chars each paragraph
    '''
    TWIT: The game of WITs. Buy the game currency WIT with earned channel  points. 
    The value of WIT fluctuates based on a modifier of 0.01 divided by the total 
    number of WIT in the system. There are two ways to improve  the value of WIT, 
    spend them, or increase the modifier. This can be  accomplished by activating 
    the live stock trade bot, after which, the  profit or loss will be added to 
    the modifier. Work together, pool your resources, and gain more WIT. The 
    round starts when the first person 

    makes the first purchase at a WIT value of 0.5.  This deems them the `half-wit`, 
    forever displaying their name and current  WIT total as a standard of measure. 
    Anyone that goes over the half-wit  total WIT value also gets displayed, but 
    as a nit-wit. Keep an eye on  these people as they are about to end the game. 
    When the game is over, everyone reaches their wits-end and all WIT is converted 
    to TWIT, saved to the database, useless, begging  for a future purpose.  
    The ultimate goal is to out-wit

    your opponents,  collect as much WIT as possible, and claim the TWIT CHAMP title 
    by activating the !win command. Winning the game affords you two privelages. 
    The first is a gift sub to my channel, or if already subbed, to any channel on 
    twitch, paid for by the host. The second gives you control of the  twit_champ 
    bot that comes with special abilities that can be used to influence the next 
    round. Will you hack, cheat, and steal your way to a  friends victory, or 
    spread evenly the power you hold over the other players.
    '''