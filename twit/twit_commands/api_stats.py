"""
- stats command API.
# fully tested 28 Feb 2022
"""
from twit.twit_api.api_command_handler import get_player_count, get_game_data

def run_stats_command(command, player, args):
    ''' games played, total players, current players'''
    
    total_players = get_player_count(count_type='total')
    current_players = get_player_count(count_type='current')
    game_data = get_game_data()
    game_count = game_data['WIT']['game']
    
    return [f'{player}, {game_count} games have been played with {total_players} total players. ' +
            f'There are currently {current_players} players playing.']