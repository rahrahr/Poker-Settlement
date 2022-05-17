import pandas as pd
from collections import defaultdict
import json
import os

def read_file(filename=''):
    file_ = filename.split('/')[-1]
    if file_[:6] == 'ledger':
        return read_pokernow_file(filename)
    elif file_[-3:] == 'xls':
        return read_wpk_file(filename)

def read_folder(folder=''):
    res = []
    for file in os.listdir(folder):

        temp = read_file(folder+'/'+file)
        res.append(temp)
    
    df = pd.concat(res)
    assert df['pnl'].sum() == 0, 'Sum of PnL is not 0!'

    df = df.groupby('player').sum().reset_index()
    df['player'] = pd.Series(merge_user(df['player'].to_list()))
    df = df.groupby('player').sum().reset_index()
    df = df.sort_values('pnl', ascending=False)
    return df

def read_wpk_file(filename):
    df = pd.read_excel(filename, skiprows=1)
    df.columns = [x.strip() for x in df.columns]
    df = df.iloc[:, [1, -2]]
    df.columns = ['player', 'pnl']
    df['player'] = pd.Series(merge_user(df['player'].to_list()))

    assert df['pnl'].sum() == 0, 'Sum of PnL is not 0!'
    return df.sort_values('pnl', ascending=False)

def read_pokernow_file(filename):
    # pokernow csv usually contains mutiple entries for the same nickname.
    df = pd.read_csv(filename)
    df = df.iloc[:, [0, -1]]
    df.columns = ['player', 'pnl']

    assert df['pnl'].sum() == 0, 'Sum of PnL is not 0!'
    df['player'] = pd.Series(merge_user(df['player'].to_list()))
    df = df.groupby('player').sum().reset_index()
    df = df.sort_values('pnl', ascending=False)
    return df


def merge_user(names, special_names='./special_name_mapping.json'):
    # merge usernames that are substring of each other.
    if special_names:
        assert os.path.exists(special_names), 'Special Names Dictionary does not exists!'
        special_names_dict = json.load(open(special_names))
    else:
        special_names_dict = {}
        
    for i, name in enumerate(names):
        if name in special_names_dict:
            names[i] = special_names_dict[name]
            name = special_names_dict[name]

        for temp_name in names:
            if temp_name == name[:len(temp_name)]:
                names[i] = temp_name
            
            if name.isascii() and temp_name.isascii()\
                and temp_name.lower() == name.lower()[:len(temp_name)]:
                names[i] = temp_name.lower()
    return names
