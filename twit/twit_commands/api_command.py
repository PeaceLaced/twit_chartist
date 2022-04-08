"""
- about command API.
# fully tested 28 Feb 2022
"""
def run_command_command(command, player, args):
    
    args_len = len(args)
    
    if args_len in {0}:
        
        return ['!command, !trade, !transfer, ' +
                '!stats, !value, !balance, ' +
                '!foss, !mic, !factorio, !ad, ' +
                '!guest, !end and !win. ' +
                'See the TWIT Game Commands panel for descriptions and arguments.']