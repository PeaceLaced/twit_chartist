"""
- pubsub channel point redemption API.

"""
from twit.twit_api.api_command_handler import get_player_data, update_player
from twit.twit_api.api_command_handler import calc_play_time

from twit.twit_api.api_progress_handler import Progress as progress

def run_pubsub_point_redemption(reward, reward_cost, player):
    ''' main pubsub point redemption function'''
    
    # make sure player is in DB
    player_data = get_player_data(player, query_type='COMMAND')
    
    # if player is on a guest list
    player_guest_status = player_data[player]['guest']
    if player_guest_status not in {'None'}:
        
        progress.crit(f'Refund {player} {reward_cost} channel points.')
        
        return [f'{player}, you are a guest of {player_guest_status}. Only non-guests may use ' +
                'channel points to add play time. Remove yourself with (!guest purge) and try again. ' +
                f'Your {reward_cost} channel points will be refunded within 24 hours.']
    
    # need guest data to return added to their acct
    guest_data = player_data[player]['guests']
    guest_data_count = len(guest_data)
    
    # get, calculate, and update play_active (players play time)
    play_active = player_data[player]['play_active']
    play_until = player_data[player]['play_until']
    update_play_time = calc_play_time(play_active, play_until)
    update_player(player, (update_play_time, reward_cost), update_type='TIME')
    
    if guest_data_count in {0}:
        return [f'{player} redeemed {reward_cost} channel points. 20 minutes of play time ' +
                'has been added to your account.']

    if guest_data_count in {1}:
        
        # handle guest_one
        guest_one = guest_data[0]
        guest_one_data = get_player_data(guest_one, query_type='COMMAND')
        guest_play_active = guest_one_data[guest_one]['play_active']
        guest_play_until = guest_one_data[guest_one]['play_until']
        update_play_active = calc_play_time(guest_play_active, guest_play_until)
        update_player(guest_one, (update_play_active, reward_cost), update_type='TIME')
        
        return [f'{player} redeemed {reward_cost} channel points. 20 minutes of play time ' +
                f'has been added to your account and your guest {guest_one}.']
        
    if guest_data_count in {2}:
        
        # handle guest_one
        guest_one = guest_data[0]
        guest_one_data = get_player_data(guest_one, query_type='COMMAND')
        guest_play_active = guest_one_data[guest_one]['play_active']
        guest_play_until = guest_one_data[guest_one]['play_until']
        update_play_active = calc_play_time(guest_play_active, guest_play_until)
        update_player(guest_one, (update_play_active, reward_cost), update_type='TIME')
        
        # handle guest_two
        guest_two = guest_data[1]
        guest_two_data = get_player_data(guest_two, query_type='COMMAND')
        guest_play_active = guest_two_data[guest_two]['play_active']
        guest_play_until = guest_two_data[guest_two]['play_until']
        update_play_active = calc_play_time(guest_play_active, guest_play_until)
        update_player(guest_two, (update_play_active, reward_cost), update_type='TIME')
        
        return [f'{player} redeemed {reward_cost} channel points. 20 minutes of play time ' +
                f'has been added to your account and your guests {guest_one} and {guest_two}.']