# Specifically for parsing player_stats.txt

import pandas as pd
from collections import defaultdict

with open('player_stats.txt', 'r') as f:
    txt_file = [x.strip() for x in f.readlines()]

player_stats = defaultdict(dict)
section = 'Play Stats'

for line in txt_file[2:]:
    if section == 'Play Stats' and ':' in line:
        if 'Player' in line:
            current_player = line.split(':')[1].strip()
            continue

        property_name, value = line.split(':')

        if 'VPIP' in property_name:
            property_name = 'VPIP'
        elif 'Rounds Won' in property_name:
            property_name = 'Win Rate'
        elif 'Showdowns Won' in property_name:
            property_name = 'Showdown win rate'

        value = value.split('(')[1][:-1].strip()
        player_stats[current_player][property_name.strip()] = value.strip()
        if property_name == 'VPIP':
            player_stats[current_player]['# of Hands'] = line.split(
                '/')[-1].strip().split('(')[0].strip()

    elif 'Win Stats' in line:
        section = 'Win Stats'

    elif 'Preflop' in line:
        section = 'Preflop'

    elif section == 'Win Stats':
        if line and '(' not in line and 'Preflop' not in line:
            current_player = line.strip()
            continue

        if ':' in line:
            property_name, value = line.split(':')
            player_stats[current_player][property_name.strip()] = value.strip()

    elif section == 'Preflop' and ':' in line:
        if 'Player' in line:
            current_player = line.split(':')[1].strip()
            continue

        property_name, value = line.split(':')

        if '(' in property_name:
            property_name = property_name.split('(')[1].strip()[:-1].strip()
        if '(' in value:
            value = value.split('(')[1][:-1].strip()

        player_stats[current_player][property_name.strip()] = value.strip()

df = pd.DataFrame(player_stats).T
df['pnl'] = pd.read_excel('suggestion.xlsx', index_col='player')['pnl']
df['pnl/hh'] = df['pnl'] / df['# of Hands'].astype(float) * 100
df = df.sort_values('pnl/hh', ascending=False)
columns_reordered = [x for x in df.columns if x not in ('# of Hands', 'pnl', 'pnl/hh')] + ['# of Hands', 'pnl', 'pnl/hh']

df = df.reindex(columns=columns_reordered)
df.to_excel('player_stats.xlsx')
